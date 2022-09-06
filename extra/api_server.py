""" API-сервер для взаимодействия с нейросетью.
"""

import os
import sys
from argparse import ArgumentParser, Namespace

from flask import jsonify, request, Response, Flask
from gevent.pywsgi import WSGIServer

# Исправление директории для импорта элементов ядра.
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from core.responder import Responder

responder: Responder = Responder("model")
app: Flask = Flask("cortex-api-server")

# Конфигурация Flask.
app.config["JSON_AS_ASCII"] = False


@app.route("/api")
def api() -> Response:
	""" Отвечает на запросы к API.

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
	arg_parser: ArgumentParser = ArgumentParser()

	arg_parser.add_argument("--host", type=str, help="Server host", default="0.0.0.0")
	arg_parser.add_argument("-p", "--port", type=int, help="Server port", default=5000)

	args: Namespace = arg_parser.parse_args()

	http_server: WSGIServer = WSGIServer((args.host, args.port), app)
	http_server.serve_forever()