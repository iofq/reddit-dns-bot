'''
TODO:
bundle/interface with unbound root resolver
testingggg
'''

import os
import re
import praw
import prawcore
import subprocess

class Bot:

    RECORD_TYPES = ["A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "SRV",
                    "TXT"]
    URL_REGEX = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

    def __init__(self):
        super().__init__()
        self.reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     username=os.environ['CLIENT_USER'],
                     password=os.environ['CLIENT_PASS'],
                     user_agent=os.environ['USER_AGENT'])
        self.url_regex = re.compile(self.URL_REGEX, re.IGNORECASE)

    def parse_query(self, query):
        args = query.split()
        for record in self.RECORD_TYPES:
            if record in args:
                break
        else: 
            record = 'A'
        for domain in args:
            domain = domain.split("://")[-1]
            if self.url_regex.match(domain):
                break
        else:
            return None
        return (record, domain)

    def respond(self, msg, response):
        try:
            #format for reddit's code block
            msg.reply(re.sub('\n', '\n    ', response))
        except prawcore.exceptions.Forbidden:
            print("  ERR: Forbidden: unable to reply to message".format(msg.id))
        except praw.exceptions.RedditAPIException:
            print("  ERR: Tried to reply with blank response")
        except:
            print("  ERR: undefined error: {} {}".format(msg, response))
        msg.mark_read()

    def log(self, entry):
        print("{} | {} -> {}".format(entry[0], entry[1], entry[2].replace("\n","\n  - ")))

    def start(self):
        print("listening for queries...")
        for msg in self.reddit.inbox.stream():
            #if msg is a DM and is new
            if not(isinstance(msg, praw.models.Message) and not msg.was_comment and msg.new):
                continue
            query = self.parse_query(msg.body)
            if query is None:
                print("Invalid query -> {}".format(msg.body))
                msg.mark_read()
                continue
            response = subprocess.run([ 'dig', '+short', query[0], query[1]],
                capture_output=True, 
                text=True, 
                bufsize=1,
                universal_newlines=True)
            reply = "\n" + response.stdout.rstrip() 
            self.log([msg.id, query, reply])
            self.respond(msg, reply)

if __name__ == "__main__":
    bot = Bot()
    bot.start()
