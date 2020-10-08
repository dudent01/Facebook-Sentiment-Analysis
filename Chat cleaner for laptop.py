import os
import json
import re

rootDir = input("Enter directory with all of your messages: ")

for dirName, subDirList, fileList in os.walk(rootDir):
    for fname in fileList:
        if fname == 'message_1.json':
            with open(dirName + '/message_1.json') as f:
                chat_file = json.load(f)
            f.close()

            del chat_file['participants']
            for message in chat_file['messages']:
                if message['type'] != 'Generic':
                    message['content'] = 'Non-textual'
                if 'share' in message:
                    del message['share']
                if 'photos' in message:
                    del message['photos']
                del message['timestamp_ms']
                del message['type']
                if 'content' in message:
                    if re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))', message['content']):
                        message['content'] = 'URL'

            with open(dirName + '/message_1_clean.json', "w") as f:
                json.dump(chat_file, f, indent=2)
            f.close()