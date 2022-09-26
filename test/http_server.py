""" API-сервер для взаимодействия с нейросетью.
"""

from argparse import ArgumentParser, Namespace

from flask import jsonify, request, Response, Flask
from gevent.pywsgi import WSGIServer

from core.io_processor.responder import Responder

app: Flask = Flask("cortex-api-io")

# Конфигурация Flask.
app.config["JSON_AS_ASCII"] = False # Для корректного отображения кириллицы.
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True # Для красивого отображения данных.


@app.route("/api/io")
def api_io() -> Response:
	""" Отвечает на запросы к API.

	:return: Ответ на запрос (flask.Response).
	"""

	# Проверка на наличие аргумента запроса.
	if "input" not in request.args:
		return jsonify({
			"status": "error",
			"error_text": "No input field provided. Please specify an input."
		})

	# Проверка на наличие текста в запросе.
	if request.args["input"] == "":
		return jsonify({
			"status": "error",
			"error_text": "No input text provided. Please specify an input text."
		})

	return jsonify({
		"status": "success",
		"question": str(request.args["input"]),
		"answer": str(responder.get_response(request.args["input"]))
	})


if __name__ == "__main__":
	arg_parser: ArgumentParser = ArgumentParser()

	arg_parser.add_argument("--host", type=str, help="Server host", default="0.0.0.0")
	arg_parser.add_argument("-p", "--port", type=int, help="Server port", default=5000)
	arg_parser.add_argument("-iomd", "--io-model-dir", type=str, help="The path to the I/O process model directory (default: ../io_processor/model)", default="../io_processor/model")

	args: Namespace = arg_parser.parse_args()

	responder: Responder = Responder(args.model_dir)

	http_server: WSGIServer = WSGIServer((args.host, args.port), app)
	http_server.serve_forever()
