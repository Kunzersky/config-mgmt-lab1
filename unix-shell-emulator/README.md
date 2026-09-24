# UNIX shell emulator

A small UNIX-like shell that operates on an in-memory filesystem loaded from a ZIP archive.

## Quick start

```sh
./run.sh --help
make test
```

The emulator accepts `--vfs PATH` for a ZIP or base64-encoded ZIP and `--script PATH` for startup commands.

## Built-in commands

`ls`, `cd`, `cat`, `chown`, `history`, `vfs_load`, and `exit` are available in the REPL.

## Project layout

- `src/vfs/` contains the in-memory tree and ZIP loader.
- `src/commands/` contains built-in commands.
- `scripts/` contains emulator-side command scripts.
- `os_scripts/` contains launch helpers for the host OS.
- `vfs_samples/` contains sample ZIP files for manual testing.

Run the complete scripted example with:

```sh
./os_scripts/run_with_script.sh
```
