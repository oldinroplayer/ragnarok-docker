FROM alpine:3.19

WORKDIR /opt

RUN apk add --no-cache \
    git \
    nodejs \
    npm \
    bash \
    nano \
    curl \
    gettext

RUN npm install -g wsproxy http-server

# baixar robrowser
RUN git clone https://github.com/MrAntares/roBrowserLegacy

WORKDIR /opt/roBrowserLegacy

# instalar dependências
RUN npm install

# build
RUN npm run build -- -O -T -H

# copiar build final
RUN cp -r dist/Web/* .

# copiar template
COPY Config.local.template.js /opt/Config.local.template.js

EXPOSE 8080 5999

CMD sh -c "cd /opt/roBrowserLegacy && envsubst < /opt/Config.local.template.js > Config.local.js && wsproxy -a ragnarok-server:6900,ragnarok-server:6121,ragnarok-server:5121 & http-server -p 8080 -a 0.0.0.0"
