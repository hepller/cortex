# Cortex ᵃˡᵖʰᵃ ![Release](https://img.shields.io/github/v/release/hepller/cortex)

> RNN LTSM нейросеть для имитации общения

![Size](https://img.shields.io/github/repo-size/hepller/cortex)
![License](https://img.shields.io/github/license/hepller/cortex)

## Описание

_Cortex_ — Простая нейросеть для имитации диалога по принципу Вопрос/Ответ с встроенным интерфейсом командной строки (CLI)

> Написано на Python с использованием библиотек [Keras](https://keras.io/) (+ [TensorFlow](https://www.tensorflow.org/)), [NLTK](https://www.nltk.org/) и [NumPy](https://numpy.org/)

_Сделано на основе https://github.com/bartosz-paternoga/Chatbot_

## Зависимости

- Python 3.10 и новее _(Совместимость с более ранними версиями не проверялась)_

_Дополнительные зависимости указаны в [`requirements.txt`](requirements.txt)_

## Установка и запуск

### Подготовка датасета

Перед запуском необходимо директорию `data` и файл `data/data.json`

Далее нужно подготовить датасет  по которому будет обучаться модель

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

_Допустимо наличие элементов с одинаковым начальным высказыванием, но разными ответами_

### Конфигурация

После подготовки датасета необходимо открыть конфигурацию в файле `config.yml` и установить необходимые вам значения

### Запуск нейросети

Для запуска нейросети нужно поочередно ввести команды в терминал:

```bash
# Установка зависимостей
$ pip install -r requirements.txt
# Для обучения на CPU можно использовать tensorflow-cpu, вместо tensorflow

# Переход в директорию ядра
$ cd core

# Подготовка данных для обучения модели
$ python preprocess.py

# Обучение модели нейросети
$ python train.py

# Переход в директорию интерфейсов
$ cd ../interfaces

# Запуск интерфейса командной строки (CLI)
$ python cli.py

```

_Для выхода из CLI введите: `/exit`_

## Дополнительная информация

Описание содержимого директории `model` (появляется после подготовки и обучения модели)
:

```yaml
model.h5 # Данные весов нейросети (появляется после завершения обучения)
both.pkl # Дамп данных валидации + данных тренировки
test.pkl # Дамп данных для валидации нейросети при обучении
train.pkl # Дамп данных для тренировки нейросети
```

## Лицензия

Copyright © 2022 [hepller](https://github.com/hepller)

Проект распространяется под лицензией [MIT](license)
