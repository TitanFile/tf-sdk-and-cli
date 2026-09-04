# TitanFile SDK

Official SDK and CLI for the [TitanFile API](https://apidocs.titanfile.com).

---

## Installation

### Option 1 — macOS / Linux (one-line install)

```bash
curl -fsSL https://raw.githubusercontent.com/TitanFile/tf-sdk-and-cli/main/titanfile-sdk/install.sh | bash
```

Detects your OS and architecture, downloads the right binary, and installs it to `/usr/local/bin/titanfile`.

### Option 2 — Windows

Download `titanfile-windows-x64.exe` from the [latest release](https://github.com/TitanFile/tf-sdk-and-cli/releases/latest), rename it to `titanfile.exe`, and place it anywhere on your `PATH`.

### Option 3 — Python (pip)

Requires Python 3.8+.

```bash
pip install "git+https://github.com/TitanFile/tf-sdk-and-cli.git#subdirectory=titanfile-sdk"
```

### Manual binary download

All platform binaries are on the [releases page](https://github.com/TitanFile/tf-sdk-and-cli/releases/latest):

| Platform | File |
|---|---|
| Windows x64 | `titanfile-windows-x64.exe` |
| macOS Apple Silicon (M1/M2/M3) | `titanfile-macos-arm64` |
| macOS Intel | `titanfile-macos-x64` |
| Linux x64 | `titanfile-linux-x64` |

**macOS Gatekeeper** — if macOS blocks the binary on first run:
> System Settings → Privacy & Security → scroll down → click "Allow Anyway"

---

## CLI Usage

Credentials can be passed as flags or set once as environment variables:

```bash
export TITANFILE_API_ID=your-api-id
export TITANFILE_API_KEY=your-api-key
export TITANFILE_SUBDOMAIN=yourcompany
```

### Upload a file

```bash
titanfile upload --file /path/to/report.pdf
# {"file_id": "abc-123"}
```

Files larger than 500 MB are automatically uploaded in chunks.

### Create a channel

```bash
titanfile channel-create --name "Project Documents"
# {"channel_id": "xyz-456"}
```

### Send a message with a file

```bash
titanfile send \
  --channel xyz-456 \
  --file-id abc-123 \
  --owner-email you@yourcompany.com \
  --message "Please review the attached report."
```

### Search channels

```bash
titanfile channel-search --query "Project"
```

### All commands accept explicit credentials as flags

```bash
titanfile --api-id YOUR_ID --api-key YOUR_KEY --subdomain yourcompany upload --file report.pdf
```

---

## Python SDK Usage

```python
from titanfile import TitanFileClient

tf = TitanFileClient(
    api_id='YOUR_API_ID',
    api_key='YOUR_API_KEY',
    subdomain='yourcompany',
)

# Create a channel
channel_id = tf.channels.create('Project Documents')

# Add a contact
tf.channels.add_contact(channel_id, 'colleague@example.com')

# Upload a file (auto-chunks files > 500 MB)
file_id = tf.files.upload('/path/to/report.pdf')

# Send a message with the file
tf.messages.send(
    channel_id=channel_id,
    owner_email='you@yourcompany.com',
    message='Please review the attached report.',
    file_id=file_id,
)
```

### Available methods

**`tf.channels`**

| Method | Description |
|---|---|
| `create(name, custom_fields=None)` | Create a channel, returns UUID. Pass `custom_fields={'field': 'value'}` if the subscription has required custom fields. |
| `list(owner_email=None)` | List channels |
| `search(query, owner_email=None)` | Search channels by name |
| `add_contact(channel_id, email, role='manager')` | Add a member to a channel |

**`tf.files`**

| Method | Description |
|---|---|
| `upload(file_path, file_name=None)` | Upload a file, returns UUID. Auto-chunks files > 500 MB |

**`tf.messages`**

| Method | Description |
|---|---|
| `send(channel_id, owner_email, message, file_id, file_ids, folder_path, notify_contacts)` | Send a message |

---

## Large File Upload (> 200 MB)

The TitanFile API exposes chunked upload endpoints for files larger than 200 MB. These require multiple sequential API calls with specific session state. Rather than implementing this yourself, the SDK and CLI handle the full flow in a single call.

### Python SDK

Install:

```bash
pip install "git+https://github.com/TitanFile/tf-sdk-and-cli.git#subdirectory=titanfile-sdk"
```

Upload:

```python
from titanfile import TitanFileClient

client = TitanFileClient(
    api_id='YOUR_API_ID',
    api_key='YOUR_API_KEY',
    subdomain='yourcompany',
)

file_id = client.files.upload('/path/to/large-file.zip')
print(file_id)
```

The SDK detects the file size automatically and switches to chunked upload when needed. No extra configuration required.

### CLI Binary (no Python runtime required)

#### macOS / Linux

Install the CLI:

```bash
curl -fsSL https://raw.githubusercontent.com/TitanFile/tf-sdk-and-cli/main/titanfile-sdk/install.sh | bash
```

Then upload:

```bash
export TITANFILE_API_ID=your-api-id
export TITANFILE_API_KEY=your-api-key
export TITANFILE_SUBDOMAIN=yourcompany

titanfile upload --file /path/to/large-file.zip
# {"file_id": "abc-123"}
```

#### Windows

1. Download `titanfile-windows-x64.exe` from the [latest release](https://github.com/TitanFile/tf-sdk-and-cli/releases/latest).
2. Rename it to `titanfile.exe` and place it anywhere on your `PATH`.
3. Run:

```bat
titanfile upload ^
  --api-id YOUR_API_ID ^
  --api-key YOUR_API_KEY ^
  --subdomain yourcompany ^
  --file C:\path\to\large-file.zip
```

The output `file_id` can be passed directly to the send message endpoint.

---

## Releasing a new version

Tag the commit and push — GitHub Actions builds and publishes everything automatically:

```bash
git tag v1.0.1
git push origin v1.0.1
```

This triggers:
- Binaries built for Windows, macOS (Intel + Apple Silicon), Linux
- GitHub Release created with all four binaries attached
