# -*- coding: utf-8 -*-

import itertools

from logging import getLogger
logger = getLogger(__name__)

from config import CONFIG

def safestr(obj, encoding='utf-8'):
    r"""
    Converts any given object to utf-8 encoded string.

        >>> safestr('hello')
        'hello'
        >>> safestr(u'\u1234')
        '\xe1\x88\xb4'
        >>> safestr(2)
        '2'
    """
    if isinstance(obj, unicode):
        return obj.encode(encoding)
    elif isinstance(obj, str):
        return obj
    elif hasattr(obj, 'next'): # iterator
        return itertools.imap(safestr, obj)
    else:
        return str(obj)

    
def dictadd(*dicts):
    """
    Returns a dictionary consisting of the keys in the argument dictionaries.
    If they share a key, the value from the last argument is used.

        >>> dictadd({1: 0, 2: 0}, {2: 1, 3: 1})
        {1: 0, 2: 1, 3: 1}
    """
    result = {}
    for dct in dicts:
        result.update(dct)
    return result

    
def sendmail(from_address, to_address, subject, message, headers=None, **kw):
    """
    Sends the email message `message` with mail and envelope headers
    for from `from_address_` to `to_address` with `subject`.
    Additional email headers can be specified with the dictionary
    `headers.

    Optionally cc, bcc and attachments can be specified as keyword arguments.
    Attachments must be an iterable and each attachment can be either a
    filename or a file object or a dictionary with filename, content and
    optionally content_type keys.
    """
    attachments = kw.pop("attachments", [])
    mail = _EmailMessage(from_address, to_address, subject, message, headers, **kw)

    for a in attachments:
        if isinstance(a, dict):
            mail.attach(a['filename'], a['content'], a.get('content_type'))
        elif hasattr(a, 'read'): # file
            filename = os.path.basename(getattr(a, "name", ""))
            content_type = getattr(a, 'content_type', None)
            mail.attach(filename, a.read(), content_type)
        elif isinstance(a, basestring):
            f = open(a, 'rb')
            content = f.read()
            f.close()
            filename = os.path.basename(a)
            mail.attach(filename, content, None)
        else:
            raise ValueError, "Invalid attachment: %s" % repr(a)

    mail.send()

class _EmailMessage:
    def __init__(self, from_address, to_address, subject, message, headers=None, **kw):
        def listify(x):
            if not isinstance(x, list):
                return [safestr(x)]
            else:
                return [safestr(a) for a in x]

        subject = safestr(subject)
        message = safestr(message)

        from_address = safestr(from_address)
        to_address = listify(to_address)
        cc = listify(kw.get('cc', []))
        bcc = listify(kw.get('bcc', []))
        recipients = to_address + cc + bcc

        import email.Utils
        self.from_address = email.Utils.parseaddr(from_address)[1]
        self.recipients = [email.Utils.parseaddr(r)[1] for r in recipients]

        self.headers = dictadd({
          'From': from_address,
          'To': ", ".join(to_address),
          'Subject': subject
        }, headers or {})

        if cc:
            self.headers['Cc'] = ", ".join(cc)

        self.message = self.new_message()
        self.message.add_header("Content-Transfer-Encoding", "7bit")
        self.message.add_header("Content-Disposition", "inline")
        self.message.add_header("MIME-Version", "1.0")
        self.message.set_payload(message, 'utf-8')
        self.multipart = False

    def new_message(self):
        from email.Message import Message
        return Message()

    def attach(self, filename, content, content_type=None):
        if not self.multipart:
            msg = self.new_message()
            msg.add_header("Content-Type", "multipart/mixed")
            msg.attach(self.message)
            self.message = msg
            self.multipart = True

        import mimetypes
        try:
            from email import encoders
        except:
            from email import Encoders as encoders

        content_type = content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"

        msg = self.new_message()
        msg.set_payload(content)
        msg.add_header('Content-Type', content_type)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)

        if not content_type.startswith("text/"):
            encoders.encode_base64(msg)

        self.message.attach(msg)

    def prepare_message(self):
        for k, v in self.headers.iteritems():
            if k.lower() == "content-type":
                self.message.set_type(v)
            else:
                self.message.add_header(k, v)

        self.headers = {}

    def send(self):
        self.prepare_message()
        message_text = self.message.as_string()

        server = CONFIG['smtp']['host']
        port = CONFIG['smtp']['port']
        username = CONFIG['smtp']['username']
        password = CONFIG['smtp']['password']
        starttls = CONFIG['smtp']['starttls']

        import smtplib
        smtpserver = smtplib.SMTP(server, port)

        if starttls:
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()

        if username and password:
            smtpserver.login(username, password)

        smtpserver.sendmail(self.from_address, self.recipients, message_text)
        smtpserver.quit()

    def __repr__(self):
        return "<EmailMessage>"

    def __str__(self):
        return self.message.as_string()

if __name__ == "__main__":
    sendmail('p.o.roussel@free.fr', 'p.o.roussel@free.fr', 'Email de test', 'Envoi depuis le serveur domotique')

