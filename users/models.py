# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Campi aggiuntivi rispetto al modello User standard
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    # Aggiunto per evitare conflitti con il campo email di AbstractUser
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'