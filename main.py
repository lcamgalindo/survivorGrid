from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import sensitive
import pandas as pd

# Start of week
week = 2

# URL template
url = 'https://www.rotowire.com/betting/nfl/odds/week-'

def downloadData(url):
    for ii in range(week,5):
        # build url
        newUrl = url+str(ii)
        
        # Start up selenium
        driver = webdriver.Chrome()
        driver.get(newUrl)
        time.sleep(2)

        # Download data
        parentBtn = driver.find_element(By.CLASS_NAME, 'export-buttons')
        childBtns = parentBtn.find_elements(By.TAG_NAME,'button')

        for button in childBtns:
            if button.get_attribute('class') == 'export-button is-csv':
                button.click()
                time.sleep(2)

        driver.quit()

def moveFiles(week):
    filePattern = 'nfl-odds-rotowire'
    matchingFiles = []

    for filename in os.listdir(sourceDir):
        if filePattern in filename and filename.endswith('.csv'):
            oldFile = sourceDir+filename
            newFile = newDir+str(week)+'/'+filename
            # Move the source file to the destination
            os.rename(oldFile, newFile)


def winPer(x):
    if x>=0:
        y = 100/(100+x)
    else:
        y = x/(x-100)
    return round(y*100,2)


def makePrediction(week):
    fn = 'Week_'+str(week)+'/nfl-odds-rotowire.csv'
    data = pd.read_csv(fn,skiprows=[0])
    # Add win % column
    data['winPer'] = data['Moneyline'].apply(winPer)
    # Sort and print the top five
    data.sort_values(by='winPer',inplace=True,ascending=False)
    print('\n######## This weeks top teams ########\n' )
    print(data[['Team','Moneyline','winPer']].head().to_string(index=False))
    # Grab name of top five teams
    topTeams = data['Team'].iloc[0:5].tolist()
    return data,topTeams

def futureValue(teams):
    data = pd.read_csv('futureValueData.csv')
    # Grab data for teams
    for team in teams:
        seasonData = data[data['Team'].apply(lambda x: team in x)]
        print('\n################ '+team+' ################\n')
        print(seasonData.to_string(index=False))
    

# downloadData(url)

# moveFiles(week)

_,topTeams = makePrediction(week)

futureValue(topTeams)

#futureValue(['Cardinals'])






