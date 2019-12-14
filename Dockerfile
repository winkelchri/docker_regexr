ARG VERSION=""

FROM winkelchri/regexr-base:${VERSION} as BASE

FROM node:10-alpine

ARG BUILD_DATE=""

ENV NODE_ENV=production

# LABELS
LABEL maintainer="winkelchri@gmail.com"

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.vcs-url="https://github.com/winkelchri/docker_regexr"
LABEL org.label-schema.docker.cmd="docker run -d -p 8080:8080 --name regexr --restart=always winkelchri/regexr"
LABEL org.label-schema.description="This image is used to start the a local container with the regexr application (https://regexr.com/)"
LABEL org.label-schema.version="0.1"

WORKDIR /home/node/
COPY --from=BASE --chown=node:users /home/node/regexr/assets regexr/assets
COPY --from=BASE --chown=node:users /home/node/regexr/deploy regexr/deploy
COPY --from=BASE --chown=node:users /home/node/regexr/index.html regexr/index.html
COPY --from=BASE --chown=node:users /home/node/regexr/LICENSE regexr/LICENSE

RUN chown -R node:users /home/node/ && \
    npm install -g http-server

USER node
EXPOSE 8080

WORKDIR /home/node/regexr
CMD [ "http-server" ]
