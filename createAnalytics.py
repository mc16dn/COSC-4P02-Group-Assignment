import pandas as pd
import datetime
import random 
import csv 
import calendar
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
from analytix import Client

#Given a list of categories and the month as well as the range, it will generate a random list of dates for that month
#This code requires you to have a csv file prepped beforehand and the method will be called with its name
def createTestAnalyticsM(year, month, categories, min, max, fileName):
    mRange = calendar.monthrange(year, month)[1] #stores the number of days in the month into mRange
    
    with open ('./Outputs/'+fileName, 'w',newline='') as fileObj: #opens the csv file
        writer = csv.writer(fileObj) #creates csv writer
        writer.writerow(categories) #creates rows
        
       
        for i in range(mRange):
            rangeNumbers = random.sample(range(min,max), len(categories)-1) #creates a randomvalue for each category 
            currDate = datetime.date(year,month,i+1)
            rangeNumbers.insert(0,currDate)
            writer.writerow (rangeNumbers) #appends the number of values

def createTestAnalyticsY(year, categories, min, max, fileName):
    with open ('./Outputs/'+fileName, 'w',newline='') as fileObj: #opens the csv file
        writer = csv.writer(fileObj) #creates csv writer
        writer.writerow(categories) #creates rows
        
        for x in range(1,12):
            mRange = calendar.monthrange(year, x)[1] #stores the number of days in the month into mRange
            rangeNumbers = [0]*(len(categories)-1) #will create a list of 0s for the number of categories minus the date
            for i in range(mRange):
                for y in range(0,len(categories)-1):
                    rangeNumbers[y] += random.randint(min,max) #creates a randomvalue for each category 
            currDate = str(year) + '-' + str(x) #year-month
            rangeNumbers.insert(0,currDate)
            writer.writerow (rangeNumbers) #appends the number of values


#This will pull out all of your youtube channels analytics sorted by days
def ytAnalytics():
    client = Client ("secrets.json")
    report = client.fetch_report(dimensions=("day",),)
    report.to_csv("./Outputs/output.csv", overwrite=True)


def ytAnalyticsDate (startDate, endDate):
    name = (str(startDate) +"_" + str(endDate))
    client = Client("secrets.json")
    
    report = client.fetch_report(
    dimensions=("day",),
    start_date= startDate,
        end_date=endDate,
    )
    report.to_csv('./Outputs/'+name + ".csv", overwrite=True)

def generateYTAnalytics(startingYear, startingMonth, endingMonth,categories):
    min = 30 #This is to emulate a steady growth in a youtube channel, this will not be used when you pull from your own analytics so it should be removed
    max = 200
    currMonth = startingMonth
    currYear = startingYear
    if (os.path.isfile('secrets.json')):
        while (currMonth != endingMonth): #This loop will replaced with ytAnalyticsDate(startingdate,enddate) for a working yt channel
            if (currMonth > 12):
                currMonth = 1
                currYear +=1
            startingdate = datetime.date(currYear,currMonth,1) #beginning of the month
            numofdays = calendar.monthrange(currYear,currMonth)[1] #number of days in the month
            endingdate = datetime.date (currYear,currMonth,numofdays) #end of the month
            ytAnalyticsDate(startingdate,endingdate)
            currMonth+=1
    else:
        while (currMonth != endingMonth): #This loop will replaced with ytAnalyticsDate(startingdate,enddate) for a working yt channel
            if (currMonth > 12):
                currMonth = 1
                currYear +=1
            fileName = str(currYear) + '_' + str(currMonth)
            createTestAnalyticsM(currYear,currMonth,categories,min,max,fileName)  #Creates a csv file with all the data for each month in the file.
            currMonth+=1

 


