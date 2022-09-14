""" API-сервер для взаимодействия с нейросетью.
"""

from argparse import ArgumentParser, Namespace

from flask import jsonify, request, Response, Flask
from gevent.pywsgi import WSGIServer

from core.responder import Responder

app: Flask = Flask("cortex-api-server")

# Конфигурация Flask.
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


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
	arg_parser.add_argument("-md", "--model-dir", type=str, help="The path to the model directory (default: ../model)", default="../model")

	args: Namespace = arg_parser.parse_args()

	# Небольшой костыль.
	responder: Responder = Responder(args.model_dir)

	http_server: WSGIServer = WSGIServer((args.host, args.port), app)
	http_server.serve_forever()
