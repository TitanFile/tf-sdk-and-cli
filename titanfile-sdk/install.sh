#!/usr/bin/env bash
set -euo pipefail

REPO="TitanFile/tf-sdk-and-cli"
INSTALL_DIR="/usr/local/bin"
BINARY_NAME="titanfile"

# Detect OS and architecture
OS="$(uname -s)"
ARCH="$(uname -m)"

case "$OS" in
  Linux)
    ASSET="titanfile-linux-x64"
    ;;
  Darwin)
    case "$ARCH" in
      arm64) ASSET="titanfile-macos-arm64" ;;
      x86_64) ASSET="titanfile-macos-x64" ;;
      *) echo "Unsupported macOS architecture: $ARCH"; exit 1 ;;
    esac
    ;;
  *)
    echo "Unsupported OS: $OS"
    echo "On Windows, download titanfile-windows-x64.exe from:"
    echo "https://github.com/$REPO/releases/latest"
    exit 1
    ;;
esac

# Get latest release download URL
DOWNLOAD_URL=$(
  curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" \
    | grep "browser_download_url" \
    | grep "$ASSET" \
    | cut -d '"' -f 4
)

if [ -z "$DOWNLOAD_URL" ]; then
  echo "Could not find release asset: $ASSET"
  exit 1
fi

echo "Downloading $ASSET..."
curl -fsSL "$DOWNLOAD_URL" -o "/tmp/$BINARY_NAME"
chmod +x "/tmp/$BINARY_NAME"

# Install
if [ -w "$INSTALL_DIR" ]; then
  mv "/tmp/$BINARY_NAME" "$INSTALL_DIR/$BINARY_NAME"
else
  echo "Installing to $INSTALL_DIR (requires sudo)..."
  sudo mv "/tmp/$BINARY_NAME" "$INSTALL_DIR/$BINARY_NAME"
fi

echo "titanfile installed to $INSTALL_DIR/$BINARY_NAME"
titanfile --help
