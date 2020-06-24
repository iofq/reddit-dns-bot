FROM iofq/docker-unbound:latest

RUN apk update && apk add --no-cache python3 py3-pip bind-tools && \
  pip3 install --upgrade pip && \
  pip3 install praw 

WORKDIR /run/python
COPY bot.py entrypoint.sh ./

ENTRYPOINT ["/bin/sh"]
CMD ["entrypoint.sh"]
