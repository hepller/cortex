""" API для взаимодействия с нейросетью.
"""

from flask import jsonify, request, Response, Flask

from core.responder import Responder
from extra.utils.config import Config

config: Config = Config("config.yml")
cortex: Responder = Responder("model")
app: Flask = Flask("cortex-api")

# Конфигурация Flask.
app.config["JSON_AS_ASCII"] = False


@app.route("/api")
def api() -> Response:
	""" Отвечает на запросы API.

	:return: Ответ на запрос (flask.Response).
	"""

	# Проверка на наличие аргумента запроса.
	if "query" not in request.args:
		return jsonify({
			"status": "error",
			"error_text": "No query field provided. Please specify an query."
		})

	# Проверка на наличие текста в запросе.
	if request.args["query"] == "":
		return jsonify({
			"status": "error",
			"error_text": "No query text provided. Please specify an query text."
		})

	return jsonify({
		"status": "success",
		"query": str(request.args["query"]),
		"output": str(cortex.handle_query(request.args["query"]))
	})


if __name__ == "__main__":
	app.run(host=config.get_api_host(), port=config.get_api_port())
