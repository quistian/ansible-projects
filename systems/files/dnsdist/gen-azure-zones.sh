#!/bin/sh
#
PATH=/bin:/usr/bin:/usr/local/bin

TMP=/tmp/azure-zones.$$

cat azure-zones | grep -v privatelink | sort | uniq  > azure-pub-zones
cat azure-zones | grep privatelink | sort | uniq  > azure-priv-zones
# cat azure-priv-zones | sed -e 's/^privatelink.//' >> azure-pub-zones
# cat azure-pub-zones | sort | uniq > $TMP
# mv $TMP azure-pub-zones

rm -f $TMP
