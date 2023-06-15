import subprocess,re,json
from core.others import good,bad,info,requester
from urllib.parse import unquote
import datetime

dorks = [
            '.*\?next=.*',
            '.*\?url=.*',
            '.*\?target=.*',
            '.*\?rurl=.*',
            '.*\/dest=.*',
            '.*\/destination=.*',
            '.*\?redir=.*',
            '.*\?redirect_uri=.*',
            '.*\?return=.*',
            '.*\?return_path.*',
            '.*\/cgi-bin\/redirect\.cgi\?.*',
            '.*\?checkout_url=.*',
            '.*\?image_url=.*',
            '.*\/out\?.*',
            '.*\?continue=.*',
            '.*\?view=.*',
            '.*\/redirect\/.*',
            '.*\?go=.*',
            '.*\?redirect=.*',
            '.*\?externallink=.*',
            '.*\?nextURL=.*',
            '.*\?redir_url=.*',
            '.*\?link=.*',
            '.*\?new_url=.*',
            '.*\?forward=.*',
            '.*\?to=.*',
            '.*\?target_url=.*',
            '.*\?move_to=.*',
            '.*\?go_to=.*',
            '.*\?r=.*',
            '.*\?nav=.*',
            '.*\?jump=.*',
            '.*\?return_to=.*',
            '.*\?rlink=.*',
            '.*\?jump_to=.*',
            '.*\?redirect_to=.*',
            '.*\?navigationLink=.*'
        ]

urls = []
matchedURLs = []
def getURLs(url, path):

    file = open(path,"w", encoding='utf-8')
    fetcher(url)

    for url in urls:
        match = re.search("|".join(dorks), url, re.IGNORECASE)
        try:
            print("%s %s" % (good,match.group()))
            matchedURLs.append(match.group())
        except AttributeError:
            continue 

    if len(matchedURLs) > 0:
        for matches in matchedURLs:
            file.write("{}\n".format(matches))

    else:
        print("%s No juicy URLs found" % bad)

def fetcher(url):
        #----------------------wayback-------------------------#
        todate = datetime.date.today().year
        fromdate = todate - 2
        #result = requester("https://web.archive.org/cdx/search/cdx?url=%s*&output=json&collapse=urlkey&filter=statuscode:200&limit=1000from=%d&to=%d" % (url, fromdate, todate), False)

        result = requester("https://web.archive.org/cdx/search/cdx?url=%s*&output=json&collapse=urlkey&limit=1000from=%d&to=%d" % (url, fromdate, todate), False)

        jsonOutput = json.loads(result.text)
        for output in range(len(jsonOutput)):
            if output >= 1000:  # Set the desired upper limit for the loop
                break
            if len(jsonOutput[output]) >= 3:  # Check if the index is within the range
                url = unquote(jsonOutput[output][2])
                #print("Current output:", output, url)
                urls.append(url)
            else:
                break  # Exit the loop if the index is out of range

