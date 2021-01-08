from django.db import models
from django.conf import settings
from django.urls import reverse


# Create your models here.

class Chat(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Пользователь №1', related_name='user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Пользователь №2', related_name='user2')
    # default_title = self.user1.nickname + self.user2.nickname
    title = models.CharField(max_length=150, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.title = 'Чат ' + self.user1.username + ' ' + self.user2.username
        super(Chat, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_chat', kwargs={"pk": self.pk})


class Message(models.Model):
    text = models.TextField(blank=True, verbose_name='Текст сообщения')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name='Отправитель', related_name='sender')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                  verbose_name='Получатель', related_name='recipient')
    dt_sending = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT, null=True, verbose_name='Чат')

    # def __str__(self):
    #     return 'Сообщение от ' + self.sender.username + ' ' + self.recipient.username + 'у в ' + str(self.dt_sending)