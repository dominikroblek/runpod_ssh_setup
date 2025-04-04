# RunPod SSH Setup

A simple CLI tool to manage SSH config entries for [RunPod](https://www.runpod.io/).
It lets you add or update a `Host` block in your `~/.ssh/config` file automatically.

## Usage

```bash
runpod_ssh_setup \
  --host <HOST_ALIAS> \
  --ssh_cmd "ssh <USER>@<HOST> -p <PORT> -i <IDENTITY_FILE>"
```

> **Tip**: You can copy the exact `--ssh_cmd` parameter directly from the RunPod Console:
> **Pods** → **_your pod_** → **Connect** → **Connection Options** → **SSH** →
> **SSH over exposed TCP**.

> **Note**: By **default**, this script **disables host key checking** for the newly
> created or updated Host entry (for convenience when dealing with frequently changing
> hosts or cloud instances). For better security, see
> [Enabling Host Key Checking](#enabling-host-key-checking) below.

### Example

```bash
runpod_ssh_setup \
  --host runpod \
  --ssh_cmd "ssh root@157.517.221.29 -p 19090 -i ~/.ssh/id_ed25519"
```

This will either replace an existing `Host runpod` block in your `~/.ssh/config`, or add
one if it does not exist. **By default**, the resulting entry includes the lines that
**disable** host key checks:

```txt
Host runpod
    HostName 157.517.221.29
    User root
    Port 19090
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    UserKnownHostsFile /dev/null
    StrictHostKeyChecking no
```

### Enabling Host Key Checking

If you add `--enable_host_key_checking`, those last two lines are **omitted**, which means
SSH will **store** and **validate** the host key in `known_hosts`:

```bash
runpod_ssh_setup \
  --host runpod \
  --enable_host_key_checking \
  --ssh_cmd "ssh root@157.517.221.29 -p 19090 -i ~/.ssh/id_ed25519"
```

The resulting config entry will **not** include `UserKnownHostsFile /dev/null` or
`StrictHostKeyChecking no`, restoring SSH’s usual security checks.

> **Security Note**: Disabling host key checking can be convenient, but it exposes you to
> potential man-in-the-middle attacks. We recommend enabling host key checks (via
> `--enable_host_key_checking`) for production or untrusted environments.

### Options

- `--config`: Path to your SSH config file (default: `~/.ssh/config`).
- `--host`: The alias to use in the `Host <ALIAS>` entry (required).
- `--enable_host_key_checking`: If present, **skip** adding lines that disable host key
  checks. By default, **host key checking is disabled** for this Host entry.
- `--ssh_cmd`: Must be in the exact format
  `ssh <USER>@<HOST> -p <PORT> -i <IDENTITY_FILE>`, as provided by RunPod.

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

This project is licensed under the [MIT License](LICENSE).
