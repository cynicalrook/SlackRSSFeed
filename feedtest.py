import feedparser
import requests
import os
import configparser
import boto3
import json
import re
from datetime import datetime
from pathlib import Path
from slackclient import SlackClient

url = 'http://feeds.arstechnica.com/arstechnica/index'
keywords = {'rocket', 'SpaceX', 'Apple', 'network', 'Trump', 'Physicist', 'physics', 'Marvel', 'iOS', 'Android', 'VMware', 'Docker', 'AI', 'Artificial Intelligence', 'Microsoft'}
#keywords = {'Windows'}

#def unshorten_url(long_url):
#    session = requests.Session()  # so connections are recycled
#    resp = session.head(long_url, allow_redirects=True)
#    return resp.url

def get_s3_client(access_key_id, secret_access_key):
    return boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

def write_to_s3(client, date, feedtitle):
    body = {'date': date, "feedtitle": feedtitle}
    json_body = json.dumps(body)
    client.put_object(ACL='private', Bucket='slackrssbucket', Key='rssfeed.json', Body=json_body)

#write_to_s3('Wed, 06 Dec 2018 16:00:17 +0000', 'Ars Technica')

def get_s3_obj(client, bucket_name, bucket_file, region):
    body = client.get_object(Bucket=bucket_name, Key=bucket_file)['Body']
    return json.loads(body.read())

def post_to_slack(slack_client, newposts):
    i = 0
    newposts.reverse()
    listsize = len(newposts)
    while i < listsize:        
        slack_client.api_call("chat.postMessage", channel="CEKB88A1Y", text=newposts[i], as_user = True)
        i = i + 1

#def get_last_update(client, bucket_name, bucket_file, region):
#    body = client.get_object(Bucket=bucket_name, Key=bucket_file)['Body']
#    last_update = get_s3_obj(client, 'slackrssbucket', 'rssfeed.json', region)['date']
#    return last_update

def getfeed(client, urlstring, last_update_obj):
    newposts_list = []
    d = feedparser.parse(url)
    numentries = len(d.entries)
    last_update = datetime.strptime(last_update_obj, '%a, %d %b %Y %H:%M:%S %z')
    count = 0
    while count < numentries :
        published_date = datetime.strptime(d.entries[count].published, '%a, %d %b %Y %H:%M:%S %z')
        if published_date > last_update :    
            linktext = d.entries[count].title
#            linksplit = set(linktext.split())
#            linksplit_lower = set(map(lambda x: x.lower(), linksplit))
            linktext_lower = linktext.lower()
            linksplit_lower = re.sub("[^a-zA-Z ]+", "", linktext_lower).split()
            keywords_lower = set(map(lambda x: x.lower(), keywords))
            if (linksplit_lower & keywords_lower) :
                newposts_list.append(d.entries[count].link)             # create post list
        else:
            # insert code here to write d.feed.title and d.entries[0].published and to AWS
#            write_to_s3(d.entries[0].published, d.feed.title)
            break
        count = count + 1
    write_to_s3(client, d.entries[0].published, d.feed.title)
#    write_to_s3(client, 'Wed, 06 Dec 2018 16:00:17 +0000', 'Ars Technica')
    return newposts_list

def load_config(config_file, config_section):
#    dir_path = os.path.dirname(os.path.relpath('config.ini'))
    dir_path = os.path.abspath('.')
    if os.path.isfile(dir_path + '\\' + config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        access_key_id = config.get(config_section, 'access_key_id')
        secret_access_key = config.get(config_section, 'secret_access_key')
        region = config.get(config_section, 'region')
        bucket_name = config.get(config_section, 'bucket_name')
        bucket_file = config.get(config_section, 'bucket_file')
        slack_token = config.get(config_section, 'token')
#        slack_channels = config.get(config_section, 'channels')
#        slack_blurb = config.get(config_section, 'blurb')
#        url = config.get(config_section, 'url')
    else:
        access_key_id = os.environ['access_key_id']
        secret_access_key = os.environ['secret_access_key']
        region = os.environ['region']
        bucket_name = os.environ['bucket_name']
        bucket_file = os.environ['bucket_file']
        slack_token = os.environ['token']
 #       slack_channels = os.environ['channels']
 #       slack_blurb = os.environ['blurb']
 #       url = os.environ['url']
    return [access_key_id, secret_access_key, region, bucket_name, bucket_file, slack_token]

def main():
    config_file = 'config.ini'
    config_section = 'dev'

    (access_key_id,
     secret_access_key,
     region,
     bucket_name,
     bucket_file,
     slack_token) = load_config(config_file, config_section)

    client = get_s3_client(access_key_id, secret_access_key)
    slack_client = SlackClient(slack_token)
    last_update_obj = get_s3_obj(client, bucket_name, bucket_file, region)['date']
    post_list = getfeed(client, url, last_update_obj)
    print(post_list)
    post_to_slack(slack_client, post_list)

def lambda_handler(event, context):
    main()


#if __name__ == '__main__':
main()
