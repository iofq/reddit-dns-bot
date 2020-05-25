FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt update && apt install -y python3 python3-pip
RUN apt install -y dnsutils
RUN pip3 install praw

WORKDIR /tmp/python

ENTRYPOINT ["/bin/python3"]
CMD ["reddit.py"]
