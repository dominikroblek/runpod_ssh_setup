# RunPod SSH Setup

A simple CLI tool to manage SSH config entries for [RunPod](https://www.runpod.io/). It
lets you add or update a `Host` block in your `~/.ssh/config` file automatically.

## Example

```bash
runpod_ssh_setup \
  --host runpod \
  --ssh_cmd "ssh root@157.517.221.29 -p 19090 -i ~/.ssh/id_ed25519"
```

This command will either replace an existing `Host runpod` block in your `~/.ssh/config`
or add one if it does not exist:

```txt
Host runpod
    HostName 157.517.221.29
    User root
    Port 19090
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

> **Tip**: You can copy the exact `--ssh_cmd` parameter directly from the RunPod
> Console:
> **Pods** → **_your pod_** → **Connect** → **Connection Options** → **SSH** →
> **SSH over exposed TCP**.

## Options

- `--config`: Path to your SSH config file (default: `~/.ssh/config`).
- `--host`: The alias to use in the `Host <ALIAS>` entry (required).
- `--disable_host_key_checking`: If present, adds lines that disable host key checks.
- `--ssh_cmd`: Must be in the exact format
  `ssh <USER>@<HOST> -p <PORT> -i <IDENTITY_FILE>`, as provided by RunPod.

### Disabling Host Key Checking

Adding `--disable_host_key_checking` inserts the following lines into the `Host` block:

```text
Host runpod
    ...
    UserKnownHostsFile /dev/null
    StrictHostKeyChecking no
```

By default, host key checking is enabled.

> **Security Note**: Disabling host key checking can be convenient for frequently
> changing or ephemeral hosts (such as cloud instances), but it increases the risk of
> man-in-the-middle attacks. We recommend keeping host key checks enabled in production
> or untrusted environments.

## Installation

If you have [Poetry](https://python-poetry.org/) installed:

```bash
poetry lock
poetry install
```

Then run via:

```bash
poetry run runpod_ssh_setup ...
```

Or build and install:

```bash
poetry build
pipx install dist/runpod_ssh_setup-*.whl
```

Then use `runpod_ssh_setup` directly.

## License

[MIT License](LICENSE)
