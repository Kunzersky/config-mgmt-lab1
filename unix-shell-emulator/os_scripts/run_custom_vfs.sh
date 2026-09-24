#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
exec "$root/run.sh" --vfs "$root/vfs_samples/few_files.zip" "$@"
