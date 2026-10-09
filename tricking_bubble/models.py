from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Utente(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32, unique=True)
    mail = models.EmailField(max_length=254)
    data_nascita = models.DateField(null=True, blank=True)
    foto_profilo = models.ImageField(upload_to='foto_utenti', blank=True)

    def __str__(self):
        return f"Utente: {self.user}"

    class Meta:
        ordering = ['user_id']
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'

class Trick(models.Model):
    nome = models.CharField(default="", max_length=32)
    categoria = models.IntegerField(default=0)
    media_difficolta = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    descrizione = models.CharField(max_length=1024)
    foto = models.ImageField(upload_to='foto_salti/', default="")
    link_1 = models.CharField(max_length=128, default="", blank=True, null=True)
    link_2 = models.CharField(max_length=128, default="", blank=True, null=True)
    link_3 = models.CharField(max_length=128, default="", blank=True, null=True)

    def __str__(self):
        return f"Trick: {self.nome} | Categoria: {self.categoria}"

    def get_media(self):
        progressioni = list(Progression.objects.filter(salto=self.id))
        somma = 0
        nValori = 0
        for p in progressioni:
            if p.valutazione == 0:
                continue
            somma += p.valutazione
            nValori += 1
        media = str(somma/nValori if nValori > 0 else 0)
        return f"{nValori}|{media}" 

    class Meta:
        verbose_name = 'Trick'
        verbose_name_plural = 'Tricks'

class Progression(models.Model):
    salto = models.ForeignKey(Trick, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Utente, on_delete=models.CASCADE)                            # da vedere
    completato = models.BooleanField(default=False)
    valutazione = models.IntegerField(default=0)

    def __str__(self):
        return f"Progression: {self.salto} - {self.user_id} - {self.valutazione}"

    class Meta:
        verbose_name = 'Progresso'
        verbose_name_plural = 'Progressi'

class Comment(models.Model):
    salto = models.ForeignKey(Trick, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Utente, to_field="nickname", on_delete=models.CASCADE )       # da vedere
    testo = models.CharField(max_length=1024)

    def __str__(self):
        return f"Commento: {self.salto} - {self.user_id}"

    class Meta:
        verbose_name = 'Commento'
        verbose_name_plural = 'Commenti'
