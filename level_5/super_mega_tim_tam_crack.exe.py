#!/usr/bin/python3
import urllib
from bs4 import BeautifulSoup
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
raidsDopeId = '250'
url_page = "http://158.69.76.135/level5.php"
windowsDeathString = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0"
payload = {
    'id': raidsDopeId,
    'holdthedoor': 'Submit'
}
timeOfVote = 1024
testing = False

def main():
    badCaptcha = 0
    page = urllib.request.urlopen(url_page)
    pageSoup = BeautifulSoup(page, 'html.parser')
    
    if testing: print(pageSoup)
    if testing: print(find_sesh_id(page))

    voteCount = find_id_vt_count(pageSoup, raidsDopeId)
    seshId = find_sesh_id(page)
    while voteCount < timeOfVote and voteCount is not -1:

        hiddVal = find_hidden_val(pageSoup)

        tmpOpener = urllib.request.build_opener()
        tmpOpener.addheaders = [
            ('User-agent', windowsDeathString),
            ('Cookie', "PHPSESSID={}; HoldTheDoor={}".format(seshId, hiddVal))
        ]
        if testing: print(tmpOpener.addheaders)
        urllib.request.install_opener(tmpOpener)
        urllib.request.urlretrieve('http://158.69.76.135' + '/tim.php', 'tim.php')
        with Image.open('tim.php') as img:
            img = img.filter(ImageFilter.MedianFilter())
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(3)
            img.save('clearCaptcha.jpg')
            crakedCaptcha = pytesseract.image_to_string(img)

        payload.update({'key': hiddVal})
        payload.update({'captcha': crakedCaptcha})
        encodedPayload = urllib.parse.urlencode(payload)
        if testing: print(payload)

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('Cookie', "PHPSESSID={}; HoldTheDoor={}".format(seshId, hiddVal)),
            ('User-Agent', windowsDeathString),
            ('Referer', url_page),
            ('Host', '158.69.76.135'),
            ('Connection', 'keep-alive')
        ]
        if testing: print(tmpOpener.addheaders)
        page = opener.open(url_page, encodedPayload.encode('utf8'))
        if testing: print(page.info())

        if page.getcode() is not 201 and page.getcode() is not 200:
            print("There was an error requesting for link: {}".format(url_page))
            break

        pageSoup = BeautifulSoup(page, 'html.parser')
        if testing: print(pageSoup)

        try:
            tmpVC = find_id_vt_count(pageSoup, raidsDopeId)
        except:
            badCaptcha += 1
            page = opener.open(url_page)
            pageSoup = BeautifulSoup(page, 'html.parser')
            continue

        if tmpVC == voteCount:
            # print fail
            print(chr(27) + "[2J")
            print("Vote did not register, check something because you thing is brokedeted")
            break
        else:
            # printing the status of the script via how many votes are successfully sent in
            voteCount = tmpVC
            print(chr(27) + "[2J")
            print("Vote added, count at: \033[92m {} \033[0m".format(tmpVC))
            print("The ORC(img to text thing magic stuff) failed a total of: \033[91m {} \033[0m times, google needs to fix their sh*t".format(badCaptcha))
    else:
        print("\033[93m You tried to run the script without an initial vote and/or are over x amount set in script \033[0m")

def find_sesh_id(pageReq):
    return pageReq.getheaders()[2][1].split(';')[0].split('=')[1]

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
