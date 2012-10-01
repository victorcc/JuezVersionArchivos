from django.db import models
from django.contrib.auth.models import User

#class Estudiante(models.Model):
#nombre = models.CharField(max_length=100)
#apellido = models.CharField(max_length=100)
#email = models.CharField(max_length=100)
#password = models.EmailField()
#    user = models.ForeignKey(User)

class Equipo(models.Model):
    userEquipo = models.OneToOneField(User, related_name='equipo')

    def __unicode__(self):
        return self.userEquipo.first_name

        #integrantes = models.ManyToManyField(Estudiante)
    def get_problemas_bien(self):
        return [p.problema for p in self.equipo_problemas.filter(resultado=1)]
    def get_problemas_mal(self):
        return [p.problema for p in self.equipo_problemas.filter(resultado=0)]


class Concurso(models.Model):
    nombre = models.CharField(max_length=100)
    duracion = models.IntegerField()
    inicio = models.DateTimeField()
    fin = models.DateTimeField() #too: fin = inicio+duracion
    disponibilidad = models.BooleanField()

    def __unicode__(self):
        return self.nombre


class Problema(models.Model):
    titulo = models.CharField(max_length=50)
    enunciado = models.TextField()
    entrada = models.FileField(upload_to="Entradas/")
    entradaEjemplo = models.CharField(max_length=400)
    salida = models.FileField(upload_to="SalidaAdministrador/")
    salidaEjemplo = models.CharField(max_length=400)
    codigo = models.CharField(max_length=20)
    peso = models.IntegerField()
    concurso = models.ForeignKey(Concurso)

    def __unicode__(self):
        return self.titulo


class Administrador(models.Model):
    userAdmin = models.ForeignKey(User)
    nombre = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    concursos = models.ManyToManyField(Concurso)


class Concurso_Equipo(models.Model):
    equipo = models.ForeignKey(Equipo)
    concurso = models.ForeignKey(Concurso)

#class Concurso_Integrante(models.Model):
#    estudiantes = models.ForeignKey(Estudiante)
#    concursos = models.ForeignKey(Concurso)


#class Integrante_Problema(models.Model):
#    problema = models.ForeignKey(Problema)
#    estudiantes = models.ForeignKey(Estudiante)


class Equipo_Problema(models.Model):
    problema = models.ForeignKey(Problema)
    equipos = models.ForeignKey(Equipo, related_name='equipo_problemas')
    resultado = models.IntegerField() #1=AC, 2 = WA, 0=- (sin resolver)
    puntaje = models.IntegerField()#para el ranking
    fecha = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        #return '%s %s %s %s' % (self.equipos.userEquipo.first_name, self.problema.titulo, self.resultado, self.fecha)
        return '%s %s %s' % (self.equipos.userEquipo.first_name, self.problema.titulo, self.resultado)

        #class Tipo_Administrador(models.Model):
#    administrador = models.ForeignKey(Administrador)
