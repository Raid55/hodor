#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
import random

raidsDopeId = '250'
url_page = "http://158.69.76.135/level4.php"
payload = {
    'id': raidsDopeId,
    'holdthedoor': 'Submit'
}
timesVote = 98
testing = False


def main():
    badProxCount = 0
    failedAtt = 0
    with open("proxy-list.txt", 'r') as proxFile:
        proxArr = proxFile.readlines()
    with open("proxy-dump-list.txt", 'r') as dumpFile:
        badProxArr = dumpFile.readlines()
    page = requests.get(url_page)
    pageSoup = BeautifulSoup(page.content, 'html.parser')
    if testing: print(pageSoup)

    voteCount = find_id_vt_count(pageSoup, raidsDopeId)
    hiddVal = find_hidden_val(pageSoup)
    while voteCount < timesVote and voteCount is not -1:
        tmpProx = find_new_prox(proxArr, badProxArr)
        headers = {
            'Cookie': "HoldTheDoor={}".format(hiddVal),
            'Referer': url_page,
            'Host': "158.69.76.135",
            'Connection': "keep-alive"
        }
        payload.update({'key': hiddVal})
        try:
            print("\033[1mTrying proxy:\033[0m \033[94m{}\033[0m".format(tmpProx))
            page = requests.post(
                url_page, 
                proxies={'http': "http://" + tmpProx},
                headers=headers,
                data=payload,
                timeout=2)
        except:
            page = requests.get(url_page)
            badProxCount += 1
            badProxArr.append(tmpProx + "\n")

        pageSoup = BeautifulSoup(page.content, 'html.parser')
        if testing: print(pageSoup)
        
        try:
            hiddVal = find_hidden_val(pageSoup)
            tmpVC = find_id_vt_count(pageSoup, raidsDopeId)
        except:
            failedAtt += 1

        if tmpVC == voteCount:
            print(chr(27) + "[2J")
            print("\033[93mVote did not register, loop will continue...\033[0m")
            print("Votes failed a total of \033[91m{}\033[0m times".format(failedAtt))
            print("The Proxy failed, now a total of: \033[91m {} \033[0m failed".format(badProxCount))
            print("VoteCount at: \033[92m {} \033[0m".format(tmpVC))
        else:
            # printing the status of the script via how many votes are successfully sent in
            print(chr(27) + "[2J")
            print("\033[92mVOTE ADDED!!!\033[0m")
            print("Vote added, count at: \033[92m {} \033[0m".format(tmpVC))
            print("The Proxy failed, now a total of: \033[91m {} \033[0m failed".format(badProxCount))
            print("Votes failed a total of \033[93m{}\033[0m times".format(failedAtt))
        voteCount = tmpVC
    else:
        print("\033[93mYou tried to run the script without an initial vote and/or are over x amount set in script or ran out of proxys \033[0m")
    with open("proxy-dump-list.txt", 'w') as dumpFile:
        for x in badProxArr:
            dumpFile.write(x)

def find_new_prox(proxList, badProx):
    tmp = random.choice(proxList)
    
    i = 0
    try:
        badProx.index(tmp)
        return find_new_prox(proxList, badProx)
    except:
        return tmp[:-1]

def find_hidden_val(soup):
    """function that returns the rand key generated per req
    """
    return soup.find('input', {'name':'key'})['value']

def find_id_vt_count(soup, id):
    """func that finds voter id and returns how many votes he has
    """
    rows = iter(soup.find('table').find_all('tr'))
    for row in rows:
        row = row.text.split()
        if row[0] == id:
            votecount = int(row[1])
            break
        else:
            votecount = -1
    return votecount





if __name__ == '__main__':
    main()

#  yourdate = datetime.today()
#     print(type(yourdate))
#     print(yourdate)
#     print(datetime.today())
#     print(timedelta(1))
#     print((datetime.today() - yourdate).days)
#     if (datetime.today() - yourdate).days > 0:
#         print("LOL")
