#!/bin/bash
cd $(dirname ${0})
LF='
'
# initialize
path_sent_day="day_sent1.txt"
date_sended_in=`cat ${path_sent_day}`

today=$(date "+%Y-%m-%d")
echo ${date_sended_in}
echo ${today}
if [ "$date_sended_in" != "$today" ]; then
  python3 main.py '' "" "${LF}" '- [ ] ' 'tag: to-do-ticket(8gJm)'
  echo $today > ./${path_sent_day}
else
  echo "todays mail has been sent."
fi