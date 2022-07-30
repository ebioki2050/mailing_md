import markdown
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from dotenv import load_dotenv

def read_md_file(path_md_file):
  text_markdown = ""
  with open(path_md_file, "r", encoding='UTF-8') as file:
    text_markdown = file.read()
    text_markdown = text_markdown.replace('- [ ] ', '- <input type="checkbox" name="checkbox2" value="checkbox"> ')
  return text_markdown
  
def render_html_mail_content_from_md_file(text_markdown):
  message = MIMEMultipart()
  md = markdown.Markdown(extensions=['tables'])
  # md = markdown.Markdown(extensions=['tables', 'markdown_checklist.extension'])
  # [Third Party Extensions · Python-Markdown/markdown Wiki](https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions)
  content_html = md.convert(text_markdown)
  message.attach(MIMEText(content_html, "html"))
  return message

def main():
  # initialize
  load_dotenv('./.env')
  path_md_file = os.environ['PATHMDFILE']

  # prepare smtp object
  smtp_server = "smtp.gmail.com"
  from_address = os.environ['FROMADDRESS']
  to_address = os.environ['TOADDRESS']
  login_name = from_address
  app_pass = os.environ['GOOGLEAPPPASSWORD']
  sender = smtplib.SMTP_SSL(smtp_server)
  sender.login(login_name, app_pass)

  # load a markdown file 
  title_md = os.path.splitext(os.path.basename(path_md_file))[0]
  text_markdown = read_md_file(path_md_file)

  # make and send message 
  message = render_html_mail_content_from_md_file(text_markdown)
  message["FROM"]=from_address
  message["TO"]=to_address
  date_today = datetime.datetime.today().strftime("%Y-%m-%d")
  message["subject"]= date_today + " " + title_md
  sender.send_message(message)

if __name__ == "__main__":
  main()