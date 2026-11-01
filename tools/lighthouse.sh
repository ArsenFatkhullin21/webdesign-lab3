#!/bin/bash
# Запуск Lighthouse: tools/lighthouse.sh <url> <папка-вывода> <имя>
# Нужно: npm i lighthouse (глобально или в /tmp), Google Chrome.
export CHROME_PATH="${CHROME_PATH:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
LH="${LH:-npx lighthouse}"
mkdir -p "$2"
for dev in mobile desktop; do
  P=""; [ $dev = desktop ] && P="--preset=desktop"
  $LH "$1" $P --chrome-flags="--headless=new --no-sandbox" --output=json --output=html \
      --output-path="$2/$3-$dev" --quiet
done
