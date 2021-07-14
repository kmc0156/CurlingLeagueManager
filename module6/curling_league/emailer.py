import yagmail


class Emailer:
    """SINGLETON"""
    _sole_instance = None
    sender_address = ""

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def configure(cls, sender_address):
        cls.sender_address = sender_address

    def send_plain_email(self, recipients, subject, message):
        "instance method"
        try:
            yagmail.SMTP(user='KevinCarterAuburn').send(to=recipients, subject=subject, contents=message)
            print("Email sent successfully")
        except:
            print("Error, email was not sent")