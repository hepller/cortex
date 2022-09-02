""" Интерфейс командной строки (CLI).
"""

from core.responder import Responder

if __name__ == "__main__":
	responder: Responder = Responder("model")

	print("Running Cortex CLI ...")

	while True:
		query: str = input(str("> "))

		if query == "/exit":
			break

		print(responder.get_response(query))
