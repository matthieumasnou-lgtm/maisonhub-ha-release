#!/bin/sh
set -eu
app=/data/nextcloud-app
[ -d /data ] || { echo 'Missing persistent HA /data'; exit 1; }
[ ! -L /data ] || { echo 'Refusing symlinked /data'; exit 1; }
if [ ! -e "$app/.maisonhub-initialized" ]; then
  [ ! -e "$app" ] || { echo 'Incomplete or existing app: manual recovery required'; exit 1; }
  mkdir "$app"
  cp -a /usr/src/nextcloud/. "$app"/
  mkdir -p "$app/data"
  chown -R www-data:www-data "$app"
  chmod 0750 "$app/data"
  touch "$app/.maisonhub-initialized"
fi
[ -f "$app/occ" ] && [ -f "$app/version.php" ] || { echo 'Invalid app state'; exit 1; }
# Refuse to start if configuration path escapes the app tree.
[ ! -L "$app/config" ] || { echo 'Symlinked config refused'; exit 1; }
exec apache2-foreground
