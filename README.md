# RunPod SSH Setup

A simple CLI tool to manage SSH config entries for [RunPod](https://www.runpod.io/).
It lets you add or update a `Host` block in your `~/.ssh/config` file automatically.

## Usage

```bash
runpod-ssh-setup \
  --name <HOST_ALIAS> \
  --ssh_command "ssh <USER>@<HOST> -p <PORT> -i <IDENTITY_FILE>"
```

### Example

```bash
runpod-ssh-setup \
  --name piran \
  --ssh_command "ssh root@157.517.221.29 -p 19090 -i ~/.ssh/id_ed25519"
```

This will either replace an existing `Host piran` block in your `~/.ssh/config`, or add
one if it does not exist. The resulting entry will be:

```txt
Host piran
    HostName 157.517.221.29
    User root
    Port 19090
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

### Options

- **`--ssh_config`**: Path to your SSH config file (default: `~/.ssh/config`).
- **`--name`**: The alias to use in the `Host <ALIAS>` entry  (default: runpod).
- **`--ssh_command`**: Must be in the exact format
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
poetry run runpod-ssh-setup ...
```

Alternatively, if you build and install it into your environment:

```bash
poetry build
pipx install dist/runpodssh-*.whl
```

Then use `runpod-ssh-setup` directly.

## License

This project is licensed under the [MIT License](LICENSE).
