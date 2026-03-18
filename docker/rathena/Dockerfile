FROM tvoll/ragnadocker

RUN apt-get update && apt-get install -y \
    git \
    zsh \
    nano \
    vim \
    curl \
    sudo \
    iproute2 \
    python3 \
    && rm -rf /var/lib/apt/lists/*


# garantir UTF-8 no container
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV LANGUAGE=C.UTF-8


RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" || true

RUN echo 'alias rathena-up="cd / && sh launch-athena.sh"' >> /root/.zshrc
RUN echo 'alias rathena-down="cd /usr/bin/rathena && sh ./athena-start stop"' >> /root/.zshrc
RUN echo 'alias rathena-update="cd /usr/bin/rathena && git pull"' >> /root/.zshrc

# Corrigir IPs para Docker networking
RUN sed -i 's/127.0.0.1/ragnarok-server/g' /datastoresetup/usr-bin-rathena/conf/*.conf

RUN sed -i 's|//login_ip|login_ip|g' /datastoresetup/usr-bin-rathena/conf/char_athena.conf
RUN sed -i 's|//char_ip|char_ip|g' /datastoresetup/usr-bin-rathena/conf/map_athena.conf
RUN sed -i 's|//map_ip|map_ip|g' /datastoresetup/usr-bin-rathena/conf/map_athena.conf

RUN sed -i 's/sql.db_hostname:.*/sql.db_hostname: db/g' /datastoresetup/usr-bin-rathena/conf/inter_athena.conf || true
RUN sed -i 's/sql.db_hostname:.*/sql.db_hostname: db/g' /datastoresetup/usr-bin-rathena/conf/map_athena.conf || true
RUN sed -i 's/sql.db_hostname:.*/sql.db_hostname: db/g' /datastoresetup/usr-bin-rathena/conf/char_athena.conf || true

COPY docker/rathena/start.sh /start.sh
COPY docker/rathena/casual.sh /casual.sh
COPY docker/rathena/build_ro_database.py /build_ro_database.py
COPY docker/rathena/database.html /var/www/html/database.html
COPY docker/rathena/cat_python.py /cat_python.py
COPY docker/rathena/analyzer.sh /analyzer.sh

RUN chmod +x /start.sh
RUN chmod +x /casual.sh
RUN chmod +x /analyzer.sh
RUN chmod +x /cat_python.py
RUN chmod +x /build_ro_database.py

CMD ["/start.sh"]
