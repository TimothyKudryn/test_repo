import json
import csv


# this function is used a couple of times throughout the code. It takes in a list, and a counter
# and depending on the data in the list returns the max. (look at comments by function calls in code)
def getMax(myDict, curMax):
    for key in myDict:
        (data1, data2) = myDict[key]
        averageComments = (data1 / data2)
        if curMax < averageComments:
            curMax = averageComments
            maxCommentChannel = key
    return maxCommentChannel, curMax


# this function scans through the file of youtube data, and returns the channel with the most
# trending videos
def getMostTrends():
    myDict = {}  # intialized new dictionary
    mostTrending = 0  # mostTrending for current most trending videos
    maxChannel = None
    # the csv file has the enconding : encoding="utf-8", so that is why I have the extra argument in mu open call
    f = open("trending.csv", "r", encoding="utf-8")
    reader = csv.DictReader(f)
    for row in reader:
        curChannel = row['channel_title']  # sets curChannel to what ever channel is on the current row
        if curChannel not in myDict and row['trending_date'] is not None:
            # if key isn't in the dictionary, code below initializes it and sets it to 1
            myDict[curChannel] = myDict.get(curChannel, 0) + 1
        else:
            myDict[curChannel] += 1  # increments the amount of videos at the given key by one.
        # checking if the current max commented channel has more comments then the next entry in the dictionary
        if mostTrending < int(myDict[curChannel]):
            mostTrending = int(myDict[curChannel])
            maxChannel = curChannel
    f.close()
    return maxChannel, mostTrending


# part 2
# This function parses the data and returns the name of the channel that has the most average comments on
# their trending videos
def getMostComments():
    myDict = {}
    counter = 0
    f = open("trending.csv", "r", encoding="utf-8")
    reader = csv.DictReader(f)
    for row in reader:
        curChannel = row['channel_title']
        curComments = int(row['comment_count'])
        if curChannel not in myDict and row['trending_date'] is not None:
            # if key isn't in the dictionary, code below initializes it and sets it to 0
            myDict[curChannel] = (0, 0)

        (comments, videos) = myDict[curChannel]  # take it out
        comments += curComments
        videos += 1
        myDict[curChannel] = (comments, videos)  # put it back in
    f.close()
    # getMax returns the name of the channel that has the most comments, and the amount of comments on the given page.
    (maxCommentChannel, counter) = getMax(myDict, counter)
    return maxCommentChannel, counter


# part 3 return the category that is the least contreversial.
# the category which has the best like to dislike ratio.
def getDislikeRatio():
    myDict = {}  # initiales new dictionary
    highAvCounter = 0
    f = open("category_id.json", "r")
    jsonfile = json.load(f)  # json file gets loaded in
    f.close()
    csvf = open("trending.csv", 'r')
    reader = csv.DictReader(csvf)  # csv file loaded into reader

    for row in reader:
        categoryID = row['category_id']
        for data in jsonfile['items']:
            if data['id'] == categoryID:  # matching the ID's
                category = data['snippet']['title']
                break
        curlikes = int(row['likes'])
        curdislikes = int(row['dislikes']) + 1
        if category not in myDict:
            myDict[category] = (0, 0)
        (averageRatio, vidCounter) = myDict[category]
        averageRatio += curlikes / (curdislikes + 1)
        vidCounter += 1
        myDict[category] = (averageRatio, vidCounter)
    # getMax returns a category from the Dictionary of categories that has the best like to dislike ratio along with
    # the ratio itself.
    (vidCategory, ratio) = getMax(myDict, highAvCounter)
    return vidCategory, ratio


(maxChannel, counter) = getMostTrends()
print(maxChannel, counter)  # most trending videos
(maxCommentChannel, comments) = getMostComments()
print(maxCommentChannel, comments)  # output the chanel with the most comments
(LDChannel, likeToDislike) = getDislikeRatio()
print(LDChannel, likeToDislike)  # print out the channel with the best like to dislike ratio
# currChannel = Bonus()
# print(currChannel)
