from django.core.mail import send_mail
from django.conf import settings

def send_password_reset_mail(email, token):
    subject = "ToDoApp | Reset you account password"
    message = f'Hello,\n\nPlease click on the following link to reset your password:\nPassword Reset Link: https://todoapp-z1cn.onrender.com/reset-password/?token={token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
