from Wiki_Bot import getLogContents
import wikitextparser as wikiParse
import bs4
import datetime
import time

heartRateLog_page = 'Heart Rate Log'


def get_hrLog_list():
    hrLogContents = getLogContents(heartRateLog_page, clearAfter=True)

    parsed_hrLog = bs4.BeautifulSoup(hrLogContents, 'lxml')
    hrLog_RawText = parsed_hrLog.page.text
    hrLog_wikiParsed = wikiParse.parse(hrLog_RawText)

    hrLog_RawList = hrLog_wikiParsed.lists()[0]  # extract list as an array

    hrLog_ArrayList = hrLog_RawList.items

    return hrLog_ArrayList


def save_hrLogReading(hrLog_ArrayList):
    logArchive_path = './Log Archive/'
    dateNow = str(datetime.date.today())
    timeNow = str(time.strftime('%H_%M'))

    logFile_Name = logArchive_path + 'Heart Monitor Log_' + dateNow + timeNow + '.csv'

    logFile = open(logFile_Name, 'w')

    for entry in hrLog_ArrayList:
        logFile.write(entry + '\n')

    logFile.close()

    return logFile_Name


print(save_hrLogReading(get_hrLog_list()))
