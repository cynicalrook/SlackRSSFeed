import feedparser
#import datetime from datetime

url = 'http://feeds.arstechnica.com/arstechnica/index'
last_update = 'Wed, 05 Dec 2018 14:52:24 +0000'
keywords = {'rocket', 'SpaceX', 'Apple', 'network', 'Trump', 'Physicist', 'physics', 'Marvel', 'iOS', 'Android', 'VMware', 'Docker', 'AI', 'Artificial Intelligence', 'Microsoft'}

def getfeed(urlstring):
    d = feedparser.parse(url)
    numentries = len(d.entries)
#    print(numentries)
    count = 0
    while count < numentries :
        if d.entries[count].published > last_update :
            linktext = d.entries[count].title
            linksplit = set(linktext.split())
            linksplit_lower = set(map(lambda x: x.lower(), linksplit))
            keywords_lower = set(map(lambda x: x.lower(), keywords))
            if (linksplit_lower & keywords_lower) :
                # insert code here to insert url in slack
                print(d.entries[count].title)
                print(d.entries[count].link)
                print(d.entries[count].published) 
        else:
            # insert code here to write d.feed.title and d.entries[0].published and to AWS
            break
        count = count + 1

#    date1 = d.entries[0].published
#    date2 = d.entries[19].published
#    print(date1)
#    print(date2)
#    if date1 > date2 :
#        print('true')


getfeed(url)




