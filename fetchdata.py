import urllib.request
from datetime import datetime,timedelta
import csv
x = urllib.request.urlopen('http://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalViewable/index.htm')
mystring = x.read().decode('utf-8')
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

whattofind = 'TRANSIT - HYPERLINK --><!-- .ssLINK/cot'
num = len(whattofind)
index = list(find_all(mystring, whattofind))
date = []
for i in index:
    date.append(datetime.strptime(mystring[(i+num):(i+num+6)],'%m%d%y'))
    if mystring[(i+num):(i+num+6)] == '122909':
        break
date.sort()

result = [['Date','Disaggregated Futures Only','Open Interest','Long_Producer/Merchant/Processor/User','Short_Producer/Merchant/Processor/User',
        'Long_Swap Dealers','Short_Swap Dealers','Spreading_Swap Dealers','Long_Managed Money','Short_Managed Money','Spreading_Managed Money',
          'Long_Other Reportables','Short_Other Reportables','Spreading_Other Reportables','Long_Nonreportables','Short_Nonreportables',
          'Disaggregated Futures-and-Options -Combined','Open Interest','Long_Producer/Merchant/Processor/User','Short_Producer/Merchant/Processor/User',
        'Long_Swap Dealers','Short_Swap Dealers','Spreading_Swap Dealers','Long_Managed Money','Short_Managed Money','Spreading_Managed Money',
          'Long_Other Reportables','Short_Other Reportables','Spreading_Other Reportables','Long_Nonreportables','Short_Nonreportables']]

for dd in date:
    date_string = dd.strftime('%m%d%y')
    if date_string == '031813':
        url1 = 'http://www.cftc.gov/files/dea/cotarchives/2013/futures/other_lf031913.htm'
        url2 = 'http://www.cftc.gov/files/dea/cotarchives/2013/options/other_lof031913.htm'
    elif date_string == '123113':
        url1 = 'http://www.cftc.gov/files/dea/cotarchives/2014/futures/other_lf123113.htm'
        url2 = 'http://www.cftc.gov/files/dea/cotarchives/2014/options/other_lof123113.htm'
    else:
        url1 = 'http://www.cftc.gov/files/dea/cotarchives/20' + date_string[4:6] + '/futures/other_lf' + date_string + '.htm'
        url2 = 'http://www.cftc.gov/files/dea/cotarchives/20' + date_string[4:6] + '/options/other_lof' + date_string + '.htm'
    temp = [dd.strftime('%Y%m%d'),'']
    x1 = urllib.request.urlopen(url1)
    mystring1 = x1.read().decode('utf-8').split("\n")
    for j in range(len(mystring1)):
        if "Code-088691" in mystring1[j]:
            for item in mystring1[j + 10].split(" "):
                if item not in ['',':','All']:
                    temp.append(item.replace(',','').replace(':','').replace('\r',''))
            break
    temp.append('')
    x2 = urllib.request.urlopen(url2)
    mystring2 = x2.read().decode('utf-8').split("\n")
    for j in range(len(mystring2)):
        if "Code-088691" in mystring2[j]:
            for item in mystring2[j + 10].split(" "):
                if item not in ['',':','All']:
                    temp.append(item.replace(',','').replace(':','').replace('\r',''))
            break
    result.append(temp)

url1 = 'http://www.cftc.gov/dea/futures/other_lf.htm'
url2 = 'http://www.cftc.gov/dea/options/other_lof.htm'
temp = [next_weekday(date[-1],1).strftime('%Y%m%d'),'']
x1 = urllib.request.urlopen(url1)
mystring1 = x1.read().decode('utf-8').split("\n")
for j in range(len(mystring1)):
    if "Code-088691" in mystring1[j]:
        for item in mystring1[j + 10].split(" "):
            if item not in ['',':','All']:
                temp.append(item.replace(',','').replace(':','').replace('\r',''))
        break
temp.append('')
x2 = urllib.request.urlopen(url2)
mystring2 = x2.read().decode('utf-8').split("\n")
for j in range(len(mystring2)):
    if "Code-088691" in mystring2[j]:
        for item in mystring2[j + 10].split(" "):
            if item not in ['',':','All']:
                temp.append(item.replace(',','').replace(':','').replace('\r',''))
        break
result.append(temp)
with open('C:\\Users\\yz283\\Desktop\\output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(result)
