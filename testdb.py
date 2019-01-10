import sys
sys.path.append('/Users/steve/Documents/python-virtual-environments/tinydbtest/Lib/site-packages')
from tinydb import TinyDB, Query

db = TinyDB('rsslist.json')

item1 = {"feedtitle": "Ars Technica", "url": "http://feeds.arstechnica.com/arstechnica/index"}
item2 = {"feedtitle": "TechSpot", "url": "https://www.techspot.com/backend.xml"}
item3 = {"feedtitle": "MIT", "url": "https://goes.here"}

#db.insert(item1)
#db.insert(item2)
#db.insert(item3)



#title = 'TechSpot'
#feed = Query()



#results = db.search(feed.feedtitle == title)
#print(results[0])

#if results != []:
#if db.search(feed.feedtitle == title) != []:
#    db.remove(feed.feedtitle.search(title))
#else:
#    print('no match')


#print(b)

#c = db.search(feed.feedtitle == 'TechSpot')
#print(c)


#feedlist = Query()
#f = db.search(feedlist.url != [])[0]
#urlnew = db.get(doc_id = 1)['url']

#print(f)
#print(urlnew)


#print(len(db))
#print(db.all())


