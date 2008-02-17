#!/bin/sh
#0,10,20,30,40,50 * * * * (cd public_html/irlp/calls; sh cron.sh)

r=`date -u +%H%M`
sh status.sh | perl connects.pl > xx
mv xx recent/$r
