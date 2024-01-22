#!/bin/sh
#


KeyID="0ICUzWHZHb9VwZQ_h6gc6A"
DOM='obsd.eis.utoronto.ca'
UID='russell.sutherland@utoronto.ca'
PWD='rogersQ1!'

#curl "https://cert-manager.com/api/acme/v2/account/${KeyID}/domain" -i -X POST \

curl -vvv  'https://cert-manager.com/api/acme/v2/account/0ICUzWHZHb9VwZQ_h6gc6A/domain' -i -X POST \
  -H 'Content-Type: application/json' \
  -H "login: $UID" \
  -H "password: $PWD" \
  -H 'customerUri: uot' \
  -d '{"domains":[{"name":"obsd.eis.utoronto.ca"}]}'
