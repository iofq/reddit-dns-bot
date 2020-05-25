CONTAINER="reddit"
IMAGE="reddit_dns_bot"

docker build . -t $IMAGE

docker run --rm -it --name $CONTAINER \
	-v $PWD:/tmp/python \
	--dns=1.1.1.1 \
  -e CLIENT_ID="xxxxxxxxxx" \
  -e CLIENT_SECRET="xxxxxxxxxxxxxx" \
  -e CLIENT_USER="user" \
  -e CLIENT_PASS="password!" \
  -e USER_AGENT="unique user agent v1.0" \
	$IMAGE 
