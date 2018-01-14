#!/usr/bin/python3
import urllib
from bs4 import BeautifulSoup

raidsDopeId = '250'
url_page = "http://158.69.76.135/level4.php"
payload = {
    'id': raidsDopeId,
    'holdthedoor': 'Submit'
}
timesVote = 30
testing = True

def main():
    badProx = 0
    i = 0
    tmpVC = 0
    page = urllib.request.urlopen(url_page)
    pageSoup = BeautifulSoup(page, 'html.parser')
    if testing: print(pageSoup)

    with open("proxy-list.txt", 'r') as proxFile:
        proxArr = proxFile.readlines()
    voteCount = find_id_vt_count(pageSoup, raidsDopeId)
    hiddVal = find_hidden_val(pageSoup)
    while voteCount < timesVote and voteCount is not -1:
        
        payload.update({'key': hiddVal})
        encodedPayload = urllib.parse.urlencode(payload)
        print("lol")
        print(payload)
        print('http://' + proxArr[i][:-1])

        proxy_support = urllib.request.ProxyHandler({'http' : 'http://' + proxArr[i][:-1]})
        opener = urllib.request.build_opener(proxy_support)
        opener.addheaders = [
            ('Cookie', 'HoldTheDoor={}'.format(hiddVal)),
            ('Referer', url_page),
            ('Host', '158.69.76.135'),
            ('Connection', 'keep-alive')
        ]
        try:
            page = opener.opener(url_page, encodedPayload.encode('utf8'))
        except:
            badProx += 1
            page = urllib.request.urlopen(url_page)
            pageSoup = BeautifulSoup(page, 'html.parser')

        if testing: print(page.info())

        # if page.getcode() is not 201 and page.getcode() is not 200:
        #     print("There was an error requesting for link: {}".format(url_page))
        #     break

        pageSoup = BeautifulSoup(page, 'html.parser')
        if testing: print("pagesoup:", pageSoup)
        
        try:
            tmpVC = find_id_vt_count(pageSoup, raidsDopeId)
        except:
            badProx += 1
            page = urllib.request.urlopen(url_page)
            pageSoup = BeautifulSoup(page, 'html.parser')

        if tmpVC == voteCount:
            # print(chr(27) + "[2J")
            print("Vote did not register, check something because you thing is brokedeted")
        else:
            # printing the status of the script via how many votes are successfully sent in
            # print(chr(27) + "[2J")
            print("Vote added, count at: \033[92m {} \033[0m".format(tmpVC))
            print("The Proxy failed, now a total of: \033[91m {} \033[0m failed".format(badProx))
        voteCount = tmpVC
        hiddVal = find_hidden_val(pageSoup)
        i += 1
    else:
        print("\033[93m You tried to run the script without an initial vote and/or are over x amount set in script or ran out of proxys \033[0m")

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
