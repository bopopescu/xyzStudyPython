# coding: utf-8
__author__ = 'root'
import smtplib
import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from conf.settings import MAIL_CONF


def _format_addr(msg):
    name, addr = parseaddr(msg)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


class SendMail(object):
    """
    SendMail
    """
    def __init__(self):
        """
        __init__
        :return:
        """
        self.smtp_serv = MAIL_CONF["server"]
        self.from_addr = MAIL_CONF["user"]
        self.from_pass = MAIL_CONF["pass"]
        self.server = smtplib.SMTP(self.smtp_serv, 25)

    def __enter__(self):
        """
        __enter__
        :return:
        """
        self.server.login(self.from_addr, self.from_pass)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.server.quit()


    def _to_charset(self, text, from_charset='utf-8', to_charset='utf-8'):
        """
        _to_charset
        :param text:
        :param from_charset:
        :param to_charset:
        :return:
        """
        if from_charset == to_charset:
            return text
        return text.decode(from_charset).encode(to_charset)

    def send_message(self, title, content, to_list=None, attach_list=None, charset='utf-8'):
        """
        send_message
        :param title:
        :param content:
        :param to_list:
        :return:
        """
        if not to_list:
            to_list = ["noogel@163.com"]

        msg = MIMEMultipart("mixed")
        msg["From"] = _format_addr(u'xyz通知帐号 <%s>' % self._to_charset(self.from_addr, to_charset=charset))
        msg["To"] = self._to_charset(",".join(to_list), to_charset=charset)
        msg["Subject"] = Header(title.decode("utf-8"), charset).encode()
        msg.attach(MIMEText(self._to_charset(content, to_charset=charset), "plain", charset))
        if attach_list:
            for attach in attach_list:
                part = self.build_attach_part(
                    attach[0], attach[1], attach[2], charset)
                msg.attach(part)
        self.server.sendmail(self.from_addr, to_list, msg.as_string())

    def build_attach_part(self, file_path_or_content, file_name, mimetype, charset):
        """构建纯文本的

        Args:
            file_path: path or content
            file_name: 文件名称
            mimetype: miemtype
        """
        content = file_path_or_content
        if not mimetype:
            mimetype, _ = mimetypes.guess_type(file_name)
        if not mimetype:
            mimetype = "application/octet-stream"
        type_maj, type_min = mimetype.split('/')
        if isinstance(file_path_or_content, str):
            with open(file_path_or_content, "rb") as f:
                content = f.read()
        elif isinstance(file_path_or_content, bytes):
            content = file_path_or_content
        else:
            content = content.getvalue()
        msg = MIMEBase(type_maj, type_min)
        msg.set_payload(content)
        encoders.encode_base64(msg)
        msg.add_header(
            "Content-Disposition",
            "attachment",
            filename=(charset, '', file_name)
        )
        return msg


# notifyer = SendMail()


if __name__ == "__main__":
    notifyer.send_message("测试邮件", "如题，今天的商品连接转换成功!")