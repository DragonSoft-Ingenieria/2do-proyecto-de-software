from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from aplicacion import views, errorViews
from ShareProf import settings
from django.conf.urls import include

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^index/$', views.index, name='index'),
    url(r'^course/$', views.CourseList.as_view()),
    url(r'^busca/$', views.busca,name='busca'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    #url(r'^users/(?P<format>[a-z0-9]+)/$', views.UserDetail.as_view()),
    #path(r'^take/(?P[0-9]+)/$', views.TakeList.as_view()),
    url(r'^tomados/$', views.TakeList.as_view()),
    url(r'^course/(?P<pk>\d+)$', views.CourseDetailView.as_view(template_name='details/course-detail.html'), name='course-detail'),
    url(r'^user/(?P<pk>\d+)$', views.UserDetailView.as_view(template_name='details/user-detail.html'), name='user-detail'),
    url(r'^crearClase/$', views.crearClase, name='crearClase'),
    path('profesor/', TemplateView.as_view(template_name='teacherMode/profesor.html'),name='modoProfesor'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
handler404 = errorViews.noEncontrado
