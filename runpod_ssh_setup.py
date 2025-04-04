import argparse
import os
import re


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
        if re.match(r"^\S", line):  # new unindented line => new block
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


def build_host_block(host_name, info):
    """Build a Host block for the SSH config."""
    return [
        f"Host {host_name}\n",
        f"    HostName {info['HostName']}\n",
        f"    User {info['User']}\n",
        f"    Port {info['Port']}\n",
        f"    IdentityFile {info['IdentityFile']}\n",
        "    IdentitiesOnly yes\n",
        "\n",
    ]


def main():
    """CLI entry point for adding or updating a Host entry in an SSH config."""
    parser = argparse.ArgumentParser(
        description="Add or update a Host entry for RunPod in ~/.ssh/config."
    )
    parser.add_argument(
        "--ssh_config",
        default="~/.ssh/config",
        required=True,
        help="Path to SSH config file (e.g., ~/.ssh/config).",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="The Host alias (e.g. 'siena').",
    )
    parser.add_argument(
        "--ssh_command",
        required=True,
        help="SSH command: 'ssh <user>@<host> -p <port> -i <identity_file>'.",
    )
    args = parser.parse_args()

    # Parse the SSH command
    ssh_info = parse_ssh_command(args.ssh_command)

    # Read or create the SSH config file
    config_path = os.path.expanduser(args.ssh_config)
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    if os.path.isfile(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = []
    blocks = split_into_blocks(lines)

    # Build the new Host block
    new_block = build_host_block(args.name, ssh_info)
    replaced = False

    # Try to replace an existing block for this Host
    for i, block in enumerate(blocks):
        first_line = block[0].rstrip()
        if first_line.lower().startswith("host "):
            host_patterns = first_line.split()[1:]  # skip "Host"
            if args.name in host_patterns:
                blocks[i] = new_block
                replaced = True
                break

    # If not replaced, append a new block
    if not replaced:
        if blocks:
            last_block = blocks[-1]
            if last_block and last_block[-1].strip():
                last_block.append("\n")
        blocks.append(new_block)

    # Write the updated config back to the file
    final_lines = join_blocks(blocks)
    with open(config_path, "w", encoding="utf-8") as f:
        f.writelines(final_lines)

    print(f"Updated Host '{args.name}' in {config_path}")


if __name__ == "__main__":
    main()
