#!/usr/bin/python3
import urllib
from bs4 import BeautifulSoup

raidsDopeId = '250'
quote_page = "http://158.69.76.135/level0.php"
data = urllib.parse.urlencode({
    'id': raidsDopeId,
    'holdthedoor': 'Submit'
})

def main():
    page = urllib.request.urlopen(quote_page)
    pageSoup = BeautifulSoup(page, 'html.parser')

    while find_id_vt_count(pageSoup, raidsDopeId) < 1024 and find_id_vt_count(pageSoup, raidsDopeId) is not -1:
        results = urllib.request.urlopen(quote_page, data.encode('utf8'))
        pageSoup = BeautifulSoup(results, 'html.parser')
        print(find_id_vt_count(pageSoup, raidsDopeId))


def find_id_vt_count(soup, id):
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
