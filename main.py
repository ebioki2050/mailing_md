import markdown
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from dotenv import load_dotenv
import sys

def readlines_md_file(path_md_file, start_to_read_with, end_to_read_with, split_with, text_if_in):
  # load a .md file and put it in argument "text_markdown"
  text_markdown = ""
  with open(path_md_file, "r", encoding='UTF-8') as file:
    text_markdown = file.read()
  
  # get text_markdown in a specific range we want
  if (len(start_to_read_with)>0):
    target = start_to_read_with 
    idx = text_markdown.find(target) 
    text_markdown = text_markdown[idx:]
  if (len(end_to_read_with)>0):
    target = end_to_read_with
    idx = text_markdown.find(target)
    text_markdown = text_markdown[:idx]

  # split text_markdown and put it in list
  row_lines = []
  if (len(split_with)>0):
    for line in text_markdown.split("{}".format(split_with)):
      if len(line) == 0:
        continue
      row_lines.append(split_with.replace("\n", "") + line) 
  else:
    row_lines.append(text_markdown)
  # select lines which mutch with a condition
  text_markdown_lines = []
  if (len(text_if_in)>0):
    for line in row_lines:
      if (len(line)!=0) & (text_if_in in line):
        text_markdown_lines.append(line.replace(text_if_in, ""))
  else:
    for line in row_lines:
      if (len(line)!=0):
        text_markdown_lines.append(line)
  text_markdown_lines.reverse()
  return text_markdown_lines


def render_html_mail_content_from_md_file(text_markdown, content_appendix):
  message = MIMEMultipart()
  md = markdown.Markdown(extensions=['tables'])
  # md = markdown.Markdown(extensions=['tables', 'markdown_checklist.extension'])
  # [Third Party Extensions · Python-Markdown/markdown Wiki](https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions)
  text_html = md.convert(text_markdown)
  content_html = text_html
  content_html += content_appendix
  message.attach(MIMEText(content_html, "html"))
  return message

def make_subject(date_to_send, title_md, str_count, str_count_all):
  return date_to_send + " " + title_md + " " + str_count + "/" + str_count_all + " (Mailing_Md By Python)"

def main():
  # initialize(read env file)
  load_dotenv('./.env')
  path_md_file = os.environ['PATHMDFILE']
  from_address = os.environ['GMAILADDRESS']
  to_address = os.environ['GMAILADDRESS']
  app_pass = os.environ['GOOGLEAPPPASSWORD']

  # initialize(read arguments)
  args = sys.argv
  title_shortize = True
  md_file_range_from = args[1]
  md_file_range_to = args[2]
  md_file_splitter = args[3]
  text_if_in = args[4]
  content_appendix = args[5]
  for i, arg in enumerate(args):
    print("arg[{}]: {}".format(i, arg))

  # prepare smtp object
  smtp_server = "smtp.gmail.com"
  sender = smtplib.SMTP_SSL(smtp_server)
  login_name = from_address
  sender.login(login_name, app_pass)

  # load a markdown file as a list of texts and get title
  title_md = os.path.splitext(os.path.basename(path_md_file))[0]
  if (title_shortize):
    title_md = title_md[:4]

  text_markdown_lines = readlines_md_file(path_md_file, md_file_range_from, md_file_range_to, md_file_splitter, text_if_in)

  # make and send message 
  for count,line in enumerate(text_markdown_lines):
    message = render_html_mail_content_from_md_file(line, content_appendix)
    message["FROM"]=from_address
    message["TO"]=to_address
    date_today = datetime.datetime.today().strftime("%Y-%m-%d")
    # message["subject"] = date_today + " " + title_md + " " + str(count+1) + "/" + str(len(text_markdown_lines))
    message["subject"] = make_subject(date_today, title_md, str(count+1), str(len(text_markdown_lines)))
    sender.send_message(message)
    print("send mail of {}/{}".format(count+1, len(text_markdown_lines)))

if __name__ == "__main__":
  main()