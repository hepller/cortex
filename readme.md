# ⚠ Новый репозиторий: https://github.com/TheNodeOrg/cortex

## Cortex <sup>alpha</sup> ![Release](https://img.shields.io/github/v/release/hepller/cortex)

> Комплекс нейросетей для различных задач

## Описание

__Cortex__ — Комплекс из нейросетей, которые могут пригодиться для разных задач

## Компоненты

1. [I/O процессор](core/io_processor/readme.md) - LTSM рекуррентная нейросеть. Подходит для имитации диалога типа вопрос-ответ и т.п.
2. [~~Распознаватель объектов~~](core/object_recognizer/readme.md) *(TODO)*

## Зависимости

- Python 3.10 и новее

*Дополнительные зависимости указаны в [`requirements.txt`](requirements.txt)*

```shell
# Установка зависимостей для ядра.
$ pip install -r requirements.txt

# Установка зависимостей для тестировочных скриптов (при необходимости).
$ pip install -r test/dev_requirements.txt

# Для обучения на CPU можно использовать tensorflow-cpu, вместо обычного tensorflow.
```

## Лицензия

Copyright © 2022 [hepller](https://github.com/hepller)

Проект распространяется под лицензией [MIT](license)
