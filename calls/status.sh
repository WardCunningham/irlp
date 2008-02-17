#/bin/sh
export TERM=vt100
export TEMP=/usr/tmp
lynx -source http://status.irlp.net/nohtmlstatus.txt | tee nodes.txt
