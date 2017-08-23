import requests
import pandas as pd
from lxml import etree
import bs4
import wikitextparser as wikiParse
import datetime
import time

username = 'Samv'
password = 'Saemsaem22'
#password = 'eqqfk2n9kshmegek2khraqgl4cdhqo7g' # see https://www.mediawiki.org/wiki/Manual:Bot_passwords
api_url = 'http://leucadia760.ddns.net:65500/mediawiki/api.php'


summary = 'bot hello'
message = 'Hello Wikipedia. I am alive!'

#***** Page Names **********
life_todo_page = "Life Todo's"
heartRateLog_page = 'Heart Rate Log'
#*******initialize Session**********
session = requests.Session()

# get login token
r1 = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
})
r1.raise_for_status()

# log in
r2 = session.post(api_url, data={
    'format': 'json',
    'action': 'login',
    'lgname': username,
    'lgpassword': password,
    'lgtoken': r1.json()['query']['tokens']['logintoken'],
})
if r2.json()['login']['result'] != 'Success':
    raise RuntimeError(r2.json()['login']['reason'])

# get edit token
editSession = session.get(api_url, params={
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
})

#**********End of Initialization***********

def getPage(url, pageName, contentsOnly):

    page = session.get(api_url, params= {
       'format': 'json',
       'action': 'query',
        'titles': pageName,
       'export': '1'
    })

    if contentsOnly:
        return page.json()['query']['export']['*'] #only return the response
    else:
        return page #return the whole page object thing

def writeToLogPage(url, editSession, pageName, logValue):

    logSession = session.post(api_url, data={
        'format': 'json',
        'action': 'edit',
        'assert': 'user',
        'prependtext': logValue,
        #'summary': summary,
        'title': pageName,
        'token': editSession.json()['query']['tokens']['csrftoken'],
    })

    print(logSession.json())



lifeToDos = getPage(api_url, life_todo_page, contentsOnly= 'Y')

'''
# save the edit
r4 = session.post(api_url, data={
    'format': 'json',
    'action': 'edit',
    'assert': 'user',
    'appendtext': message,
    'summary': summary,
    'title': page,
    'token': r3.json()['query']['tokens']['csrftoken'],
})
'''

def logHeartRate(ibi_avg, bpm_avg):

    eventType = {1:'Measurement', 2: 'EventOccurance'}
    dateNow = str(datetime.date.today())
    timeNow = str(time.strftime('%H:%M:%S'))


    log = '*' + eventType[1] + ', ' + str(bpm_avg) + ', ' + timeNow + ', ' + dateNow +  ',\n' #TODO: Log Stdev of IBI and BPM

    writeToLogPage(api_url, editSession, heartRateLog_page, log)


def getLogContents(logFileName, clearAfter=False):
    logContents = getPage(api_url, logFileName, contentsOnly=True)

    if clearAfter:
        clearSession = session.post(api_url, data={
            'format': 'json',
            'action': 'edit',
            'assert': 'user',
            'text': '',
            # 'summary': summary,
            'title': logFileName,
            'token': editSession.json()['query']['tokens']['csrftoken'],
        })

    return logContents




parsedTodos = bs4.BeautifulSoup(lifeToDos, 'lxml')
lifeToDos_RawText = parsedTodos.page.text
lifeToDos_Parsed = wikiParse.parse(lifeToDos_RawText)

for section in lifeToDos_Parsed.sections:
    text = section.contents
    parsedText = wikiParse.parse(text)
    print(section.title)
    print("items:")

    if len(parsedText.lists()) > 0:
        todoList = parsedText.lists()[0]
        for item in todoList.items:
            print('\t' + item)
    else:
        print("\tNone")
    print('\n******\n')




#todoData = pd.DataFrame(response)
#print todoData
#print (r4.text)