
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import urllib.parse
import csv
import datetime

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.implicitly_wait(200)

#driver.get('https://marketplace.atlassian.com/')
driver.get('https://issues.apache.org/jira/browse/CAMEL-10597')

time.sleep(4)

page_source = driver.page_source
driver.close()


f = open('Data/reports.csv', 'w', newline='',encoding='utf-8')
writer = csv.writer(f)
writer.writerow(['Type','Status','Priority','Resolution','Component','Assignee'])


specificCategorySoup = BeautifulSoup(page_source,"html.parser")

detailsContainer=specificCategorySoup.find('div',{'id':'details-module'})
type=detailsContainer.find('span',{'id':'type-val'}).getText().strip()
status=detailsContainer.find('span',{'id':'status-val'}).find('span').getText().strip()
priority=detailsContainer.find('span',{'id':'priority-val'}).getText().strip()
resolution=detailsContainer.find('span',{'id':'resolution-val'}).getText().strip()
component=detailsContainer.find('span',{'id':'components-field'}).getText().strip()

peoplesContainer=specificCategorySoup.find('div',{'id':'peoplemodule'})
assignee=peoplesContainer.find('span',{'id':'assignee-val'}).getText().strip()
reporter=peoplesContainer.find('span',{'id':'reporter-val'}).getText().strip()

datesContainer=specificCategorySoup.find('div',{'id':'peoplemodule'})
epoch_time = datetime.datetime(2021, 6, 9, 2, 0).timestamp()
print("Converted epoch time:", epoch_time)

print(type+','+status+','+priority+','+resolution+','+component+','+assignee+','+reporter)
writer.writerow([type,status,priority,resolution,component,assignee,reporter])

# quit and close browser
f.close()
driver.quit()