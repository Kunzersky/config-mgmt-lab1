"""A small command shell emulator for Stage 1 (REPL)."""

import getpass
import shlex
import socket
from collections.abc import Callable


CommandHandler = Callable[[list[str]], None]


def make_prompt() -> str:
	"""Build the shell prompt from the current system user and hostname."""
	username = getpass.getuser()
	hostname = socket.gethostname()
	return f"{username}@{hostname}:~$ "


def command_ls(arguments: list[str]) -> None:
	"""Handle the ls placeholder command."""
	print(f"ls: заглушка, аргументы: {arguments}")


def command_cd(arguments: list[str]) -> None:
	"""Handle the cd placeholder command."""
	print(f"cd: заглушка, аргументы: {arguments}")


def run_shell() -> None:
	"""Run the interactive command loop."""
	commands: dict[str, CommandHandler] = {
		"ls": command_ls,
		"cd": command_cd,
	}

	while True:
		try:
			line = input(make_prompt())
		except EOFError:
			print()
			break
		except KeyboardInterrupt:
			print()
			continue

		try:
			parts = shlex.split(line)
		except ValueError as error:
			print(f"shell: ошибка разбора команды: {error}")
			continue

		if not parts:
			continue

		command, arguments = parts[0], parts[1:]

		if command == "exit":
			break

		handler = commands.get(command)
		if handler is None:
			print(f"shell: command not found: {command}")
			continue

		handler(arguments)


if __name__ == "__main__":
	run_shell()
