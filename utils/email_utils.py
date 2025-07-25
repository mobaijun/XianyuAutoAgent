import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime

# 邮件配置（可从环境变量读取）
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.163.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '465'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
TO_EMAIL = os.getenv('TO_EMAIL')

MAIL_SUBJECT = '【闲鱼AI客服】有新顾客消息 - {user_name} 咨询了商品！'

HTML_TEMPLATE = '''
<html>
  <body>
    <h2>有新顾客发来消息</h2>
    <ul>
      <li><b>用户名：</b>{user_name}</li>
      <li><b>商品标题：</b>{item_title}</li>
      <li><b>商品链接：</b><a href="{item_url}">{item_url}</a></li>
      <li><b>商品详情：</b>{item_desc}</li>
      <li><b>价格：</b>{item_price} 元</li>
      <li><b>消息内容：</b>{user_message}</li>
      <li><b>时间：</b>{msg_time}</li>
    </ul>
  </body>
</html>
'''

def send_customer_message_email(user_name, item_title, item_url, item_desc, item_price, user_message, msg_time=None):
    if msg_time is None:
        msg_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subject = MAIL_SUBJECT.format(user_name=user_name, item_title=item_title)
    html_content = HTML_TEMPLATE.format(
        user_name=user_name,
        item_title=item_title,
        item_url=item_url,
        item_desc=item_desc,
        item_price=item_price,
        user_message=user_message,
        msg_time=msg_time
    )
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False 