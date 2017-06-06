import os
import glob
import json

'''
This is a python script to clean the noisy review data and to parse and create output
in JSON format which can easily be loaded in order to train and test th classifiers.
'''
global ct
ct=1

'''
This function identifies the key components from the dataset and loads it onto a list of dictionaries.
'''
def cleanReviewDataSet():
    mainReviewDirectory = os.path.dirname(os.path.abspath(__file__)) + '\\ReviewData'+'\\testData'
    files = glob.glob(mainReviewDirectory + '\\*.dat')
    for file in files:
        '''Lists to hold the data extracted from the review corpus'''
        AuthorList = []
        ContentList = []
        DateList = []
        ReaderList = []
        HelpfullnessList = []
        OverallRatingList = []
        RoomsRatingList = []
        ValueRatingList = []
        LocationRatingList = []
        CleanlinessRatingList = []
        ReceptionRatingList = []
        ServiceRatingList = []
        BusinessServiceRatingList = []
        reviewFile=open(file,'r',encoding='utf-8')
        '''
            This function returns the number of themes covered in a given review
            The themes extracted include:
            i.The value for money proposition
            ii.The quality of the rooms in the hotel.
            iii.The location of the hotel.
            iv. The cleanliness and hygiene.
            v.The Service provided by the hotel.
            vi.The competence of officials at the front desk.
        '''
        for line in reviewFile:
            if '<Author>' in line:
                AuthorList.append(line[line.index('>')+1:len(line)-1])
            elif '<Content>' in line:
                ContentList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<Date>' in line:
                DateList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<No. Reader>' in line:
                ReaderList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<No. Helpful>' in line:
                HelpfullnessList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<Overall>' in line:
                OverallRatingList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<Value>' in line:
                ValueRatingList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<Rooms>' in line:
                RoomsRatingList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<Location>' in line:
                LocationRatingList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<Cleanliness>' in line:
                CleanlinessRatingList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<Check in / front desk>' in line:
                ReceptionRatingList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<Service>' in line:
                ServiceRatingList.append(line[line.index('>') + 1:len(line) - 1])
            elif '<Business service>' in line:
                BusinessServiceRatingList.append(line[line.index('>') + 1:len(line) - 1])
        reviewFile.close()
        createReviewsList(AuthorList,ContentList, DateList, ReaderList ,HelpfullnessList, OverallRatingList,  RoomsRatingList, ValueRatingList ,LocationRatingList ,CleanlinessRatingList ,ReceptionRatingList, ServiceRatingList, BusinessServiceRatingList)

'''
This function creates the list of dictionaries.
'''
def createReviewsList(AuthorList,ContentList, DateList, ReaderList ,HelpfullnessList, OverallRatingList,  RoomsRatingList, ValueRatingList ,LocationRatingList ,CleanlinessRatingList ,ReceptionRatingList, ServiceRatingList, BusinessServiceRatingList):
    ReviewsList = []
    for index in range(0,len(AuthorList)):
        Review = {}
        Review['Author']=AuthorList[index]
        Review['Content'] = ContentList[index]
        Review['Date'] = DateList[index]
        if int(ReaderList[index]) == -1:
            Review['Reader'] = 0
        else:
            Review['Reader'] = int(ReaderList[index])
        if int(HelpfullnessList[index])==-1:
            Review['Helpfullness'] =0
        else:
            Review['Helpfullness'] = int(HelpfullnessList[index])
        if int(OverallRatingList[index]) == -1:
            Review['OverallRating'] = 0
        else:
            Review['OverallRating'] = int(OverallRatingList[index])
        if int(ValueRatingList[index]) == -1:
            Review['ValueRating'] =0
        else:
            Review['ValueRating'] = int(ValueRatingList[index])
        if int(RoomsRatingList[index]) == -1:
            Review['RoomsRating'] = 0
        else:
            Review['RoomsRating'] = int(RoomsRatingList[index])
        if int(LocationRatingList[index]) == -1:
            Review['LocationRating'] = 0
        else:
            Review['LocationRating'] = int(LocationRatingList[index])
        if int(CleanlinessRatingList[index]) == -1:
            Review['CleanlinessRating'] = 0
        else:
            Review['CleanlinessRating'] = int(CleanlinessRatingList[index])
        if int(ReceptionRatingList[index]) == -1:
            Review['ReceptionRating'] = 0
        else:
            Review['ReceptionRating'] = int(ReceptionRatingList[index])
        if int(ServiceRatingList[index]) == -1:
            Review['ServiceRating'] = 0
        else:
            Review['ServiceRating'] = int(ServiceRatingList[index])
        if int(BusinessServiceRatingList[index]) == -1:
            Review['BusinessServiceRating'] = 0
        else:
            Review['BusinessServiceRating'] = int(BusinessServiceRatingList[index])
        ReviewsList.append(Review)
    makeJSON(ReviewsList)

'''
This function is responsible for parsing the list and creating JSON output
'''
def makeJSON(list):
    global ct
    with open('cleanedData\\testData'+str(ct)+'.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(list, outfile, ensure_ascii=False))
    ct+=1
    outfile.close()


cleanReviewDataSet()

