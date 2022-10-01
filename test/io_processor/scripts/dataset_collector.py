""" Сборщик датасета из диалогов ВК.

Взят из старого проекта, над качеством кода не заморачивался.
"""

# TODO: Переписать.

import io
import json
import os.path
from typing import TextIO

from vkbottle.dispatch.rules.base import FromUserRule, PeerRule
# from vkbottle.bot import Bot, Message
from vkbottle.user import User, Message

# bot: Bot = Bot(token="TOKEN")
bot: User = User(token="TOKEN")

json_path: str = "../data/data.json"

if not os.path.exists(json_path):
	with io.open(json_path, "w") as file:
		json.dump([], file, indent=2, ensure_ascii=False)

with open(json_path, "rb") as json_file:
	json_data: list[dict[str, list[str]]] = json.load(json_file)


@bot.on.message(FromUserRule(), PeerRule())
async def handler(message: Message) -> None:
	""" Обрабатывает входящее сообщение.

	:param message: Объект сообщения.
	"""

	# Игнорирование сообщений без текста.
	if message.text == "":
		return None

	# Игнорирование сообщений без ответа.
	if message.reply_message is None:
		return None

	# Игнорирование сообщений с ответом на сообщения без текста.
	if message.reply_message.text == "":
		return None

	# Игнорирование сообщений от групп.
	if message.reply_message.from_id < 0 or message.from_id < 0:
		return None

	if message.from_id != 358163592:
		return None

	new_element: dict = {
		"input": message.reply_message.text,
		"outputs": [message.text]
	}

	# Сохранение первого элемента при пустом датасете.
	if len(json_data) == 0:
		json_data.append(new_element)

	curr_file: TextIO = open(json_path, "w")

	# Перебор датасета.
	for item in json_data:

		# Обработка элементов с полем "input" аналогичным тексту начального сообщения.
		if item["input"] == message.reply_message.text:

			# Обработка элементов, где нет такого-же ответа как в сообщении-ответе.
			if message.text not in item["outputs"]:

				# Добавление текста из сообщения-ответа.
				item["outputs"].append(message.text)

				json.dump(json_data, curr_file, indent=2, ensure_ascii=False)

				return None
			else:
				json.dump(json_data, curr_file, indent=2, ensure_ascii=False)  # Фикс удаления всего датасета при совпадающем ответе.

				return None

	json_data.append(new_element)

	json.dump(json_data, curr_file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
	bot.run_forever()
