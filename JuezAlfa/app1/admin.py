__author__ = 'wilson'
from django.contrib import admin
from app1.models import Equipo, Concurso, Problema, Concurso_Equipo, Equipo_Problema, User

#admin.site.register(Estudiante)
admin.site.register(Equipo)
admin.site.register(Problema)
admin.site.register(Concurso)
#admin.site.register(Administrador)
admin.site.register(Concurso_Equipo)
admin.site.register(Equipo_Problema)

#admin.site.register(Concurso_Integrante)
#admin.site.register(Integrante_Problema)