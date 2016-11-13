import os
import praw
import csv
import datetime
import re

def getPost(sub):
    reddit = praw.Reddit(user_agent = "/u/LucasChilders")
    post = reddit.get_subreddit(sub).get_new(limit = 1)
    post = list(post)
    return post[0]

def getDate(post):
    time = post.created
    return datetime.datetime.fromtimestamp(time)

def writeFile(post):
    logFile = open("log.csv", "a", newline="")
    writer = csv.writer(logFile, delimiter = ',')

    title = post.title
    title = title.replace(",", "|")

    try:
        catagory = title.split("]")[0]
        catagory = catagory.split("[")[1]
        title = title.split("]")[1]
        title = title.strip()
    except:
        logFile.close()
        print("Catagory not found, returning.")
        return

    if catagory.lower() == "meta":
        logFile.close()
        print("META post found, returning.")
        return

    try:
        price = title.split("$")[1]
        price = price.split(" ")[0]
        price = re.findall(r'\d+', price)[0]
    except:
        price = ""
        print("Cannot find price, blank inserted.")

    url = post.url
    url = url.replace(",", "|")

    data = catagory + "," + title + "," + price + "," + str(getDate(post)) + "," + url
    data = data.split(",")

    writer.writerow(data)
    logFile.close()


post = getPost("buildapcsales")
writeFile(post)
