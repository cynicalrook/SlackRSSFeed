import feedparser
import boto3
import json

url = 'http://feeds.arstechnica.com/arstechnica/index'
#last_update = 'Wed, 05 Dec 2018 14:52:24 +0000'
keywords = {'rocket', 'SpaceX', 'Apple', 'network', 'Trump', 'Physicist', 'physics', 'Marvel', 'iOS', 'Android', 'VMware', 'Docker', 'AI', 'Artificial Intelligence', 'Microsoft'}

client = boto3.client('s3')

def write_to_s3(date, feedtitle):
    client = boto3.client('s3')
    body = {'date': date, "feedtitle": feedtitle}
    json_body = json.dumps(body)
    client.put_object(ACL='private', Bucket='slackrssbucket', Key='rssfeed.json', Body=json_body)

#write_to_s3('Wed, 06 Dec 2018 16:00:17 +0000', 'Ars Technica')

def get_s3_obj(client, bucket_name, bucket_file, region):
    body = client.get_object(Bucket=bucket_name, Key=bucket_file)['Body']
    return json.loads(body.read())

last_update = get_s3_obj(client, 'slackrssbucket', 'rssfeed.json', 'us-east-1')['date']
print(last_update)

def getfeed(urlstring):
    d = feedparser.parse(url)
    numentries = len(d.entries)
    last_update = get_s3_obj(client, 'slackrssbucket', 'rssfeed.json', 'us-east-1')['date']
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
            write_to_s3(d.entries[0].published, d.feed.title)
            break
        count = count + 1

#    date1 = d.entries[0].published
#    date2 = d.entries[19].published
#    print(date1)
#    print(date2)
#    if date1 > date2 :
#        print('true')


getfeed(url)




