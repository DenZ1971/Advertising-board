from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from froala_editor.fields import FroalaField


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', default=None, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateField(blank=True, null=True)


class Advert(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    TANKS = 'TS'
    HILS = 'HL'
    MERCH = 'MH'
    DD = 'DD'
    GILDMISTERS = 'GM'
    QUESTGIV = 'QG'
    BLACKSMITHS = 'BS'
    TANNERS = 'TR'
    POTIONMAKERS = 'PM'
    SPELLMASTERS = 'SM'

    CATEGORY_CHOICES = (
        (TANKS, 'Танки'),
        (HILS, 'Хиллы'),
        (MERCH, 'Торговцы'),
        (DD, 'ДД'),
        (GILDMISTERS, 'Гилдмастеры'),
        (QUESTGIV, 'Квестгиверы'),
        (BLACKSMITHS, 'Кузнецы'),
        (TANNERS, 'Кожевники'),
        (POTIONMAKERS, 'Зельевары'),
        (SPELLMASTERS, 'Мастера заклинаний'),
        (GILDMISTERS, 'Гилдмастеры'),
    )
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=256)
    text = FroalaField()
    timeCreation = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('advert_detail', kwargs={'pk': self.pk})


class Response(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    responseAdvert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    response_status = models.BooleanField(default=False)
    timeCreation = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('response_detail', kwargs={'pk': self.pk})
