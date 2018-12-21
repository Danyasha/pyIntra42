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
        formattedUsers.append("top " +str(k) + ": https://profile.intra.42.fr/users/" + users[k].get('login') + " lvl = " + str(round(users[k].get('lvl'), 2))  + "\n")
    for i in formattedUsers:
        print(i)
if __name__ == "__main__":
    main()