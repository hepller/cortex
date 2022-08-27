import yaml

def get_config(path: str):
  """
  Получает конфигурацию.

  :param path: Путь к файлу конфигурации.
  :return: Конфигурация.
  """

  with open(path) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

  return config
