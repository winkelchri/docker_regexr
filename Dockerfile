FROM node:8-alpine

LABEL maintainer="winkelchri@gmail.com"
LABEL description="This image is used to start the a local container with the regexr application (https://regexr.com/)"
LABEL version="0.1"
LABEL license="GPL v3"
LABEL git="https://gitlab.com/winkelchri/docker-regexr"

# ENV NODE_ENV=production

ARG REGEXR_REPO="https://github.com/gskinner/regexr/"

WORKDIR /home/node/regexr
RUN apk add --no-cache --virtual .build-deps \
    git \
    python \
    gcc \
    g++ \
    make && \
    git clone ${REGEXR_REPO} . && \
    npm install && \
    npm install -g \
        gulp \
        http-server && \
    gulp deploy --v $(git tag -l | tail -n1 ) && \
    sed -i '/www\.googletagmanager\.com/d' index.html && \
    sed -i '/buysellads\.com/d' index.html && \
    rm -rf \
        node_modules \
        build \
        server \
        dev \
        index.php \
        gulpfile.js \
        package* \
        .git \
        && \
    npm uninstall -g gulp && \
    chown -R node:node /home/node && \
    apk del .build-deps

USER node
CMD [ "http-server" ]

EXPOSE 8080
