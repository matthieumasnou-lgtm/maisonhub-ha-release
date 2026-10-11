# LAB ONLY. Pin upstream digest before deployment.
FROM nextcloud:apache
ARG BUILD_VERSION=0.1.0
ARG BUILD_ARCH=aarch64
LABEL io.hass.version="${BUILD_VERSION}" io.hass.type="app" io.hass.arch="${BUILD_ARCH}"
COPY apache-docroot.conf /etc/apache2/conf-enabled/maisonhub-docroot.conf
COPY apache-vhost.conf /etc/apache2/sites-available/000-default.conf
COPY start.sh /usr/local/bin/maisonhub-start
# Apache validates DocumentRoot during image build, before the runtime /data
# volume is mounted and start.sh populates /data/nextcloud-app.
# Remove the temporary directory after validation: an empty Docker volume
# otherwise copies it into /data and start.sh correctly refuses to overwrite it.
RUN chmod 0755 /usr/local/bin/maisonhub-start \
 && mkdir -p /data/nextcloud-app \
 && apache2ctl -t \
 && rmdir /data/nextcloud-app
ENTRYPOINT ["/usr/local/bin/maisonhub-start"]
CMD []
