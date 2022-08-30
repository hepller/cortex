# Cortex ᵇᵉᵗᵃ ![Release](https://img.shields.io/github/v/release/hepller/cortex)

> RNN LTSM нейросеть для имитации общения

![Size](https://img.shields.io/github/repo-size/hepller/cortex)
![License](https://img.shields.io/github/license/hepller/cortex)

## Описание

_Cortex_ — Простая нейросеть для имитации диалога по принципу Вопрос/Ответ

> Написано на Python с использованием библиотек [Keras](https://keras.io/) (+ [TensorFlow](https://www.tensorflow.org/)), [NLTK](https://www.nltk.org/) и [NumPy](https://numpy.org/)

_Сделано на основе https://github.com/bartosz-paternoga/Chatbot_

## Зависимости

- Python 3.10

_Дополнительные зависимости указаны в [`requirements.txt`](requirements.txt)_

## Установка и запуск

### Подготовка датасета

Перед запуском необходимо подготовить датасет `data.json` (нужно добавить этот файл в директорию) по которому будет обучаться модель

Пример элементов датасета:

```json5
[
  {
    "question": "Докажи", // Начальное высказывание
    "answer": "Не обязан" // Ответ на высказывание
  },
  {
    "question": "Кто",
    "answer": "Я"
  },
  
  // ...
]
```

### Запуск нейросети

```bash
# Установка зависимостей
$ pip install -r requirements.txt

# Переход в директорию ядра
$ cd core

# Подготовка модели
$ python preprocess.py

# Обучение модели
$ python train.py

# Запуск CLI
$ python conversation.py
```

## Лицензия

Copyright © 2022 [hepller](https://github.com/hepller)

Проект распространяется под лицензией [MIT](license)
