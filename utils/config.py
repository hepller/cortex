""" Работа с конфигурацией.
"""

import yaml


class Config:
	""" Класс для работы с конфигурацией.
	"""

	def __init__(self, path: str) -> None:
		""" Инициализирует конфигурацию.

		:param path: Путь к файлу конфигурации.
		"""

		self.path = path

		with open(self.path) as file:
			self.config = yaml.load(file, Loader=yaml.FullLoader)

	def get_config(self) -> dict:
		""" Получает конфигурацию

		:return: Конфигурация
		"""

		return self.config

	def get_dataset_size(self) -> int:
		""" Получает размер датасета.

		:return: Размер датасета.
		"""

		return int(self.config["core"]["dataset_size"])

	def get_epochs_count(self) -> int:
		""" Получает кол-во эпох.

		:return: Кол-во эпох.
		"""

		return int(self.config["core"]["epochs_count"])

	def get_batch_size(self) -> int:
		""" Получает кол-во эпох.

		:return: Кол-во эпох.
		"""

		return int(self.config["core"]["batch_size"])

	def get_api_host(self):
		""" Получает хост на котором будет запускаться API.

		:return: Хост на котором будет запускаться API.
		"""

		return self.config["api"]["host"]

	def get_api_port(self):
		""" Получает порт на котором будет запускаться API.

		:return: Порт на котором будет запускаться API.
		"""

		return int(self.config["api"]["port"])
