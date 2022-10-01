# I/O процессор

> Сделано с использованием библиотек [Keras](https://keras.io/) (+ [TensorFlow](https://www.tensorflow.org/))
> , [NLTK](https://www.nltk.org/) и [NumPy](https://numpy.org/) на основе https://github.com/bartosz-paternoga/Chatbot

## Описание

Может использоватся для имитации диалога типа вопрос-ответ

Использование:

- [Подготовка данных для обучения](#подготовка-данных-для-обучения)
- [Обучение нейросети](#обучение-нейросети)
- [Получение ответа](#получение-ответа)

## Использование

### Подготовка данных для обучения

Сбор данных при помощи коллектора датасета:

```python
# ...

# Укажите токен.
bot: User = User(token="TOKEN")

# ...
```

```shell
$ python dataset_collector.py
```

Пример элементов датасета:

```json5
[
  {
    // Начальное высказывание.
    "input": "Докажи",
    // Варианты ответа на высказывание.
    "outputs": [
       "Не обязан",
       "Ещё что"
    ]
  },
  {
    "input": "Кто",
    "outputs": [
       "Я",
       "Не знаю"
    ]
  },
  // ...
]
```

Использование препроцессора данных:

```python
from core.io_processor.preprocessor import Preprocessor

# model_dir_path: Путь к директории с моделью.
# dataset_path: Путь к датасету.
preprocessor: Preprocessor = Preprocessor(model_dir_path="model", dataset_path="data.json")

# dataset_size: Размер датасета (вместо всего файла при обучении будет использовано только указанное кол-во элементов).
preprocessor.preprocess_dataset(dataset_size=200)
```

### Обучение нейросети

```python
from keras.losses import CategoricalCrossentropy
from keras.optimizers import Adam

from core.io_processor.trainer import Trainer

# model_dir_path: Путь к директории с моделью.
# model_name: Имя нейросети.
trainer: Trainer = Trainer(model_dir_path="model", model_name="cortex-test")

# epochs_count: Кол-во эпох.
# batch_size: Размер батча.
# overtrain: Будет ли дообучена существующая модель вместо создания новой.
# optimizer: Оптимизатор обучения (Keras).
# loss_function: Функция потерь (Keras).
trainer.train_model(epochs_count=900, batch_size=32, overtrain=False, optimizer=Adam(), loss_function=CategoricalCrossentropy())
```

### Получение ответа

```python
from core.io_processor.responder import Responder

# model_dir_path: Путь к директории с моделью.
responder: Responder = Responder(model_dir_path="model")

# query_text: Текст запроса.
response: str = responder.get_response(query_text="Запрос")

print(response)

# Прим. ответа: "не обязан".
```