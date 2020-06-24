import sys
from bot import Bot

TEST_ARRAY = [ 
    ["AAAA google.com", ("AAAA", "google.com")],
    ["AAAA www.google.com", ("AAAA", "www.google.com")],
    ["https://google.com AAAA", ("AAAA", "google.com")],
    ["google.com", ("A", "google.com")],
    ["AAAA google.com", ("AAAA", "google.com")],
    ["com", None],
]

def main():
    bot = Bot()
    for test in TEST_ARRAY:
        if test[1] == bot.parse_query(test[0]):
            print("passed: {0}".format(test))
        else:
            print("failed: {0}".format(test))

if __name__ == "__main__":
    main()

