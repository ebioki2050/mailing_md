#!/bin/bash
cd $(dirname ${0})
date_sended_in=`cat send_in.txt`
today=$(date "+%Y-%m-%d")

echo ${date_sended_in}
echo ${today}

if [ "$date_sended_in" != "$today" ]; then
  echo $today > ./send_in.txt
  python3 main.py
else
  echo "todays mail has been sent."
fi