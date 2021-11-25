import re

import requests
import json


def paperdetails(keyword):
    listofpaperdetails = []
    response = requests.get("https://dblp.org/search/publ/api?q=" + keyword + "&h=1000&format=json")
    response = response.json()
    temp = response['result']['hits']['hit']
    for item in temp:
        info = item['info']
        if (info['type'] == "Conference and Workshop Papers"):
            listofpaperdetails.append(info)

    return listofpaperdetails


if __name__ == "__main__":
    key = input("enter keyword")
    item_list = paperdetails(key)
    print(item_list)
