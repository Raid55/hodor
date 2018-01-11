#!/usr/bin/python3
import urllib
from bs4 import BeautifulSoup

raidsDopeId = '250'
url_page = "http://158.69.76.135/level1.php"
payload = {
    'id': raidsDopeId,
    'holdthedoor': 'Submit'
}

def main():
    page = urllib.request.urlopen(url_page)
    pageSoup = BeautifulSoup(page, 'html.parser')

    voteCount = find_id_vt_count(pageSoup, raidsDopeId)
    hiddVal = find_hidden_val(pageSoup)
    while voteCount < 4096 and find_id_vt_count(pageSoup, raidsDopeId) is not -1:
        
        payload.update({'key': find_hidden_val(pageSoup)})
        encodedPayload = urllib.parse.urlencode(payload)
        # print(payload)

        opener = urllib.request.build_opener()
        opener.addheaders.append(('Cookie', 'HoldTheDoor={}'.format(hiddVal)))
        results = opener.open(url_page, encodedPayload.encode('utf8'))
        # print(results)

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
