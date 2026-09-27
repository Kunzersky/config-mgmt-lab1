#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
cd "$root"
exec "$root/run.sh" --vfs "$root/vfs_samples/few_files.b64" --script "$root/scripts/test_all.txt" "$@"
