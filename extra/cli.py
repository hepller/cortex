""" Интерфейс командной строки (CLI).
"""

from core.respond import Responder

if __name__ == "__main__":
	cortex: Responder = Responder("../model")

	print("Running Cortex CLI ...")

	while True:
		query: str = input(str("> "))

		if query == "/exit":
			break

		print(cortex.handle_query(query))
