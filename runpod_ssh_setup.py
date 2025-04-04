import argparse
import os
import re
from pathlib import Path

from loguru import logger


def parse_ssh_command(ssh_cmd):
    """Parse the given SSH command and return a dictionary with connection details."""
    pattern = re.compile(
        r"^ssh"
        r"\s+(?P<user>[^@]+)@(?P<host>\S+)"
        r"\s+-p\s+(?P<port>\d+)"
        r"\s+-i\s+(?P<identity>\S+)$"
    )
    m = pattern.match(ssh_cmd.strip())
    if not m:
        raise ValueError(f"SSH command not in the expected format: {ssh_cmd}")
    return {
        "User": m.group("user"),
        "HostName": m.group("host"),
        "Port": m.group("port"),
        "IdentityFile": m.group("identity"),
        "IdentitiesOnly": "yes",
    }


def split_into_blocks(lines):
    """Split the SSH config into blocks, where an unindented line starts a new block."""
    blocks = []
    current_block = []
    for line in lines:
        # If the line starts with a non-whitespace char, it's a new block
        if re.match(r"^\S", line):
            if current_block:
                blocks.append(current_block)
            current_block = [line]
        else:
            current_block.append(line)
    if current_block:
        blocks.append(current_block)
    return blocks


def join_blocks(blocks):
    """Join the list of blocks back into a list of lines."""
    new_lines = []
    for block in blocks:
        new_lines.extend(block)
    return new_lines


def build_host_block(host_name, info, disable_host_key_checking):
    """Build a Host block for the SSH config.

    If disable_host_key_checking is True, add lines that skip storing/validating the host key.
    """
    block = [
        f"Host {host_name}\n",
        f"    HostName {info['HostName']}\n",
        f"    User {info['User']}\n",
        f"    Port {info['Port']}\n",
        f"    IdentityFile {info['IdentityFile']}\n",
        "    IdentitiesOnly yes\n",
    ]
    if disable_host_key_checking:
        logger.warning(
            "Host key checking is disabled for '{}'. This may be insecure in production"
            " environments!",
            host_name,
        )
        block += [
            "    UserKnownHostsFile /dev/null\n",
            "    StrictHostKeyChecking no\n",
        ]
    block.append("\n")
    return block


def main():
    """CLI entry point for adding or updating a RunPod Host entry in an SSH config."""
    parser = argparse.ArgumentParser(
        description="Add or update a Host entry for RunPod in ~/.ssh/config."
    )
    parser.add_argument(
        "--config",
        default="~/.ssh/config",
        help="Path to SSH config file (default: ~/.ssh/config).",
    )
    parser.add_argument(
        "--host",
        required=True,
        help="The Host alias (e.g., runpod).",
    )
    parser.add_argument(
        "--disable_host_key_checking",
        action="store_true",
        help=(
            "If set, adds 'UserKnownHostsFile /dev/null' and 'StrictHostKeyChecking no' "
            "to disable host key checks. By default, host key checking is enabled."
        ),
    )
    parser.add_argument(
        "--ssh_cmd",
        required=True,
        help=(
            "SSH command provided by RunPod in exactly the format: "
            "'ssh <user>@<host> -p <port> -i <identity_file>'."
        ),
    )
    args = parser.parse_args()

    # Parse the SSH command
    ssh_info = parse_ssh_command(args.ssh_cmd)

    # Resolve config file path and ensure parent directory exists
    config_path = Path(args.config).expanduser()
    config_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)

    # Read existing lines if file exists
    file_exists = config_path.is_file()
    if file_exists:
        lines = config_path.read_text(encoding="utf-8").splitlines(keepends=True)
    else:
        lines = []

    # Split into blocks for manipulation
    blocks = split_into_blocks(lines)

    # Build our new or updated block
    new_block = build_host_block(
        args.host,
        ssh_info,
        args.disable_host_key_checking,
    )

    # Try to replace an existing block for this Host
    replaced = False
    for i, block in enumerate(blocks):
        first_line = block[0].rstrip()
        if first_line.lower().startswith("host "):
            host_patterns = first_line.split()[1:]  # Skip the word "Host"
            if args.host in host_patterns:
                logger.info("Found existing Host entry for '{}'. Replacing.", args.host)
                blocks[i] = new_block
                replaced = True
                break

    # If not replaced, append a new block
    if not replaced:
        logger.info(
            "No existing Host entry found for '{}'. Adding new entry.", args.host
        )
        if blocks:
            last_block = blocks[-1]
            # If the last line in the last block isn't empty, add a blank line
            if last_block and last_block[-1].strip():
                last_block.append("\n")
        blocks.append(new_block)

    # Reassemble final lines and write back to file
    final_lines = join_blocks(blocks)
    final_content = "".join(final_lines)
    config_path.write_text(final_content, encoding="utf-8")

    # Set strict permissions on new file if it didn't exist before
    if not file_exists:
        os.chmod(config_path, 0o600)

    if replaced:
        logger.info("Successfully updated Host '{}' in {}.", args.host, config_path)
    else:
        logger.info("Successfully added Host '{}' to {}.", args.host, config_path)


if __name__ == "__main__":
    main()
