# coding: utf-8
__author__ = 'root'
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(msg):
    name, addr = parseaddr(msg)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


class SendMail(object):
    def __init__(self):
        """
        __init__
        :return:
        """
        self.smtp_serv = "smtp.sina.com"
        self.from_addr = "xyznoogel@sina.com"
        self.from_pass = "xyznoogel123"
        self.server = smtplib.SMTP(self.smtp_serv, 25)
        self.server.login(self.from_addr, self.from_pass)

    def send_message(self, title, content, to_list=None):
        """
        send_message
        :param title:
        :param content:
        :param to_list:
        :return:
        """
        if not to_list:
            to_list = ["noogel@163.com"]

        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = _format_addr(u'xyz通知帐号 <%s>' % self.from_addr)
        msg['To'] = _format_addr(u'接收账户 <%s>' % ",".join(to_list))
        msg['Subject'] = Header(title.decode("utf-8"), 'utf-8').encode()
        self.server.sendmail(self.from_addr, to_list, msg.as_string())

notifyer = SendMail()

if __name__ == "__main__":
    notifyer.send_message("测试邮件", "如题，今天的商品连接转换成功!")