import requests
import json
from time import sleep
import Intra42

UID = ""
SECRET = ""
def getCampuses():
    fd = open('a.json', 'w')
    temp = IntraPy.campus()
    json.dump(temp,fd, ensure_ascii=False, sort_keys=True, indent=4)
    fd.close()
def main():
    IntraPy = Intra42.Intra42(UID, SECRET)
    raiting = []
    LastPage = IntraPy.cursus_users(getPage='last',filterBy = "campus_id", filterVal = "17")
    for i in range(0, LastPage + 1):
        users = IntraPy.cursus_users(page=str(i), filterBy = "campus_id", filterVal = "17")
        k = 0
        print(i)
        for user in users:
            raiting.append({'login':users[k].get('user').get('login'), 'lvl':users[k].get('level')})
            k += 1
    fd = open("moscow.json", "w")
    raiting = sorted(users, key=lambda x: -x['lvl'])
    json.dump(raiting, fd, ensure_ascii=False, sort_keys=True, indent=4)
    fd.close()
if __name__ == "__main__":
    main()