from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Utente)
admin.site.register(Trick)
admin.site.register(Progression)
admin.site.register(Comment)