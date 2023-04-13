from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Response
from django.core.mail import send_mail


@receiver(pre_save, sender=Response)
def notif_about_response(sender, instance, **kwargs):
    if instance.response_status:
        mail = instance.sender.email
        send_mail(
            subject='Отклик!',
            message=f'{sender}, Ваш отклик принят!',
            from_email=None,
            recipient_list=[mail],
            fail_silently=False

        )
    else:

        mail = instance.responseAdvert.username.email
        send_mail(
            subject='Отклик!',
            message=f'{instance.responseAdvert.username}, Вы получили отклик на Ваше объявление!',
            from_email=None,
            recipient_list=[mail],
            fail_silently=False
        )




