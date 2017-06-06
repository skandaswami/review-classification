
import plotly.plotly as py
import plotly.graph_objs as go
from textblob import TextBlob
from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
import LoadDataset
import numpy



'''
To make the training set, we use the reviews that have already received plenty of
votes for being very helpful. Since other humans are the ones rating whether or not a particular review
is helpful, we can assume that reviews which carry a high number of helpfullness ratings are probably
the most useful reviews.So we determine the reviews with the highest helpfullness rating, and use these
reviews to train our classifier.
'''


def reviewsVsReaders():
  ReviewList=LoadDataset.LoadTrainingData(40)
  ctReaders=0
  ctReviews=0
  for index in range(0,len(ReviewList)):
    ctReviews+=1
    if(ReviewList[index]['Reader']>0):
        ctReaders+=1
  print('The number of reviews are:'+str(ctReviews))
  print('The number of reviews which have been read atleast once are:' + str(ctReaders))

def buildClassifier():
    ReviewList = LoadDataset.LoadTrainingData(160)
    TestData=LoadDataset.LoadTestData(20)

    normalizedTestList=LoadDataset.normalizingFeatures(TestData)
    '''
    Each Review is classified as either being helpful or not helpful
    '''
    LabelSet=[]
    for index in range(0,len(ReviewList)):
        if ReviewList[index]['Helpfullness'] > 0:
            LabelSet.append(1)
        else:
            LabelSet.append(0)
    #print(len(LabelSet))

    normalizedFeatureList=LoadDataset.normalizingFeatures(ReviewList)
    biglist = []
    biglist2 = []
    for index in range(0,len(normalizedFeatureList)):
        item1 = normalizedFeatureList[index]['Helpfullness']
        item2 = normalizedFeatureList[index]['topicsCovered']
        item3 = normalizedFeatureList[index]['Length']
        item4 = normalizedFeatureList[index]['Subjectivity']
        item5 = normalizedFeatureList[index]['OverallRating']
        minilist=[item1,item2,item3,item4,item5]
        biglist.append(minilist)
    for index in range(0, len(normalizedTestList)):
        item1 = normalizedTestList[index]['Helpfullness']
        item2 = normalizedTestList[index]['topicsCovered']
        item3 = normalizedTestList[index]['Length']
        item4 = normalizedTestList[index]['Subjectivity']
        item5 = normalizedTestList[index]['OverallRating']
        minilist = [item1, item2, item3, item4, item5]
        biglist2.append(minilist)
    pest=[]
    for index in range(0, len(TestData)):
        if TestData[index]['Helpfullness']==0:
            pest.append(0)
        else:
            pest.append(1)

    svmClassifier = svm.SVC()
    svmClassifier.fit(biglist,LabelSet)
    final1=svmClassifier.score(biglist2,pest)

    print('Score:'+str(final1))

buildClassifier()


def newChart():
    ReviewList = LoadDataset.LoadTrainingData(20)
    xcoord = [1,2,3,4,5,6,7]
    ycoord = [0,0,0,0,0,0,0]
    for index in range(0, len(ReviewList)):
        ycoord[LoadDataset.calculateTopicsCovered(ReviewList[index])-1]+=ReviewList[index]['Helpfullness']

    data = [
        go.Bar(
            x=xcoord,
            y=ycoord
        )
    ]
    plot_url = py.plot(data, filename='basic-bar')


