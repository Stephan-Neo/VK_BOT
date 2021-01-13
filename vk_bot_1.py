import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlite3

# ссылка на бота в вк https://vk.com/im?media=&sel=-200020330
vk_session = vk_api.VkApi(token="607f22888eefc4fa2a9ee847aa4a4ad181a45b6e432e7741a101df2f633eac53fc7f6c0578f33b3326397")
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
Random = 0
conn = sqlite3.connect("db.db")
c = conn.cursor()
message_for_admin = []


def answer_message(text=""):
    vk.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random_id()
    )


def random_id():
    global Random
    Random += random.randint(0, 1000000)
    return Random


# def check_if_exists(user_id):
#     c.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
#     result = c.fetchone()
#     if result is None:
#         return False
#     return True


# def register_new_user(user_id):
#     c.execute("INSERT INTO users(user_id, message) VALUES (%d, '')" % user_id)
#     conn.commit()


def upload_picture(file):
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages(file)
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(peer_id=event.peer_id, random_id=0, attachment=attachment)


def change_keyboard(text, keyboard):
    vk.messages.send(
        user_id=event.user_id,
        message=text,
        keyboard=open(keyboard, "r", encoding="UTF-8").read(),
        random_id=random_id()
    )


while True:
    message_for_admin.clear()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            message = event.text.lower()

            # получение имени пользователя
            user = vk.users.get(user_id=event.user_id)
            user_name = user[0]['first_name']

            if message == "начать":
                answer_message(f"Привет, {user_name}!")
                answer_message('Если ты здесь, это значит \n'
                               'что ты хочешь оставить заявку \n'
                               'на создание чего-то крутого')
                upload_picture('python.png')

                # замена клавиатуры на "Сайт" и "Бот"
                change_keyboard('Выбери что тебе надо: ', 'keyboard_2.json')

            elif message == "начать сначала":
                change_keyboard(')', 'keyboard_0.json')

            elif message == 'сайт':
                message_for_admin.append(f'Пользователь хочет: {message}')

                change_keyboard('Хоршо, если это оканчательное решение то,\n'
                                'отправь заявку, если нет, то начни\n'
                                'сначала', 'keyboard_1.json')

            elif message == 'бот':
                message_for_admin.append(f'Пользователь хочет: {message}')

                change_keyboard('Хоршо, если это оканчательное решение то,\n'
                                'отправь заявку, если нет, то начни\n'
                                'сначала', 'keyboard_1.json')

            elif message == "отправить заявку":
                answer_message("Спасибо, заявка отправлена)")

                # получение полного имени пользователя
                full_user_name = user[0]['first_name'] + ' ' + user[0]['last_name']

                # добавление id пользователя в сообщение админа
                message_for_admin.append(f'{full_user_name}: https://vk.com/id{event.user_id}')

                # распаковка списка
                hah, sc = message_for_admin

                vk.messages.send(
                    user_id=244445323,
                    message=('Новая заявка!!!\n' + hah + '\n' + sc),
                    random_id=random_id()
                )
                message_for_admin.clear()
                hah, sc = '', ''
                print(hah, sc)

            else:
                answer_message("Нераспознанная команда!")
