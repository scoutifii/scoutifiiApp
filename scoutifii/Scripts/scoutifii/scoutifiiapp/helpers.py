import os
import magic
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
import uuid
from twilio.rest import Client

def validate_is_video(file):
    valid_mime_types = ['video/mp4', 'video/webm', 'video/ogg', 'video/mkv', 'video/avi', 'video/m4v', 'video/wmv']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.mp4', '.webm', '.ogg', '.mkv', '.avi', '.m4v', '.wmv']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')


def send_forgot_password_mail(email, token):
    subject = 'You forgot password link'
    message = 'Hi, click on the link to reset your password http://127.0.0.1/change-password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def validate_file_size(value):
    filesize = value.size
    if filesize > 10485760:
        raise ValidationError("File exceeded limit of 10Mb")
    else:
        return value


class MessageHandler:
    phone_number=None
    otp=None
    def __init__(self,phone_number,otp) -> None:
        self.phone_number=phone_number
        self.otp=otp
    def send_otp_via_message(self):     
        client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        message=client.messages.create(body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_PHONE_NUMBER}',to=f'{settings.COUNTRY_CODE}{self.phone_number}')
    def send_otp_via_whatsapp(self):     
        client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        message=client.messages.create(body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_WHATSAPP_NUMBER}',to=f'whatsapp:{settings.COUNTRY_CODE}{self.phone_number}')
