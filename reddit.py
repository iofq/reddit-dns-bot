'''
TODO:
output/log/stats
bundle/interface with unbound root resolver
write testing for parse function
'''

import os
import re
import praw
import subprocess

RECORD_TYPES = ["A",
                "AAAA",
                "CNAME",
                "MX",
                "SRV",
                "TXT"]
USAGE_FLAGS = ["help",
               "usage",
               "-h"]
URL_REGEX = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
MENTION_REGEX = r"\\\+\/u\/dns\\_bot"

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     username=os.environ['CLIENT_USER'],
                     password=os.environ['CLIENT_PASS'],
                     user_agent=os.environ['USER_AGENT'])

'''
Parse record type and domain name from query
'''
def parse_query(query):
    args = query.split()
    parsed_query = []
    for h in USAGE_FLAGS:
        if h in args:
            return ["usage"]
    for record in RECORD_TYPES:
        if record in args:
            parsed_query.append(record)
            break
    else:
        parsed_query.append('A')
    for arg in args:
        arg = arg.split("://")[-1]
        if re.match(URL_REGEX, arg):
            parsed_query.append(arg)
            break
    else: # no url found
        return ["usage"]
    return parsed_query

'''
Streams from inbox and yields unread messages
'''
def stream():
    for i in reddit.inbox.stream(skip_existing=True):
        if i.new:
            yield i
'''
Build, format, and return usage/help reply
'''
def usage():
    records = "\n\n".join(['`' + s + '`' for s in RECORD_TYPES])
    return "Usage:\n\nPm me a dns query in the form 'AAAA google.com' or just 'google.com'.\n\nI currently support records:\n\n" + records

def main():
    for msg in stream():
        if isinstance(msg, praw.models.Comment) and not re.match(MENTION_REGEX, msg.body):
            print("skipping",msg.body)
            continue
        query = parse_query(msg.body)
        if "usage" in query:
            msg.reply(usage())
            continue
        answer = subprocess.run(['dig', '+short', query[0], query[1]], capture_output=True, text=True, bufsize=1, universal_newlines=True)
        print(msg.id,msg.body)
        msg.reply(re.sub('^', '    ', answer.stdout.replace("\n","\n\n")))
        msg.mark_read()

if __name__ == "__main__":
    main()
