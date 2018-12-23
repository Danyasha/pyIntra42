import vk_api
import time
import json
from vk_api.longpoll import VkLongPoll, VkEventType

tokenfd = open("config.json")
config = json.loads(tokenfd.read())
token = config.get("tokenVK")
tokenfd.close()
vk_session = vk_api.VkApi(login=None, password=None, token=token)
vk = vk_session.get_api()

def getBeforeAfter(raiting):
    k = 0
    for i in raiting:
        k += len(i.get("users"))
    before = 0
    after = k
    for i in range(0, len(raiting)):
        usersHere = len(raiting[i].get("users"))
        raiting[i].update({"before":before, "after":after - usersHere})
        before += len(raiting[i].get("users"))
        after = after - usersHere
    return(raiting)

def getUsers():
    fd = open("moscow.json", 'r')
    users = json.load(fd)
    fd.close()
    return(users)
def findLogin(login, users):
    k = 0
    for i in users:
        if login in i.get("users"):
            howMuchUsers = "\nделит место с %s людьми"%str(len(i.get("users")))
            answer = "%s:\n%s в общем рейтинге с %s уровнем,"%(login, str(k), str(round(i.get("lvl"), 2))) + howMuchUsers
            answer += "\nПеред: %s\nПосле: %s"%(str(i.get("before")), str(i.get("after")))
            return(answer)
        k+=1
    return("Проверь правильность написания логина")
longpoll = VkLongPoll(vk_session)
users = getUsers()
users = getBeforeAfter(users)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.from_chat and event.text and "!рейтинг" in event.text.split()[0].lower():
        try:
            login = event.text.split()[1].lower()
            if login != "vice-wra":
                vk.messages.send(peer_id=2000000000 + event.chat_id, message=findLogin(login, users), random_id = "0")
            else:
                vk.messages.send(peer_id=2000000000 + event.chat_id, message="undefined. Kicked for harassment", random_id = "0")
        except IndexError:
            print("6 утра, мне было лень")

