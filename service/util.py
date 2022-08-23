import yagmail

from config.config import settings

EMAIL = settings.admin_email
PASSWORD = settings.password_email


def send_mail(addressee: str, subject: str, text: str): 
    try:
        yag = yagmail.SMTP(user=EMAIL, password=PASSWORD)              
        yag.send(
            to=addressee,
            subject=subject,
            contents=text           
        )
        print("e-mail enviado correctamente!")
    except Exception as e:
        print(e)