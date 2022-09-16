# mailing markdown (mailing-md)
## purpose
- It sends mail(s) of sentence(s) got by parsing markdown file.

## works
### main.py
- read a markdown file and output mail(s)
- `python3 main.py "arg[1]" "arg[2]" "arg[3]" "arg[4]" "arg[5]"`
  - main.py needs arguments of...
    1. "reading starts with..." 
    2. "reading ends with..." 
    3. "md file splited with..." 
    4. "mails sended if the line containing..." 
    5. "mails has ... in the prefix."
- main.py needs enviroment arguments 
  - path_md_file = os.environ['PATHMDFILE']
  - from_address = os.environ['FROMADDRESS']
  - to_address = os.environ['TOADDRESS']
  - app_pass = os.environ['GOOGLEAPPPASSWORD']

### execute.sh
- this is to execute main.py once a day 
- output day_sent.txt in which sent day is written. 
- read day_sent.txt.
- execute main.py only if day_sent.txt is before today.

## prepare 
- edit sample.md or select markdown path in .env .
- set environment arguments in .env or ${HOME}/.bash_profile .
- option: 
  - (windows)set starts up shortcut or .bat file runs `wsl ${HOME}/.../mailing_md/execute1.sh`
  - (mac or linux) set cron runs execute.sh 

## main structure 
- main.py
- sample.md
- execute.sh
- day_sent.txt
- .env(rename .env-example)

## sub files 
- test.sh 
  - delete day_sent.txt and run execute.sh 
- git_iacp_mes_bra.sh 
  - git commit and push
  - argument: "commit message" "branch"