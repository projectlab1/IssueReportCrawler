



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Welcome to Web scrapping')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import urllib.parse
import csv
from datetime import datetime
import re

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.implicitly_wait(200)

#any issue report can be passed by updating the report id
issueId='10597'
driver.get('https://issues.apache.org/jira/browse/CAMEL-'+issueId)

time.sleep(4)

page_source = driver.page_source
driver.close()


f = open('Data/reports.csv', 'w', newline='',encoding='utf-8')
writer = csv.writer(f)
writer.writerow(['Type','Status','Priority','Resolution','Component','Assignee','Reporter','Create Date',
                 'Created Epoch','Description','GitLink','Comments'])

specificCategorySoup = BeautifulSoup(page_source,"html.parser")

#parsing the different report details
detailsContainer=specificCategorySoup.find('div',{'id':'details-module'})
type=detailsContainer.find('span',{'id':'type-val'}).getText().strip()
status=detailsContainer.find('span',{'id':'status-val'}).find('span').getText().strip()
priority=detailsContainer.find('span',{'id':'priority-val'}).getText().strip()
resolution=detailsContainer.find('span',{'id':'resolution-val'}).getText().strip()
component=detailsContainer.find('span',{'id':'components-field'}).getText().strip()

#parsing the assignee and reporter
peoplesContainer=specificCategorySoup.find('div',{'id':'peoplemodule'})
assignee=peoplesContainer.find('span',{'id':'assignee-val'}).getText().strip()
reporter=peoplesContainer.find('span',{'id':'reporter-val'}).getText().strip()

#parsing the create date
datesContainer=specificCategorySoup.find('div',{'id':'datesmodule'})
createdDate=datesContainer.find('span',{'data-name':'Created'}).find('time').getText()
createdEpochTime = datetime.strptime('14/Dec/16 14:42','%d/%b/%y %H:%M').timestamp()

#parsing the description
descriptionContainer=specificCategorySoup.find('div',{'id':'description-val'})
textList=descriptionContainer.findAll('p')
codeSectionList=descriptionContainer.findAll('div',{'class':'code panel'})
mergedText=''
for t in textList:
    mergedText=mergedText + ' . ' + t.getText().replace(',','')
mergedCode=''
for c in codeSectionList:
    processedCode=' '.join(c.getText().strip().split()).replace(',','')
    mergedCode = mergedCode + ' ' + processedCode
description=mergedText+'------'+mergedCode

#parsing the git pull link
gitPullLinkContainer=specificCategorySoup.find('div',{'id':'linkingmodule'})
link=gitPullLinkContainer.find('a')['href']

allComments=''
commentsContainer=specificCategorySoup.findAll('div',{'id':re.compile(r'comment-[0-9]+')})
print(len(commentsContainer))
for c in commentsContainer:
    commenterName=c.find('a',{'class':'user-hover user-avatar'}).getText()
    commentTime=c.find('span',{'class':'date user-tz'}).getText()
    commentContent=c.find('div',{'class':'action-body flooded'}).getText().replace('\n','')
    #Seperating commneter name, time and text using --- seperator for later spliting
    comment=commenterName+'---'+commentTime+'---'+commentContent
    # Seperating each comment using ----- seperator for later spliting, as each report will have varing number of comments
    allComments=allComments+'-----'+comment.replace(',','')
    print(comment)

#writing all in file
print(type+','+status+','+priority+','+resolution+','+component+','+assignee+','+reporter+','+createdDate+','+link+','+allComments)
writer.writerow([type,status,priority,resolution,component,assignee,reporter,createdDate,createdEpochTime
                 ,description,link,allComments])

# quit and close browser
f.close()
driver.quit()