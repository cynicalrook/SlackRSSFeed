import feedparser
import datetime from datetime

url = 'http://feeds.arstechnica.com/arstechnica/index'

# Key words:  rocket, SpaceX, Apple, network, Trump, Physicist, physics, Marvel, iOS, Android, VMware, Docker
keywords = {'rocket', 'SpaceX', 'Apple', 'network', 'Trump', 'Physicist', 'physics', 'Marvel', 'iOS', 'Android', 'VMware', 'Docker'}

d = feedparser.parse(url)

numentries = len(d.entries)
print(numentries)
count = 0
while count < numentries :
    linktext = d.entries[count].title
    linksplit = set(linktext.split())
    linksplit_lower = set(map(lambda x: x.lower(), linksplit))
    keywords_lower = set(map(lambda x: x.lower(), keywords))
    if (linksplit_lower & keywords_lower) :
        print(d.entries[count].title)
        print(d.entries[count].link)
        print(d.entries[count].published) 
        print(linksplit_lower)
        print(keywords_lower)
    count = count + 1

date1 = d.entries[0].published
date2 = d.entries[19].published

print(date1)
print(date2)
if date1 > date2 :
    print('true')




