""" Утилита для работы с конфигурацией.
"""

import yaml


class Config:
	""" Класс для работы с конфигурацией.
	"""

	def __init__(self, path: str):
		self.path = path

	def get_config(self):
		""" Получает конфигурацию.

		:return: Конфигурация.
		"""

		with open(self.path) as file:
			config = yaml.load(file, Loader=yaml.FullLoader)

		return config
