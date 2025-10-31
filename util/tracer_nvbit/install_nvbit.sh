#!/bin/bash
set -euo pipefail

export BASH_ROOT="$( cd "$( dirname "$BASH_SOURCE" )" && pwd )"
cd "$BASH_ROOT"

URL="https://github.com/NVlabs/NVBit/releases/download/v1.7.6/nvbit-Linux-x86_64-1.7.6.tar.bz2"
ARCHIVE="$BASH_ROOT/nvbit-Linux-x86_64-1.7.6.tar.bz2"
DEST_DIR="$BASH_ROOT/nvbit_release"

# Clean previous release dir
rm -rf "$DEST_DIR"
mkdir -p "$DEST_DIR"

# Remove any partially downloaded archives
rm -f "$ARCHIVE" "$ARCHIVE".* || true

echo "Downloading NVBit from: $URL"
if command -v wget >/dev/null 2>&1; then
	wget --tries=5 --timeout=30 --retry-connrefused --waitretry=2 -O "$ARCHIVE" "$URL"
elif command -v curl >/dev/null 2>&1; then
	curl -L --retry 5 --retry-delay 2 -o "$ARCHIVE" "$URL"
else
	echo "Error: neither wget nor curl is available for download." >&2
	exit 1
fi

echo "Verifying archive integrity..."
if ! bzip2 -tvv "$ARCHIVE" >/dev/null 2>&1; then
	echo "Error: NVBit archive appears to be corrupted. Please check your network and try again." >&2
	rm -f "$ARCHIVE"
	exit 2
fi

echo "Extracting NVBit to: $DEST_DIR"
tar -xjf "$ARCHIVE" -C "$DEST_DIR" --strip-components=1
rm -f "$ARCHIVE"

echo "NVBit installed at $DEST_DIR"
