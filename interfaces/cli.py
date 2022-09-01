""" Интерфейс командной строки (CLI).
"""

from core.main import Cortex

if __name__ == "__main__":
	cortex: Cortex = Cortex("../model")

	while True:
		query: str = input(str("> "))

		if query == "/exit":
			break

		print(cortex.handle_text(query))
