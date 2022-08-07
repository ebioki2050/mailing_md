#!/bin/bash
cd $(dirname ${0})
date_sended_in=`cat send_in.txt`
today=$(date "+%Y-%m-%d")

echo ${date_sended_in}
echo ${today}

LF='
'

if [ "$date_sended_in" != "$today" ]; then
  python3 main.py '## Dayly' "${LF}## " '' ''  'tag: dayly(h5aK)'
  echo $today > ./send_in.txt
else
  echo "todays mail has been sent."
fi