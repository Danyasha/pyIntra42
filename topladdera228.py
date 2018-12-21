import vk_api
import time
import json
from vk_api.longpoll import VkLongPoll, VkEventType
token = "token"
vk_session = vk_api.VkApi(login=None, password=None, token=token)
vk = vk_session.get_api()

def getUsers():
    fd = open("moscow.json", 'r')
    users = json.load(fd)
    fd.close()
    return(users)
def findLogin(login, users):
    k = 0
    for i in users:
        if i.get('login') == login:
            return("Ты %s в общем рейтинге с %s уровнем"%(str(k), str(round(i.get('lvl'), 2))))
        k+=1
    return("Я тебя не нашел. Проверь правильность написания логина")
longpoll = VkLongPoll(vk_session)
users = getUsers()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.from_chat and "!рейтинг" in event.text.split()[0].lower():
        try:
            login = event.text.split()[1]
            vk.messages.send(peer_id=2000000000 + event.chat_id, message=findLogin(login, users), random_id = "0")
        except IndexError:
            print("6 утра, мне было лень")

