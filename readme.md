# Cortex ᵃˡᵖʰᵃ ![Release](https://img.shields.io/github/v/release/hepller/cortex)

> RNN LTSM нейросеть для имитации общения

![Size](https://img.shields.io/github/repo-size/hepller/cortex)
![License](https://img.shields.io/github/license/hepller/cortex)

## Описание

__Cortex__ — Простая нейросеть для имитации диалога по принципу Вопрос/Ответ.

> Написано на Python с использованием библиотек [Keras](https://keras.io/) (+ [TensorFlow](https://www.tensorflow.org/))
> , [NLTK](https://www.nltk.org/) и [NumPy](https://numpy.org/) _на основе https://github.com/bartosz-paternoga/Chatbot_

Имеется интерфейс командной строки (CLI) и небольшой API-сервер для интеграции в чат-ботов: [`extra/readme.md`](extra/readme.md)

## Зависимости

- Python 3.10 и новее _(Совместимость с более ранними версиями не проверялась)_

_Дополнительные зависимости указаны в [`requirements.txt`](requirements.txt)_

```shell
# Установка зависимостей.
$ pip install -r requirements.txt

# Для обучения на CPU можно использовать tensorflow-cpu, вместо обычного tensorflow.

# Ненужные зависимости можно закоментировать перед установкой.
```

## Использование

### Использование препроцессора:

_(подготавливает данные для обучения)_

```python
from core.preprocessor import Preprocessor

# model_dir_path: Путь к директории с моделью.
# dataset_path: Путь к датасету.
preprocessor: Preprocessor = Preprocessor(model_dir_path="model", dataset_path="data.json")

# dataset_size: Размер датасета (вместо всего файла при обучении будет использовано только указанное кол-во элементов).
preprocessor.preprocess_dataset(dataset_size=200)
```

### Использование «тренера»:

_(обучает модель нейросеть)_

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

_(обрабатывает запрос и получает ответ)_

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
