# UNIX shell emulator

A small UNIX-like shell that operates on an in-memory filesystem loaded from a ZIP archive.

## Quick start

```sh
./run.sh --help
make test
```

The emulator accepts `--vfs PATH` for a ZIP or base64-encoded ZIP and `--script PATH` for startup commands.
