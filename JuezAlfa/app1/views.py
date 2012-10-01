import mimetypes
import os
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
#para la autentificacion
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import *
from app1.models import Concurso, Problema, Equipo, Equipo_Problema
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth.decorators import login_required
import datetime
#@login_required
def home(request):
    if request.user.is_authenticated():# para no poder ingresar sin loguearse
        return render_to_response('home/principal.html', {}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def registro(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        codigo = request.POST.get('codigo')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.create(first_name=nombre, email=email, username=codigo)
        user.set_password(password)
        user.save()
        
        equipo = Equipo(userEquipo=user)
        equipo.save()
        return render_to_response('home/Registro_exito.html', {'user': user}, context_instance=RequestContext(request))
    else:
        return render_to_response('home/registro.html', context_instance=RequestContext(request))


def loguearse(request):
    if not request.user.is_anonymous():
        return render_to_response('home/principal.html', {}, context_instance=RequestContext(request))

    if request.method == "POST":
        username = request.POST.get('codigo')
        password = request.POST.get('pass')

        auth = authenticate(username=username, password=password)# verificamos si los datos son correcto

        if auth:
            login(request, auth)
            return render_to_response('home/principal.html', {}, context_instance=RequestContext(request))
        else:
            return render_to_response('home/login.html', {}, context_instance=RequestContext(request))
    else:
        return render_to_response('home/login.html', {}, context_instance=RequestContext(request))


def desloguearse(request):
    logout(request)
    return HttpResponseRedirect('/')#evitamos el error de redirect()


def concursos(request):
    if request.user.is_authenticated():# para no poder ingresar sin loguearse
        objeto = Concurso.objects.all()

        return render_to_response('home/concursos.html', {'Concursos': objeto}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def problemas(request):
    return render_to_response('sin_usar/problemas.html', context_instance=RequestContext(request))


def division(request):
    if request.user.is_authenticated():# para no poder ingresar sin loguearse
        id_concurso = request.GET.get('concurso', '')
        id_problema = request.GET.get('problema', '')
        concurso = Concurso.objects.filter(id=id_concurso)
        problemas = Problema.objects.filter(concurso=concurso)

        now = datetime.datetime.now()
        #fecha = now.strftime("%Y%m%d%H%M%S")
        concursoInicio = concurso[0].inicio
        concursoFinal = concurso[0].fin
        #fechaConcursoInicio = concursoInicio.strftime("%Y%m%d%H%M%S")
        #fechaConcursoFinal = concursoFinal.strftime("%Y%m%d%H%M%S")

        #fechaRealInicio=int(fechaConcursoInicio)-50000 #se resta 5 horas, xk en el SAD con lo que muestra la consola, la diferencia es de 5 horas
        #fechaRealFinal=int(fechaConcursoFinal)-50000#con esto ya no tendremos problemas con el adminstrador

        band=False
        if concursoInicio<now and now<concursoFinal:
            band=True

        #print band
        return render_to_response('home/division.html', {'problemas': problemas, 'concurso_id': id_concurso,'fecha':band},
            context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def problemas_concurso(request):
    if request.user.is_authenticated():# para no poder ingresar sin loguearse
        if request.method == "POST" and request.is_ajax():
            try:
                id_concurso = request.POST.get('concurso', '')
                id_problema = request.POST.get('problema', '')
                tituloProblema = request.POST.get('titulo','')#con esto cargo el archivo de salida, el cual debe tener el mismo nombre del problema

                listaProblemas = Problema.objects.filter(id=id_problema)#para mostrar la lista de poblemas despues de elegir el concurso
                objetoProblema = Problema.objects.get(id=id_problema)#obtenemos un objeto que tiene (una fila que contiene ese id)

                if request.FILES.get('archivo'):
                    archivo1 = request.FILES.get('archivo')#cargo el archivo del concursante, no importa con que nombre me envie
                    linea1 = archivo1.readline()

                    band = True

                    archivo2 = open('SalidaAdministrador/'+tituloProblema+'.out','r')
                    linea2 = archivo2.readline()

                    c=0 #contador para indicar si hay algun error, mostrarle en que caso esta la falla
                    while linea1 != "":
                        c=c+1
                        #
                        if linea1 != linea2:
                            band = False
                            break
                        linea1 = archivo1.readline()
                        linea2 = archivo2.readline()
                    archivo1.close()
                    archivo2.close()

                    #insertar a la base de datos el resultado del problema del concurso del participante
                    ep=Equipo_Problema.objects.filter(problema=objetoProblema, equipos=Equipo.objects.get(userEquipo=request.user))

                    '''
                        Este filtro tiene que ser exacto para que la lista tenga solo un elemento, en este filtro estamos
                        seleccionando que el problema sea igual al problema que tenga el id del problema que estamos enviando
                        la solucion, y el usuario que actualmente esta activo, con eso se espera una lista solo un registro (elemento)
                    '''
                    puntos=0
                    if band:
                        if len(ep)==0:
                            puntos=puntos+1
                            Equipo_Problema.objects.create(problema=objetoProblema,equipos=Equipo.objects.get(userEquipo=request.user), resultado=1,puntaje=puntos,fecha=datetime.datetime.now())
                        elif len(ep)==1:
                            if ep[0].resultado==0:
                                ep[0].resultado=1
                                ep[0].puntaje=ep[0].puntaje+1
                                ep[0].fecha=datetime.datetime.now()
                                ep[0].save()
                        return render_to_response('problemas/resultado.html',{'status':1,'problemas': listaProblemas, 'concurso_id': id_concurso}, context_instance=RequestContext(request))
                        #return render_to_response('problemas/problema.html', {'problemas': listaProblemas, 'concurso_id': id_concurso,'status':1},context_instance=RequestContext(request))
                    else:
                        if len(ep)==0:
                            Equipo_Problema.objects.create(problema=objetoProblema,equipos=Equipo.objects.get(userEquipo=request.user), resultado=0,puntaje=0)
                        #return render_to_response('problemas/problema.html', {'problemas': listaProblemas, 'concurso_id': id_concurso,'status':0},context_instance=RequestContext(request))
                        return render_to_response('problemas/resultado.html',{'status':0,'problemas': listaProblemas, 'concurso_id': id_concurso,'lineaError':c}, context_instance=RequestContext(request))
            except Exception, ex:
                print ex
        else:
            print "entro por get"
            id_concurso = request.GET.get('concurso', '')
            id_problema = request.GET.get('problema', '')
            tituloProblema = request.GET.get('titulo','')#con esto cargo el archivo de salida, el cual debe tener el mismo nombre del problema
            listaProblemas = Problema.objects.filter(id=id_problema) #para mostrar la lista de poblemas despues de elegir el concurso
            objetoProblema = Problema.objects.get(id=id_problema)#obtenemos un objeto que tiene (una fila que contiene ese id)
            return render_to_response('problemas/problema.html', {'problemas': listaProblemas, 'concurso_id': id_concurso},
            context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect('/')

def submit_solution(request):#ya no es necesario, no se esta usando
    if request.method == "POST":
        if request.POST.get('problema') and request.FILES.get('archivo'):
            archivo = request.FILES.get('archivo')
            linea = archivo.readline()

            while linea != "":
                print linea
                linea = archivo.readline()
            archivo.close()
            #nombre_problema = request.POST.get('problema')

            #path = default_storage.save(request.FILES.get('archivo').name, request.FILES.get('archivo'))#para guardar en una carpeta
    return render_to_response('problemas/submit.html', context_instance=RequestContext(request))

def ranking(request):
    #hay un problema cuando el equipo hace otra pregunta se inserta en la tabla como nuevo registro, se debe actualizar la fila
    id_concurso = request.GET.get('concurso', '')#para que funcione el link de problemas
    equipos = Equipo_Problema.objects.order_by("puntaje")
    return render_to_response('problemas/ranking.html', {'equipos':equipos,'problemas': problemas, 'concurso_id': id_concurso},context_instance=RequestContext(request))

def registroEnvios(request):
    id_concurso = request.GET.get('concurso', '')#para que funcione el link de problemas de nav
    equipos = Equipo_Problema.objects.order_by("-fecha")
    return render_to_response('problemas/RegistroEnvios.html', {'equipos':equipos, 'problemas': problemas, 'concurso_id': id_concurso},context_instance=RequestContext(request))

def downloadFile(request):
    id_problema= request.GET.get('id_problema','')
    if id_problema!='':
        problema= Problema.objects.get(id=id_problema)
    filename=problema.titulo
    file = open("Entradas/"+filename+".in","r")
    mimetype = "application/octet-stream"
    response = HttpResponse(file.read(), mimetype=mimetype)
    response['Content-Disposition'] = 'attachment; filename={}'.format(problema.titulo)
    return response


