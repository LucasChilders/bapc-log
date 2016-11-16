import os
import praw
import csv
import datetime
import re

LOG_DIR = "Desktop/bapc-log/log.csv"
SUB_REDDIT = "buildapcsales"
CATA = ["case", "cooler", "fan", "hdd", "keyboard", 
        "mouse", "ram", "mobo", "controller", "cpu", 
        "gpu", "headphones", "monitor", "psu", "ssd", 
        "laptop"]
#PUSH_LOC = "./Desktop/bapc-log/push.sh"

def getPost(sub):
    reddit = praw.Reddit(user_agent = "/u/LucasChilders")
    post = reddit.get_subreddit(sub).get_new(limit = 1)
    post = list(post)
    return post[0]

def getDate(post):
    time = post.created
    return datetime.datetime.fromtimestamp(time)

def checkFile(post):
    with open(LOG_DIR, 'rt', encoding='iso-8859-1') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if post.id == row[0]:
                f.close()
                return True
    f.close()

#def updateGit():
#	os.system(PUSH_LOC)

def isValidCatagory(catagory):
    if catagory.lower() in CATA:
        return True
    else:
        return False

def writeFile(post):
    if checkFile(post):
        print("Duplicate post found, returning.")
        return

    logFile = open(LOG_DIR, "a", newline="", encoding='iso-8859-1')
    writer = csv.writer(logFile, delimiter = ',')

    title = post.title
    title = title.replace(",", "|")

    try:
        catagory = title.split("]")[0]
        catagory = catagory.split("[")[1]
        
        if isValidCatagory(catagory) == False:
            logFile.close();
            print("Catagory not allowed, returning.")
            return
        
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

    url = post.permalink
    url = url.replace(",", "|")

    postId = post.id

    data = postId + "," + catagory + "," + title + "," + price + "," + str(getDate(post)) + "," + url
    data = data.split(",")

    writer.writerow(data)
    logFile.close()
    #updateGit()

writeFile(getPost(SUB_REDDIT))
