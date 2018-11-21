from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from rest_framework.urlpatterns import format_suffix_patterns
from aplicacion import views, errorViews
from ShareProf import settings
from django.conf.urls import include

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.index, name='index'),
    url(r'^course/$', views.CourseList.as_view()),
    url(r'^busca/$', views.busca,name='busca'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^tomados/$', views.TakeList.as_view()),
    url(r'^course/(?P<pk>\d+)$', views.CourseDetailView.as_view(template_name='details/course-detail.html'), name='course-detail'),
    url(r'^user/(?P<pk>\d+)$', views.UserDetailView.as_view(template_name='details/user-detail.html'), name='user-detail'),
    url(r'^user/edit$', views.edit_account, name='edit-account'),
    url(r'^rate/(?P<user_id>\d+)/(?P<take_id>\d+)/$', views.rate_user, name='rate-user'),
    url(r'^crearClase/$', views.crearClase, name='crearClase'),
    url(r'^contactoEmail/$', views.contactoEmail, name='contactoEmail'),
    path('tomarClase', views.tomarClase,name='tomarClase'),
    url('enviarAviso/(?P<key>\d+)/(?P<clase>\d+)/$', views.enviarAviso,name='enviarAviso'),
    url('enviarAviso2/(?P<key>\d+)/(?P<clase>\d+)/$', views.enviarAviso2,name='enviarAviso2'),
    url('aceptar/(?P<key>\d+)/$', views.aceptar,name='aceptar'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('profesor/', views.modoProfesor,name='modoProfesor'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)

handler404 = errorViews.noEncontrado
