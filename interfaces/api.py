""" API для взаимодействия с нейросетью.
"""

import flask
from flask import jsonify, request, Response

from core.handler import handle_text
from utils.config import Config

app = flask.Flask("cortex-api")

# Конфигурация Flask.
app.config["JSON_AS_ASCII"] = False


@app.route("/api")
def api() -> Response:
	""" Отвечает на запросы API

	:return: Ответ на запрос (flask.Response)
	"""

	if "query" not in request.args:
		return jsonify({
			"status": "error",
			"error_text": "No query field provided. Please specify an query."
		})

	return jsonify({
		"status": "success",
		"query": str(request.args["query"]),
		"output": str(handle_text("../model", request.args["query"]))
	})


if __name__ == "__main__":
	config = Config("../config.yml")

	app.run(host=config.get_api_host(), port=config.get_api_port())
