# RunPod SSH Setup

A simple CLI tool to manage SSH config entries for [RunPod](https://www.runpod.io/).
It lets you add or update a `Host` block in your `~/.ssh/config` file automatically.

## Usage

```bash
runpod_ssh_setup \
  --host <HOST_ALIAS> \
  --ssh_cmd "ssh <USER>@<HOST> -p <PORT> -i <IDENTITY_FILE>"
```

### Example

```bash
runpod_ssh_setup \
  --host runpod \
  --ssh_cmd "ssh root@157.517.221.29 -p 19090 -i ~/.ssh/id_ed25519"
```

This will either replace an existing `Host runpod` block in your `~/.ssh/config`, or add
one if it does not exist. The resulting entry will be:

```txt
Host runpod
    HostName 157.517.221.29
    User root
    Port 19090
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

### Options

- **`--config`**: Path to your SSH config file (default: `~/.ssh/config`).
- **`--host`**: The alias to use in the `Host <ALIAS>` entry.
- **`--ssh_cmd`**: Must be in the exact format
  `ssh <USER>@<HOST> -p <PORT> -i <IDENTITY_FILE>`.

> **Note**: You can conveniently copy the exact --ssh_command parameter directly from
> the [RunPod Console](https://www.runpod.io/console/pods) under **Pods** →
> **\<pod_name\>** → **Connect** → **Connection Options** → **SSH** → **SSH over exposed
> TCP**.

## Installation

If you have [Poetry](https://python-poetry.org/) installed:

```bash
poetry install
```

This will install the script locally. You can then run it via:

```bash
poetry run runpod_ssh_setup ...
```

Alternatively, if you build and install it into your environment:

```bash
poetry build
pipx install dist/runpod_ssh_setup-*.whl
```

Then use `runpod_ssh_setup` directly.

## License

This project is licensed under the [MIT License](LICENSE).
