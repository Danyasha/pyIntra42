import requests
import json
class Intra42:
    def __init__(self, id, secret):
        self.URL = "https://api.intra.42.fr/"
        TOKEN_URL = self.URL + "oauth/token"
        data = {"grant_type":"client_credentials",
            "client_id":id,"client_secret":secret}
        response = requests.post(TOKEN_URL, data=data)
        self.token = response.json().get('access_token') 
        self.header = {'Authorization':"Bearer " + response.json().get('access_token')}
    def getNumberOfLastPage(self, methodURL, headers = None):
        data = requests.get(methodURL, headers=self.header)
        lastPage = data.headers.get('Link')
        lastPage = lastPage.split("page=")[1].split(">;")[0] #its ridiculous
        return(int(lastPage))
    def getData(self, methodURL, headers = None):
        if not headers:
            data = requests.get(methodURL, headers=self.header)
            return(data.json())
        else:
            return(requests.get(methodURL, headers=self.header).json())
    def cursus(self, sort=None, filter=None, range=None, page=None, pageNumber=None, getPage = None):
        endpoint = self.URL + "v2/cursus"
        sortedBy = ["id", "name", "created_at", "updated_at", "slug", "kind", "restricted", "is_subscriptable"]
        if page:
            endpoint += "?page=" + page
        if sort:
            sort = sort.split(',')
            endpoint += "&sort="
            for i in range(len(sort)):
                if sort[i] in sortedBy:
                    endpoint += sort[i]
                    if i < len(sort) - 1:
                        endpoint += ','
        data = self.getData(endpoint)
        return (data)
    def cursus_users(self, page=None, cursus_id="1", getPage = None, pageSize = 100, filterBy = None,filterVal = None):
        endpoint = self.URL + "v2/cursus_users"+"?cursus_id=" + cursus_id
        if filter and filterVal:
            endpoint += "&filter[%s]=%s"%(filterBy,filterVal)
        if pageSize:
            endpoint += "&page[size]="+str(pageSize)
        if getPage and getPage == "last":
            return(self.getNumberOfLastPage(endpoint))
        if page:
            endpoint += "&page[number]=" + page
        data = self.getData(endpoint)
        return(data)
    def campus(self):
        endpoint = self.URL + "/v2/campus"
        data = self.getData(endpoint)
        return(data)
    def campus_users(self, filterBy = "campus_id", filterVal = "17"):
        endpoint = self.URL + "/v2/campus_users"
        if filter and filterVal:
            endpoint += "?filter[%s]=%s"%(filterBy,filterVal)
        data = self.getData(endpoint)
        return(data)

    def sortUsersByRaiting(self, raiting, addBeforeAfter = False):
        raiting = sorted(raiting, key=lambda x: -x['lvl'])
        k = 0
        sortedRaiting = [{"users":[raiting[0].get("login")],"lvl":raiting[0].get("lvl")}]
        for i in raiting:
            if i.get("lvl") == sortedRaiting[k].get("lvl") and i.get("login") not in sortedRaiting[k].get("users"):
                    sortedRaiting[k].get("users").append(i.get("login"))
            elif i.get("login") not in sortedRaiting[k].get("users"):
                k += 1
                sortedRaiting.append({"users":[i.get("login")],"lvl":i.get("lvl")})
        if (addBeforeAfter):
            return(self.getBeforeAfter(sortedRaiting))
        return(sortedRaiting)
    def getBeforeAfter(self, raiting):
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