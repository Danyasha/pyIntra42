import requests
import json
from time import sleep
import Intra42
configfd = open("config.json")
config = json.loads(configfd.read())
UID = config.get("UID")
SECRET = config.get("SECRET")
configfd.close()
def main():
    IntraPy = Intra42.Intra42(UID, SECRET)
    raiting = []
    for i in range(0, IntraPy.cursus_users(getPage='last') + 1):
    #for i in range(0, 2):
        users = IntraPy.cursus_users(page=str(i))
        k = 0
        print(i)
        for user in users:
            raiting.append({'login':users[k].get('user').get('login'), 'lvl':users[k].get('level')})
            k += 1
    fd = open("loginsAndLvls.json", "w")
    raiting = IntraPy.sortUsersByRaiting(raiting)
    json.dump(raiting, fd, ensure_ascii=False, sort_keys=True, indent=4)
    fd.close()

if __name__ == "__main__":
    main()