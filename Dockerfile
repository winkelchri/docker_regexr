FROM node:8-alpine as BASE

# ENV NODE_ENV=production

ARG REGEXR_REPO="https://github.com/gskinner/regexr/"

WORKDIR /home/node/regexr
RUN apk add --no-cache \
    git \
    python \
    gcc \
    g++ \
    make

RUN git clone ${REGEXR_REPO} . && \
    npm install && \
    npm install -g \
        gulp \
        http-server

RUN gulp deploy --v $(git tag -l | tail -n1 ) && \
    rm -rf \
        node_modules \
        build \
        server \
        dev \
        index.php \
        gulpfile.js \
        package* \
        .git
    # npm uninstall -g gulp && \
    # chown -R node:node /home/node && \

RUN sed -i '/www\.googletagmanager\.com/d' index.html && \
    sed -i '/buysellads\.com/d' index.html

FROM node:8-alpine

WORKDIR /home/node/
COPY --from=BASE --chown=node:users /home/node/regexr/assets regexr/assets
COPY --from=BASE --chown=node:users /home/node/regexr/deploy regexr/deploy
COPY --from=BASE --chown=node:users /home/node/regexr/index.html regexr/index.html
COPY --from=BASE --chown=node:users /home/node/regexr/LICENSE regexr/LICENSE

RUN chown -R node:users /home/node/ && \
    npm install -g http-server

LABEL maintainer="winkelchri@gmail.com"
LABEL description="This image is used to start the a local container with the regexr application (https://regexr.com/)"
LABEL version="0.1"
LABEL license="GPL v3"
LABEL git="https://gitlab.com/winkelchri/docker-regexr"

USER node
EXPOSE 8080

WORKDIR /home/node/regexr
CMD [ "http-server" ]
