# Cortex <sup>alpha</sup> ![Release](https://img.shields.io/github/v/release/hepller/cortex)

> RNN LTSM нейросеть для имитации диалогового общения

## Описание

__Cortex__ — Простая нейросеть для имитации диалога по принципу Вопрос/Ответ.

> Написано на Python с использованием библиотек [Keras](https://keras.io/) (+ [TensorFlow](https://www.tensorflow.org/))
> , [NLTK](https://www.nltk.org/) и [NumPy](https://numpy.org/) на основе https://github.com/bartosz-paternoga/Chatbot

Имеется интерфейс командной строки (CLI) и небольшой API-сервер для интеграции в чат-ботов: [`test/readme.md`](test/readme.md)

## Зависимости

- Python 3.10 и новее *(Совместимость с более ранними версиями не проверялась)*

*Дополнительные зависимости указаны в [`requirements.txt`](requirements.txt)*

```shell
# Установка зависимостей для ядра.
$ pip install -r requirements.txt

# Установка зависимостей для всего проекта, включая зависимости для тестировочных скриптов.
$ pip install -r dev_requirements.txt

# Для обучения на CPU можно использовать tensorflow-cpu, вместо обычного tensorflow.
```

## Использование

### Использование препроцессора:

*(Подготавливает данные для обучения)*

```python
from core.preprocessor import Preprocessor

# model_dir_path: Путь к директории с моделью.
# dataset_path: Путь к датасету.
preprocessor: Preprocessor = Preprocessor(model_dir_path="model", dataset_path="data.json")

# dataset_size: Размер датасета (вместо всего файла при обучении будет использовано только указанное кол-во элементов).
preprocessor.preprocess_dataset(dataset_size=200)
```

### Использование «тренера»:

*(Обучает модель нейросеть)*

```python
from core.trainer import Trainer

# model_dir_path: Путь к директории с моделью.
# model_name: Имя нейросети.
trainer: Trainer = Trainer(model_dir_path="model", model_name="cortex-test")

# epochs_count: Кол-во эпох.
# batch_size: Размер батча.
# overtrain: Будет ли дообучена существующая модель вместо создания новой.
trainer.train_model(epochs_count=900, batch_size=32, overtrain=False)
```

### Использование «ответчика»:

*(Обрабатывает запрос и получает ответ)*

```python
from core.responder import Responder

# model_dir_path: Путь к директории с моделью.
responder: Responder = Responder(model_dir_path="model")

# query_text: Текст запроса.
response: str = responder.get_response(query_text="Запрос")

print(response)

# Прим. ответа: "не обязан".
```

## Лицензия

Copyright © 2022 [hepller](https://github.com/hepller)

Проект распространяется под лицензией [MIT](license)