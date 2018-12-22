
import json
from sys import argv
def main():
    fd = open(argv[1], 'r')
    users = json.load(fd)
    fd.close()
    users = sorted(users, key=lambda x: -x['lvl'])
    fd = open(argv[1], 'w')
    json.dump(users, fd, ensure_ascii=False, sort_keys=True, indent=4)
    fd.close()
    users = users[0:15]
    formattedUsers = []
    for k in range(0, len(users)):
        placeGuys = ""
        for i in users[k].get('users'):
            placeGuys += "https://profile.intra.42.fr/users/" + i + "\n"
        placeGuys = placeGuys[0:-1]
        formattedUsers.append("top-%s c lvl - %s:\n%s" %(str(k), str(round(users[k].get('lvl'), 2)), placeGuys))
    for i in formattedUsers:
        print(i)
if __name__ == "__main__":
    main()