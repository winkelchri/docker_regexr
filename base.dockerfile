FROM node:8-alpine as BASE

ARG REGEXR_REPO="https://github.com/gskinner/regexr/"
ARG REGEXR_VERSION="3.6.1"
ARG BUILD_DATE=""

# LABELS
LABEL maintainer="winkelchri@gmail.com"
LABEL node_version="8"

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.description="Base image for regexr docker container"
LABEL org.label-schema.vcs-url="https://github.com/winkelchri/docker_regexr"
LABEL org.label-schema.docker.cmd="docker run -d -p 8080:8080 --name regexr --restart=always winkelchri/regexr"


WORKDIR /home/node/regexr
RUN apk add --no-cache \
    git \
    python \
    gcc \
    g++ \
    make

RUN git clone ${REGEXR_REPO} . && \
    git checkout ${REGEXR_VERSION}

# Using force to solve an dependency issue with fsevent which does not
# supports (nor is required) on linux.
RUN npm install --no-optional
RUN npm install -g \
    gulp \
    http-server

RUN gulp build-deploy

RUN sed -i '/www\.googletagmanager\.com/d' index.html && \
    sed -i '/buysellads\.com/d' index.html