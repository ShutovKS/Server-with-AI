# Сервер с AI агентом

[Русский](./README.md) | [English](./README.en.md)

## Описание

Сервер с AI агентом, который работает на основе LLM (Large Language Model) модели,
модели имеют доступ к различным инструментам:

- Поиск в интернете
- Поиск в Wikipedia
- Доступ к RAG с базой данных

## Установка

Для установки необходимо клонировать репозиторий и установить зависимости:

```bash
git clone <repo>
cd <repo>
pip install -r requirements.txt
```

В папку `data` необходимо добавить файлы .txt с текстом для базы знаний для RAG.

## Запуск

Для запуска сервера необходимо выполнить:

```bash
python main.py
```

Для пересоздания базы данных необходимо выполнить:

```bash
python ./app/engine/generate.py
```

## Использование

После запуска сервера, можно отправлять POST запросы на `http://127.0.0.1:8000/api/`

Обращение к ИИ в формате чата, доступ к БД и инструментам:

```bash
curl -X POST "http://127.0.0.1:8000/api/chat/request" -H "accept: application/json" -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"Что грозит человеку укравшему интеллектуальную собственность?"}]}'
```

Обращение к ИИ:

```bash
curl -X POST "http://127.0.0.1:8000/api/query/complete" -H "Content-Type: application/json" -d '{"query": "Что грозит
человеку укравшему интеллектуальную собственность?"}'
```

Обращение к ИИ с доступом к БД:

```bash
curl -X POST "http://127.0.0.1:8000/api/query/request-to-stored-index" -H "Content-Type: application/json" -d '{"
query": "Что грозит человеку укравшему интеллектуальную собственность?"}'
```

Обращение к ИИ с доступом к БД и инструментам:

```bash
curl -X POST "http://127.0.0.1:8000/api/query/request-agent" -H "Content-Type: application/json" -d '{"query": "Что
грозит человеку укравшему интеллектуальную собственность?"}'
```