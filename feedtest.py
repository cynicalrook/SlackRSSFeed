import feedparser
import requests
import os
import configparser
import boto3
import json
from datetime import datetime
from slackclient import SlackClient

url = 'http://feeds.arstechnica.com/arstechnica/index'
keywords = {'rocket', 'SpaceX', 'Apple', 'network', 'Trump', 'Physicist', 'physics', 'Marvel', 'iOS', 'Android', 'VMware', 'Docker', 'AI', 'Artificial Intelligence', 'Microsoft'}
#keywords = ['AI']
token = ''
slack_client = SlackClient(token)
client = boto3.client('s3')
post_list = []
    
#last_update = 'Wed, 05 Dec 2018 14:52:24 +0000'


def load_config(config_file, config_section):
    dir_path = os.path.dirname(os.path.relpath(__file__))
    if os.path.isfile(dir_path + '/' + config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        access_key_id = config.get(config_section, 'access_key_id')
        secret_access_key = config.get(config_section, 'secret_access_key')
        region = config.get(config_section, 'region')
#        bucket_name = config.get(config_section, 'bucket_name')
#        bucket_file = config.get(config_section, 'bucket_file')
        slack_token = config.get(config_section, 'token')
#        slack_channels = config.get(config_section, 'channels')
#        slack_blurb = config.get(config_section, 'blurb')
#        url = config.get(config_section, 'url')
    else:
        access_key_id = os.environ['access_key_id']
        secret_access_key = os.environ['secret_access_key']
        region = os.environ['region']
 #       bucket_name = os.environ['bucket_name']
 #       bucket_file = os.environ['bucket_file']
        slack_token = os.environ['token']
 #       slack_channels = os.environ['channels']
 #       slack_blurb = os.environ['blurb']
 #       url = os.environ['url']
    return [access_key_id, secret_access_key, region, slack_token]

def lambda_handler(event, context):
    main()

def unshorten_url(long_url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(long_url, allow_redirects=True)
    return resp.url
 
def write_to_s3(date, feedtitle):
    body = {'date': date, "feedtitle": feedtitle}
    json_body = json.dumps(body)
    client.put_object(ACL='private', Bucket='slackrssbucket', Key='rssfeed.json', Body=json_body)

#write_to_s3('Wed, 06 Dec 2018 16:00:17 +0000', 'Ars Technica')

def get_s3_obj(client, bucket_name, bucket_file, region):
    body = client.get_object(Bucket=bucket_name, Key=bucket_file)['Body']
    return json.loads(body.read())

def post_to_slack():
    i = 0
    post_list.reverse()
    listsize = len(post_list)
    while i < listsize:        
        slack_client.api_call("chat.postMessage", channel="CEKB88A1Y", text=post_list[i], as_user = True)
        i = i + 1

def getfeed(urlstring):
    d = feedparser.parse(url)
    numentries = len(d.entries)
    last_update_obj = get_s3_obj(client, 'slackrssbucket', 'rssfeed.json', 'us-east-1')['date']
    last_update = datetime.strptime(last_update_obj, '%a, %d %b %Y %H:%M:%S %z')
    count = 0
    while count < numentries :
        published_date = datetime.strptime(d.entries[count].published, '%a, %d %b %Y %H:%M:%S %z')
        if published_date > last_update :    
            linktext = d.entries[count].title
            linksplit = set(linktext.split())
            linksplit_lower = set(map(lambda x: x.lower(), linksplit))
            keywords_lower = set(map(lambda x: x.lower(), keywords))
            if (linksplit_lower & keywords_lower) :
                post_list.append(d.entries[count].link)             # create post list
#                short_url = unshorten_url(d.entries[count].link)
#                post_list.append(short_url)
        else:
            # insert code here to write d.feed.title and d.entries[0].published and to AWS
#            write_to_s3(d.entries[0].published, d.feed.title)
            break
        count = count + 1
    write_to_s3(d.entries[0].published, d.feed.title)

#    date1 = d.entries[0].published
#    date2 = d.entries[19].published
#    print(date1)
#    print(date2)
#    if date1 > date2 :
#        print('true')


#print(post_list)
#last_update = get_s3_obj(client, 'slackrssbucket', 'rssfeed.json', 'us-east-1')['date']
#print(last_update)

def main():
#    config_file = 'config.ini'
#    config_section = 'dev'

#    (access_key_id,
#     secret_access_key,
#     region,
#     slack_token) = load_config(config_file, config_section)

    getfeed(url)
#    post_to_slack()
#    print(post_list)

#if __name__ == '__main__':

main()
