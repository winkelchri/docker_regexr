# REGEXR Docker container

The regexr (https://regexr.com/) application is great for testing out regular expressions. But if you don't want to upload sensible data to a foreign web server, you might consider using a local version of this great software. So this is what the container is for.


# How to use this image

`docker run -d -p 8080:8080 --name regexr --restart=always winkelchri/regexr`
