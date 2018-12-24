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

def getUsers():
    fd = open("moscow.json", 'r')
    users = json.load(fd)
    fd.close()
    return(users)
def findLogin(login, users):
    k = 0
    for i in users:
        if login in i.get("users"):
            howMuchUsers = "\nделит место с %s людьми"%str(len(i.get("users")) - 1)
            answer = "%s:\n%s в общем рейтинге с %s уровнем,"%(login, str(k), str(round(i.get("lvl"), 2))) + howMuchUsers
            answer += "\nПеред: %s\nПосле: %s"%(str(i.get("before")), str(i.get("after")))
            return(answer)
        k+=1
    return("Проверь правильность написания логина")
def getTop(users):
    users = users[0:15]
    formattedUsers = []
    temp = ""
    for k in range(0, len(users)):
        placeGuys = ""
        for i in users[k].get('users'):
            placeGuys += "https://profile.intra.42.fr/users/" + i + "\n"
        formattedUsers.append("top-%s c lvl - %s:\n%s" %(str(k + 1) , str(round(users[k].get('lvl'), 2)), placeGuys))
    temp = temp.join(formattedUsers)
    return (temp)
longpoll = VkLongPoll(vk_session)
users = getUsers()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.text and event.text.split()[0].lower() == "!рейтинг":
        if event.from_chat:
            try:
                login = event.text.split()[1].lower()
                if login != "vice-wra":
                    vk.messages.send(peer_id=2000000000 + event.chat_id, message=findLogin(login, users), random_id = "0")
                else:
                    vk.messages.send(peer_id=2000000000 + event.chat_id, message="undefined. Kicked for harassment", random_id = "0")
            except IndexError:
                print("6 утра, мне было лень")
        elif event.to_me:
            if (len(event.text.split()) >= 2):
                login = event.text.split()[1].lower()
                vk.messages.send(user_id = event.user_id, message=findLogin(login, users), random_id = "0")
            else:
                vk.messages.send(user_id = event.user_id, message=getTop(users), random_id = "0")


