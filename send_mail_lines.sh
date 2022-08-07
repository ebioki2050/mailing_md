#!/bin/bash
cd $(dirname ${0})
date_sended_in=`cat send_in_lines.txt`
today=$(date "+%Y-%m-%d")

echo ${date_sended_in}
echo ${today}

LF='
'

if [ "$date_sended_in" != "$today" ]; then
  python3 main.py '' "" "${LF}" '- [ ] ' 'tag: to-do-ticket(8gJm)'
  echo $today > ./send_in_lines.txt
else
  echo "todays mail has been sent."
fi