import markdown
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from dotenv import load_dotenv

def readlines_md_file(path_md_file):
  with open(path_md_file, "r", encoding='UTF-8') as file:
    text_markdown_lists = file.readlines()
    text_markdown_lists = [line.strip() for line in text_markdown_lists]
  return text_markdown_lists

def render_html_mail_content_from_md_file(text_markdown):
  message = MIMEMultipart()
  md = markdown.Markdown(extensions=['tables'])
  # md = markdown.Markdown(extensions=['tables', 'markdown_checklist.extension'])
  # [Third Party Extensions · Python-Markdown/markdown Wiki](https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions)
  content_html = md.convert(text_markdown)
  message.attach(MIMEText(content_html, "html"))
  return message

def whether_send_or_not(content):
  if "- [ ] " in content:
    return True
  else:
    return False  


def main():
  # initialize
  load_dotenv('./.env')
  path_md_file = os.environ['PATHMDFILE']
  from_address = os.environ['FROMADDRESS']
  to_address = os.environ['TOADDRESS']
  app_pass = os.environ['GOOGLEAPPPASSWORD']

  # prepare smtp object
  smtp_server = "smtp.gmail.com"
  sender = smtplib.SMTP_SSL(smtp_server)
  login_name = from_address
  sender.login(login_name, app_pass)

  # load a markdown file 
  title_md = os.path.splitext(os.path.basename(path_md_file))[0]
  text_markdown_lines = []
  for line in reversed(readlines_md_file(path_md_file)):
    if whether_send_or_not(line):
      text_markdown_lines.append(line.replace("- [ ] ", ""))

  # make and send message 
  for line in text_markdown_lines:
    message = render_html_mail_content_from_md_file(line)
    message["FROM"]=from_address
    message["TO"]=to_address
    date_today = datetime.datetime.today().strftime("%Y-%m-%d")
    message["subject"]= date_today + " " + title_md
    sender.send_message(message)

if __name__ == "__main__":
  main()