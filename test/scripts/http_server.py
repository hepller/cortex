""" API-сервер для взаимодействия с нейросетью.
"""

from argparse import ArgumentParser, Namespace

from flask import jsonify, request, Response, Flask
from gevent.pywsgi import WSGIServer

from core.responder import Responder

app: Flask = Flask("cortex-api-server")

# Конфигурация Flask.
app.config["JSON_AS_ASCII"] = False # Для корректного отображения кириллицы.
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True # Для красивого отображения данных.


@app.route("/qa")
def qa_api() -> Response:
	""" Отвечает на запросы к API.

	:return: Ответ на запрос (flask.Response).
	"""

	# Проверка на наличие аргумента запроса.
	if "question" not in request.args:
		return jsonify({
			"status": "error",
			"error_text": "No question field provided. Please specify an query."
		})

	# Проверка на наличие текста в запросе.
	if request.args["question"] == "":
		return jsonify({
			"status": "error",
			"error_text": "No question text provided. Please specify an query text."
		})

	return jsonify({
		"status": "success",
		"question": str(request.args["question"]),
		"answer": str(responder.get_response(request.args["question"]))
	})


if __name__ == "__main__":
	arg_parser: ArgumentParser = ArgumentParser()

	arg_parser.add_argument("--host", type=str, help="Server host", default="0.0.0.0")
	arg_parser.add_argument("-p", "--port", type=int, help="Server port", default=5000)
	arg_parser.add_argument("-md", "--model-dir", type=str, help="The path to the model directory (default: ../model)", default="../model")

	args: Namespace = arg_parser.parse_args()

	# Небольшой костыль (чтобы путь к модели можно было указать через аргумент).
	responder: Responder = Responder(args.model_dir)

	http_server: WSGIServer = WSGIServer((args.host, args.port), app)
	http_server.serve_forever()
