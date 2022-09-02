""" API-сервер для взаимодействия с нейросетью.
"""

from flask import jsonify, request, Response, Flask
from gevent.pywsgi import WSGIServer

from core.responder import Responder
from extra.utils.config import Config

config: Config = Config("config.yml")
responder: Responder = Responder("model")
app: Flask = Flask("cortex-api-server")

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
		"output": str(responder.get_response(request.args["query"]))
	})


if __name__ == "__main__":
	http_server = WSGIServer((config.get_api_host(), config.get_api_port()), app)
	http_server.serve_forever()
