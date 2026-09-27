#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
exec "$root/run.sh" --vfs "$root/vfs_samples/deep_tree.b64" "$@"