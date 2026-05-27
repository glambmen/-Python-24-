import requests
import telebot
from bs4 import BeautifulSoup


TOKEN = "8967568180:AAHhYZUSM_UvUSDdOgDijUCJNG-Fz-LgxII"

bot = telebot.TeleBot(TOKEN)


COUNTRIES = {
    "россия": "Москва",
    "франция": "Париж",
    "германия": "Берлин",
    "италия": "Рим",
    "япония": "Токио",
    "китай": "Пекин",
    "сша": "Вашингтон",
    "англия": "Лондон",
    "испания": "Мадрид",
    "бразилия": "Бразилиа"
}


def get_capital_info(capital):
    """Получает информацию о столице с Wikipedia."""
    try:
        url = f"https://ru.wikipedia.org/wiki/{capital}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = "utf-8"
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["sup", "style", "script"]):
            tag.decompose()

        paragraphs = soup.find_all("p")

        for paragraph in paragraphs:
            text = paragraph.get_text(" ", strip=True)

            if capital in text and len(text) > 100:
                return text[:900]

        for paragraph in paragraphs:
            text = paragraph.get_text(" ", strip=True)

            if len(text) > 100:
                return text[:900]

        return "Информация найдена, но описание не удалось выделить."

    except Exception as error:
        return f"Не удалось получить информацию о столице. Ошибка: {error}"


@bot.message_handler(commands=["start"])
def start_message(message):
    """Команда /start."""
    user_name = message.from_user.first_name

    text = (
        f"Здравствуйте, {user_name}!\n\n"
        "Я бот по теме «Столицы мира».\n\n"
        "Введите название страны,\n"
        "например:\n"
        "Россия\n"
        "Франция\n"
        "Япония"
    )

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["help"])
def help_message(message):
    """Команда /help."""
    text = (
        "Инструкция:\n\n"
        "Введите название страны.\n"
        "Бот покажет столицу и информацию о ней.\n\n"
        "Пример:\n"
        "Россия"
    )

    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def country_message(message):
    """Обработка кнопок и названия страны."""
    try:
        user_text = message.text.strip()
        country = user_text.lower()

        if country == "помощь":
            help_message(message)
            return

        if country == "показать информацию":
            bot.send_message(
                message.chat.id,
                "Введите название страны, например: Россия"
            )
            return

        if country in COUNTRIES:
            capital = COUNTRIES[country]

            bot.send_message(
                message.chat.id,
                f"Столица страны {user_text} — {capital}.\n"
                "Получаю информацию..."
            )

            info = get_capital_info(capital)

            bot.send_message(
                message.chat.id,
                f"Страна: {user_text}\n"
                f"Столица: {capital}\n\n"
                f"Информация:\n{info}"
            )
        else:
            bot.send_message(
                message.chat.id,
                "Страна не найдена.\n"
                "Введите название страны, например:\n"
                "Россия\nФранция\nГермания\nЯпония"
            )

    except Exception:
        bot.send_message(
            message.chat.id,
            "Произошла ошибка, но бот продолжает работу."
        )


def main():
    """Запуск бота."""
    print("Бот запущен.")

    try:
        bot.polling(non_stop=True)
    except Exception:
        print("Ошибка при работе бота.")


main()