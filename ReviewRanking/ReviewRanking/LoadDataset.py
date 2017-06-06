import os
import glob
import json
from textblob import TextBlob
'''
A list of dictionaries, ReviewList is created, which contains
the following information regarding each review of a hotel.
 1.The id of the reviewer
 2.The content of the review
 3.The date on which the review was written
 4.The number of prior readers of the review
 5.The number of users who found the review to be helpful
 6. The overall rating of the review
 7. The rating of certain common themes expected in each hotel review
'''




'''
This is a function that parses the JSON files and creates python dictionaries which can be used to perform various operations.
The batchsize variable indicates the number of files from which the review data is to be extracted
'''

def LoadTrainingData(batchSize):
    ct=0
    ReviewsList=[]
    files=glob.glob(os.path.dirname(os.path.abspath(__file__))+'\\cleanedData\\trainingData\\*.json')
    for file in files:
        if(batchSize>ct):
            with open(file, encoding='utf-8') as data_file:
                ct+=1
                data = json.load(data_file)
                ReviewsList+=data
        data_file.close()
    return ReviewsList

def LoadTestData(batchSize):
    ct=0
    ReviewsList = []
    files = glob.glob(os.path.dirname(os.path.abspath(__file__)) + '\\cleanedData\\testData\\*.json')
    for file in files:
        if (batchSize > ct):
            with open(file, encoding='utf-8') as data_file:
                ct += 1
                data = json.load(data_file)
                ReviewsList += data
        data_file.close()
    return ReviewsList

def calculateTopicsCovered(dict):
    topicsCovered=7
    if(dict['BusinessServiceRating']==0):
        topicsCovered-=1
    if (dict['LocationRating'] == 0):
        topicsCovered -= 1
    if (dict['OverallRating'] == 0):
        topicsCovered -= 1
    if (dict['ValueRating'] == 0):
        topicsCovered -= 1
    if (dict['CleanlinessRating'] == 0):
        topicsCovered -= 1
    if (dict['RoomsRating'] == 0):
        topicsCovered -= 1
    if (dict['ReceptionRating'] == 0):
        topicsCovered -= 1
    return topicsCovered
        

def AddComputedFeatures(ReviewList):
    for index in range(0,len(ReviewList)):
        ReviewList[index]['Length']=len(ReviewList[index]['Content'])
        ReviewList[index]['Subjectivity']=TextBlob(ReviewList[index]['Content']).sentiment.subjectivity
        ReviewList[index]['topicsCovered']=calculateTopicsCovered(ReviewList[index])


def findExtremeties(ReviewList):
    AddComputedFeatures(ReviewList)
    
    maxOverallRating = ReviewList[0]['OverallRating']
    maxReader = ReviewList[0]['Reader']
    maxHelpfullness = ReviewList[0]['Helpfullness']
    maxLength=ReviewList[0]['Length']
    maxSubjectivity=ReviewList[0]['Subjectivity']
    maxTopicsCovered=ReviewList[0]['topicsCovered']

    minOverallRating = ReviewList[0]['OverallRating']
    minReader = ReviewList[0]['Reader']
    minHelpfullness = ReviewList[0]['Helpfullness']
    minLength = ReviewList[0]['Length']
    minSubjectivity = ReviewList[0]['Subjectivity']
    minTopicsCovered = ReviewList[0]['topicsCovered']
    
    for index in range(0,len(ReviewList)):
        if (ReviewList[index]['OverallRating'] > maxOverallRating):
            maxOverallRating = ReviewList[index]['OverallRating']
        if(ReviewList[index]['Reader']>maxReader):
            maxReader=ReviewList[index]['Reader']
        if(ReviewList[index]['Helpfullness']>maxHelpfullness):
            maxHelpfullness=ReviewList[index]['Helpfullness']
        if (ReviewList[index]['Length'] > maxLength):
            maxLength = ReviewList[index]['Length']
        if (ReviewList[index]['Subjectivity'] > maxSubjectivity):
            maxSubjectivity = ReviewList[index]['Subjectivity']
        if (ReviewList[index]['topicsCovered'] > maxTopicsCovered):
            maxTopicsCovered = ReviewList[index]['topicsCovered']
            
        if (ReviewList[index]['OverallRating'] < minOverallRating):
            minOverallRating = ReviewList[index]['OverallRating']
        if (ReviewList[index]['Reader'] < minReader):
            minReader = ReviewList[index]['Reader']
        if (ReviewList[index]['Helpfullness'] < minHelpfullness):
            minHelpfullness = ReviewList[index]['Helpfullness']
        if (ReviewList[index]['Length'] < minLength):
            minLength = ReviewList[index]['Length']
        if (ReviewList[index]['Subjectivity'] < minSubjectivity):
            minSubjectivity = ReviewList[index]['Subjectivity']
        if (ReviewList[index]['topicsCovered'] < minTopicsCovered):
            minTopicsCovered = ReviewList[index]['topicsCovered']

    return maxHelpfullness,minHelpfullness,maxOverallRating,minOverallRating,maxReader,minReader,maxLength,minLength,maxSubjectivity,minSubjectivity,maxTopicsCovered,minTopicsCovered

def normalizingFeatures(ReviewList):
    normalizedFeatureList=[]
    maxh,minh,maxO,minO,maxR,minR,maxL,minL,maxS,minS,maxT,minT=findExtremeties(ReviewList)
    for index in range(0,len(ReviewList)):
        normalizedDict={}
        normalizedDict['Helpfullness']=(ReviewList[index]['Helpfullness']-minh)/(maxh-minh)
        normalizedDict['OverallRating']=(ReviewList[index]['OverallRating']-minO)/(maxO-minO)
        normalizedDict['Reader']=(ReviewList[index]['Reader']-minR)/(maxR-minR)
        normalizedDict['Length']=(ReviewList[index]['Length']-minL)/(maxL-minL)
        normalizedDict['Subjectivity']=(ReviewList[index]['Subjectivity']-minS)/(maxS-minS)
        normalizedDict['topicsCovered']=(ReviewList[index]['topicsCovered']-minT)/(maxT-minT)
        normalizedFeatureList.append(normalizedDict)
    return normalizedFeatureList