# RunPod SSH Setup

Tired of manually updating your `~/.ssh/config` file every time you spin up a
[RunPod](https://www.runpod.io/) instance?

`runpod_ssh_setup` is a simple command-line tool that automates this. It takes the
standard SSH connection command provided by RunPod and automatically creates or updates
a corresponding `Host` entry in your SSH configuration file.

This allows you to connect to your pods using a simple alias (e.g., `ssh runpod`)
instead of the full command.

## How it Works: Example

1. Copy the SSH command from the RunPod UI:

   **Pods** → **_your pod_** → **Connect**
   → **Connection Options** → **SSH** → **SSH over exposed TCP**

2. Run the tool with your desired host alias:

   ```bash
   runpod_ssh_setup \
     --host runpod \
     --ssh_cmd "ssh root@157.517.221.29 -p 19090 -i ~/.ssh/id_ed25519"
   ```

3. The tool adds or updates the entry in `~/.ssh/config`:

   ```txt
   Host runpod
      HostName 157.517.221.29
      User root
      Port 19090
      IdentityFile ~/.ssh/id_ed25519
      IdentitiesOnly yes
   ```

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

### Option 1: Install From PyPI

Using `pip`:

```bash
pip install runpod_ssh_setup
```

This installs `runpod_ssh_setup` in your current environment (system-wide or
virtualenv).

For a global, isolated install, use [`pipx`](https://pypa.github.io/pipx/)
(recommended):

```bash
pipx install runpod_ssh_setup
```

### Option 2: Build From Source

If you have [Poetry](https://python-poetry.org/) installed:

```bash
poetry lock
poetry install
```

Then run:

```bash
poetry run runpod_ssh_setup ...
```

Or build a wheel and install it via pipx:

```bash
poetry build
pipx install dist/runpod_ssh_setup-*.whl
```

Then you can run `runpod_ssh_setup` directly.

## License

[MIT License](LICENSE)
