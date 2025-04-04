import argparse
import os
import re


def parse_ssh_command(ssh_cmd):
    pattern = re.compile(
        r"^ssh\s+(?P<user>[^@]+)@(?P<host>\S+)\s+-p\s+(?P<port>\d+)\s+-i\s+(?P<identity>\S+)$"
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
    new_lines = []
    for block in blocks:
        new_lines.extend(block)
    return new_lines


def build_host_block(host_name, info):
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
    parser = argparse.ArgumentParser(
        description="Add or update a Host entry for RunPoid in ~/.ssh/config."
    )
    parser.add_argument(
        "--ssh_config",
        default="~/.ssh/config",
        required=True,
        help="The Host alias (e.g. 'siena').",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="The Host alias (e.g. 'siena').",
    )
    parser.add_argument(
        "--ssh_command",
        required=True,
        help="ssh command: 'ssh <user>@<host> -p <port> -i <identity_file>'.",
    )
    args = parser.parse_args()

    # 1) Parse the SSH command
    ssh_info = parse_ssh_command(args.ssh_command)

    # 2) Read ~/.ssh/config
    config_path = os.path.expanduser(args.ssh_config)
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    if os.path.isfile(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = []

    # 3) Split into blocks
    blocks = split_into_blocks(lines)

    # 4) TODO
    new_block = build_host_block(args.name, ssh_info)
    replaced = False

    for i, block in enumerate(blocks):
        first_line = block[0].rstrip()
        if first_line.lower().startswith("host "):
            # e.g. "Host siena" or "Host siena somethingelse"
            # If our target name is in that line, we replace the entire block
            host_patterns = first_line.split()[1:]  # skip "Host"
            if args.name in host_patterns:
                blocks[i] = new_block
                replaced = True
                break

    # 5) If not replaced, append the new block
    if not replaced:
        blocks.append(new_block)

    # 6) Write back
    final_lines = join_blocks(blocks)
    with open(config_path, "w", encoding="utf-8") as f:
        f.writelines(final_lines)

    print(f"Updated Host '{args.name}' in {config_path}")


if __name__ == "__main__":
    main()
