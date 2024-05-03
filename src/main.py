import datetime as dt
from datetime import datetime
import json

PROMPT_FOR_FORMAT_TIME = "Время вводится в формате 20 23 или 01 42."


def calculate_sleep_time(fall_asleep_time, wake_up_time, until_midnight=True):

    today = dt.date.today() - dt.timedelta(days=until_midnight)
    data_time_str = today.strftime("%Y-%m-%d") + " " + fall_asleep_time

    fall_asleep_time = datetime.strptime(data_time_str, "%Y-%m-%d %H:%M")

    today = dt.date.today()
    data_time_str = today.strftime("%Y-%m-%d") + " " + wake_up_time

    wake_up_time = datetime.strptime(data_time_str, "%Y-%m-%d %H:%M")

    return wake_up_time - fall_asleep_time


def validate_format_sleep_time(user_time):
    if (
        " " in user_time and 5 >= len(user_time) >= 4
    ):  # проверка длинны и наличия пробела
        hours, minutes = user_time.split()
        if hours.isdigit() and minutes.isdigit():  # проверка на цифры
            # проверки на адекватность цифр
            if not (0 <= int(hours) <= 23):
                print("Не бывает таких часов")
                return False
            if not (0 <= int(minutes) <= 59):
                print("Не бывает таких минут")
                return False
        else:
            print("Должны быть только цифры ")
            return False
    else:
        print("Не содержит пробел или неправильная длина")
        return False
    return True


def get_user_sleep_time(until_midnight):
    """
    Проверяет на корректность ввод пользователя и возвращает
    преобразовываем в нужный формат
    :param until_midnight
    :return 20:23  str:
    """
    print(PROMPT_FOR_FORMAT_TIME)

    fall_asleep_time = input(
        f"Введите время, в которое вы заснули {dt.date.today() - dt.timedelta(days=until_midnight)}:"
    ).strip()

    while not validate_format_sleep_time(fall_asleep_time):
        fall_asleep_time = input(
            f"Введите время, в которое вы заснули {dt.date.today() - dt.timedelta(days=until_midnight)}:"
        ).strip()

    # все проверки пройдены преобразовываем время в нужный формат
    hours, minutes = fall_asleep_time.split()
    fall_asleep_time = ":".join([hours, minutes])

    wake_up_time = input(f"Введите время, в которое вы проснулись {dt.date.today()}:")

    while not validate_format_sleep_time(wake_up_time):
        wake_up_time = input(
            f"Введите время, в которое вы проснулись {dt.date.today() - dt.timedelta(days=until_midnight)}:"
        ).strip()

    # все проверки пройдены преобразовываем время в нужный формат
    hours, minutes = wake_up_time.split()
    wake_up_time = ":".join([hours, minutes])

    return fall_asleep_time, wake_up_time


def save_users_data(
    fall_asleep_time, wake_up_time, sleep_time, state_of_sleep, users_note
):
    try:
        with open("data.json", "r", encoding="utf-8") as data_json:
            all_data_for_json = json.load(data_json)

    except FileNotFoundError:
        print("Файл не был найден.")
        all_data_for_json = []

    data_about_sleep = {
        "date": str(dt.date.today()),
        "time_to_sleep": fall_asleep_time,
        "wake_up_time": wake_up_time,
        "hours_slept": str(sleep_time),
        "sleep_quality": state_of_sleep,
        "notes": users_note,
    }

    all_data_for_json.append(data_about_sleep)

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(all_data_for_json, file, indent=4, ensure_ascii=False)


def process_sleep_data(until_midnight):
    fall_asleep_time, wake_up_time = get_user_sleep_time(until_midnight)
    sleep_time = calculate_sleep_time(fall_asleep_time, wake_up_time, until_midnight)
    state_of_sleep = input("Оцените состояние сна: good, average, bad ")
    users_note = input("Заполните заметки о сне. (Enter чтобы пропустить)")
    print(sleep_time)
    save_users_data(
        fall_asleep_time, wake_up_time, sleep_time, state_of_sleep, users_note
    )


def main():
    print(f"Привет, сегодня - {dt.date.today()}, пора вводить данные!")

    are_sleep_intervals = (
        input("Были ли промежутки во сне, длиной более, чем 30 минут? (да/нет)")
        .lower()
        .strip()
    )

    while not (are_sleep_intervals in ("да", "нет")):
        print("Недопустимое значение")
        are_sleep_intervals = (
            input("Были ли промежутки во сне, длиной более, чем 30 минут? (да/нет)")
            .lower()
            .strip()
        )

    if are_sleep_intervals == "да":
        ...
        # нужно сделать 2-ой режим (другой счет при наличии промежутков сна)
    elif are_sleep_intervals == "нет":
        user_answer = input(
            f"Вы заснули 1 - {dt.date.today()} (после полуночи) или 2 - {dt.date.today() - dt.timedelta(days=1)} (перед полуночью)?"
        )
        # позволяет выбрать время сна для более удобного счета

        while not (user_answer in ("1", "2")):
            print("Недопустимое значение")
            user_answer = input(
                f"Вы заснули 1 - {dt.date.today()} (после полуночи) или 2 - {dt.date.today() - dt.timedelta(days=1)} (перед полуночью)?"
            )

        if user_answer == "1":
            # вариант счета, если заснул после полуночи
            process_sleep_data(False)

        elif user_answer == "2":
            process_sleep_data(True)

            # вариант счета, если заснул до полуночи
    else:
        print("Неправильный ввод")
        # отсутсвуют другие варианты на данный момент


if __name__ == "__main__":
    main()
