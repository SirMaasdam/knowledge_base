from django.conf import settings

from knowledge_base.celery import app
from django.core.mail import send_mail


@app.task
def user_created(username, email):
    """Sending an email in case of successful registration"""

    subject = f'Регистрация в базе знаний'
    message = f'Уважаемый {username}, Вы зарегестрировались в базе знаний\n\n' \
              f'Желаем Вам получить ответ на все Ваши вопросы в нашем сервесе.\n\n' \
              f'Желаем вам удачи!'
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_HOST_USER,
                          [email])
    return mail_sent
