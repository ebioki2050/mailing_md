#!/bin/bash
cd $(dirname ${0})
source .env
source ${HOME}/.profile

# initialize
path_sent_day="day_sent.txt"
date_sended_in=`cat ${path_sent_day}`

today=$(date "+%Y-%m-%d")
echo ${date_sended_in}
echo ${today}

LF='
'

# execute if recoded date is before today. 
if [ "$date_sended_in" != "$today" ]; then
  python3 main.py '' "" "${LF}" '- [ ] ' 'tag: to-do-ticket'
  python3 main.py "## Dayly" "${LF}## " "${LF}### " '' 'tag: to-do-on-time'
  echo $today > ./${path_sent_day}
else
  echo "todays mail has been sent."
fi