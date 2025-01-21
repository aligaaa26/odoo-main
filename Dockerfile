FROM odoo:17.0

ARG LOCALE=en_US.UTF-8

ENV LANGUAGE=${LOCALE}
ENV LC_ALL=${LOCALE}
ENV LANG=${LOCALE}

USER 0

RUN apt-get -y update && apt-get install -y --no-install-recommends locales netcat-openbsd \
    && locale-gen ${LOCALE}

WORKDIR /app

# Menyalin folder addons dari proyekmu ke dalam container
COPY ./addons /mnt/extra-addons/

COPY --chmod=755 entrypoint.sh ./

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

ENTRYPOINT ["/bin/sh"]

CMD ["entrypoint.sh"]
