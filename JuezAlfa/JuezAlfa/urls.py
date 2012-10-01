from django.conf.urls import patterns, include, url
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app1.views.loguearse',name='vista_login'),

    url(r'^login/$', 'app1.views.loguearse',name='vista_login'),
    url(r'^judge/$', 'app1.views.home',name='vista_principal'),
    url(r'^registro/$', 'app1.views.registro',name='vista_registro'),

    url(r'^logout/$', 'app1.views.desloguearse'),
    url(r'^judge/concursos/$', 'app1.views.concursos',name='vista_concursos'),
    url(r'^judge/problemas/$', 'app1.views.problemas',name='vista_problemas'),
    url(r'^judge/concurso/$', 'app1.views.division',name='vista_division'),
    url(r'^judge/concurso/problema/$', 'app1.views.problemas_concurso',name='vista_problemas_concurso'),
    url(r'^judge/concurso/problema/resultado/$', 'app1.views.problemas_concurso',name='vista_problema_resultado'),
    url(r'^judge/concurso/problema/ranking/$', 'app1.views.ranking',name='vista_ranking'),
    url(r'^judge/concurso/problema/envios/$', 'app1.views.registroEnvios',name='vista_registroEnvios'),
    url(r'^judge/concurso/problema/downland/$', 'app1.views.downloadFile',name='vista_downland'),
    #url(r'^judge/concursos/solucion/$', 'app1.views.submit_solution',name='vista_solucion'),#no se esta usando
    #url(r'^judge/administrador/$', 'app1.views.vista_administrador',name='vista_administrador'),

    url(r'^admin/', include(admin.site.urls)),
)
