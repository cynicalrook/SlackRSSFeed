import os
import time
import re
import configparser
from slackclient import SlackClient


# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
starterbot_id = None
command_text = ['help', 'list feeds', 'list keywords', 'add keyword', 'add feed', 'remove keyword', 'remove feed', 'two']

def parse_bot_commands(slackbot_id, slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == slackbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(slack_client, command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command in command_text:
        if command in ('one'):
            response = 'One received'
        elif command in ('two'):
            response = 'Two received'
    else:
        response = 'Commands:\nlist feeds\nlist keywords\nadd feed <RSS feed URL>\nadd keyword <keyword>\nremove feed <feed name from *list feeds* command>\nremove keyword <keyword>'
    




    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )



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

    slack_client = SlackClient(slack_token)
    if slack_client.rtm_connect(with_team_state=False, auto_reconnect=True):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        slackbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slackbot_id, slack_client.rtm_read())
            print(slack_client.rtm_read())
            if command:
                handle_command(slack_client, command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")





#if __name__ == "__main__":
#    main()
main()

#print('Commands:\nlist feeds\nlist keywords\nadd feed <RSS feed URL>\nadd keyword <keyword>\nremove feed <feed name from \033[1mlist feeds\033[0m command>\nremove keyword <keyword>')