import asyncio
import os
from typing import List

from app.api.routers.chat import chat_request
from app.api.routers.models import ChatData, MessageRole, Message
from app.api.routers.query import query_request
from app.engine.generate import generate_datasource, storage_dir
from app.settings import init_settings


async def run_query() -> None:
    text = input("Введите запрос: ")
    response = await query_request(text)
    print("\nОтвет:\n", response, "\n")


async def run_chat() -> None:
    messages: List[Message] = []

    print("Для выхода из чата введите /exit\n")

    while True:
        user_input = input("Вы: ")
        if user_input.strip().lower() == "/exit":
            break

        # Добавляем новое сообщение от пользователя
        messages.append(Message(
            role=MessageRole.USER,
            content=user_input,
            annotations=None
        ))

        # Отправляем всё, что накопилось, чтобы сохранить контекст
        chat_data = ChatData(
            data=None,
            messages=messages
        )
        response = (await chat_request(chat_data)).result.content

        # Запоминаем ответ ассистента в истории
        messages.append(Message(
            role=MessageRole.ASSISTANT,
            content=response,
            annotations=None
        ))

        print("\nАссистент:\n", response, "\n")


def main():
    # Инициализируем настройки
    init_settings()

    # Если индекс ещё не создан – строим и сохраняем его
    if not os.path.exists(storage_dir):
        generate_datasource()

    while True:
        print("Выберите режим:\n1) Запрос\n2) Чат\n3) Выход")
        choice = input("Введите номер: ").strip()

        if choice == "1":
            asyncio.run(run_query())
        elif choice == "2":
            asyncio.run(run_chat())
        elif choice == "3":
            print("До встречи!")
            break
        else:
            print("Неверный ввод. Повторите попытку.\n")


if __name__ == "__main__":
    main()
