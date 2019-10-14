from aplicacion.models import Profile, Course, Take
from aplicacion.serializers import UserSerializer, CourseSerializer, TakeSerializer
from rest_framework import generics
from django.contrib.auth import logout
from django.contrib import messages
from aplicacion.forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TakeList(generics.ListCreateAPIView):
    queryset = Take.objects.all()
    serializer_class = TakeSerializer


class TakeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Take.objects.all()
    serializer_class = TakeSerializer

@login_required
def contactoEmail(request):
    if request.method == 'POST':
        formulario = Formulario(request.POST)
        if formulario.is_valid():
            asunto = 'Confirmacion de asesoria'
            mensaje = formulario.cleaned_data['mensaje']
            mail = EmailMessage(asunto,mensaje,to=['panlocastellanos@gmail.com'])
            mail.send()
            #send_mail('subject', 'body of the message', 'panlocastellanos@gmail.com', ['panlocastellanos@gmail.com',])
            messages.success(request, 'La asesoria ha sido solicitada, espera una respuesta')
            return redirect('contactoEmail')
        return HttpResponseRedirect('/')
    else:
        formulario = Formulario()
    return render(request, 'contacto_mail.html', {'formulario': formulario})


"""def signup(request):
    if request.method == 'POST':
        form1 = SignUpForm(request.POST)
        form2 = ProfileForm(request.POST, request.FILES)
        if form2.is_valid() and form1.is_valid():
            form1.save()
            username = form1.cleaned_data.get('username')
            usuario = User.objects.all().get(username=username)
            form2 = ProfileForm(request.POST, instance=usuario.profile)
            form2.save()
            raw_password = form1.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form1 = SignUpForm()
        form2 = ProfileForm()
    return render(request, 'registration/signup.html', {'form1': form1,'form2':form2})


"""

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()#commit=False)
            return render(request, 'index.html')
            #user.is_active = False
            #current_site = get_current_site(request)
            #mail_subject = 'Activate your blog account.'
            #message = render_to_string('registration/acc_active_email.html', {
            #    'user': user,
            #    'domain': current_site.domain,
            #    'uid':urlsafe_base64_encode(force_bytes(user.pk)),#.decode(),
            #    'token':account_activation_token.make_token(user),
            #})
            #to_email = form.cleaned_data.get('email')
            #email = EmailMessage(
            #    mail_subject, message, to=[to_email]
            #)
            #email.send()
            #return HttpResponse('Por favor confirma tu correo para completar el registro')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Gracias por confirmar, ahora puedes ingresar.')
    else:
        return HttpResponse('Código de activación inválido')

def logout_view(request):
    logout(request)
    return render(request, 'index.html')


def index(request):
    return render(request, 'index.html')

def busca(request):
    toSearch = request.GET['busqueda']
    if not toSearch:
        return HttpResponse("return this string")

    searchResult = Course.objects.filter(title__icontains=toSearch)
    return render(request, 'resultados.html', {'resultados': searchResult})


class CourseDetailView(DetailView):
    model = Course


class UserDetailView(DetailView):
    model = User

#@user_passes_test(lambda u: u.has_perm('aplicacion.is_teacher'))
@login_required
def modoProfesor(request):
    current_user = request.user
    searchResult = Course.objects.filter(teacher=current_user.profile.id)
    return render(request,'teacherMode/profesor.html', {'resultados': searchResult})


#@user_passes_test(lambda u: u.has_perm('aplicacion.is_teacher'))
#@login_required
def aceptar(request, key):
    taken = Take.objects.filter(course=key)
    aceptadas = set()
    no_aceptadas = set()
    for t in taken:
        s = User.objects.get(profile=t.student)
        print(s.first_name + ' ' + str(t.aceptada))
        if t.aceptada:
            aceptadas.add((s, t))
        else:
            no_aceptadas.add(s)
    return render(request,
                  'teacherMode/accept.html',
                  {'aceptadas': aceptadas,
                   'no_aceptadas': no_aceptadas,
                   'num_resultados': len(aceptadas) + len(no_aceptadas),
                   'clase': key})


@login_required
def enviarAviso(request,key,clase):
     user = User.objects.get(pk=key)
     current_user = request.user
     tomado = Take()
     tomado.student = current_user.profile
     tomado.course = Course.objects.get(pk=clase)
     tomado.save()
     mail = EmailMessage('Confirmacion de asesoria','Han solicitado una de tus asesorias',to=[user.email])
     mail.send()
     return render(request, 'CorreoAviso.html')

@login_required
def enviarAviso2(request,key,clase):
    user = User.objects.get(pk=key)
    taken = Take.objects.get(student=user.profile,course=clase)
    taken.aceptada = True
    taken.save()
    mail = EmailMessage('Confirmacion de asesoria','Te han aceptado en una asesoría',to=[user.email])
    mail.send()
    return render(request, 'AceptaAviso.html')

@login_required
def tomarClase(request):
    if request.GET.get('clase'):
        id_clase = request.GET.get('clase')
        current_user = request.user
        tomado = Take()
        tomado.student = current_user.profile
        tomado.course = Course.objects.get(pk=id_clase)
        tomado.save()
    return redirect('index')


@login_required
def crearClase(request):
    form = CrearClaseForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_user = request.user
            new_teacher = form.save(commit=False)
            usuario = current_user.profile
            new_teacher.teacher = usuario
            new_teacher.save()
            messages.success(request, 'Clase creada exitosamente')
            return redirect('crearClase')
        else:
            form = CrearClaseForm()
    return render(request, 'teacherMode/crearClase.html', {'form': form})


@login_required
def edit_account(request):
    u = request.user
    profile = u.profile
    if request.method == 'POST':
        POST = request.POST.copy()
        POST['username'] = u.username # No se puede cambiar el username y django no rellena este campo automágicamente
        form1 = EditUserForm(POST, instance=u)
        form2 = ProfileForm(POST, request.FILES, instance=profile)
        if form2.is_valid() and form1.is_valid():
            form1.save()
            form2.save()
            u.set_password(form1.cleaned_data.get('password1'))
            if form1.cleaned_data.get('password1'):
                u.save()
            return redirect('edit-account')
    else:
        form1 = EditUserForm(instance=u)
        form2 = ProfileForm(instance=profile)
    return render(request, 'registration/edit-account.html', {'form1': form1, 'form2': form2})


@login_required
def rate_user(request, user_id, take_id):
    try:
        user_r = User.objects.get(pk=user_id)
        take = Take.objects.get(pk=take_id)
        course = Course.objects.get(pk=take.course_id)
    except User.DoesNotExist or Take.DoesNotExist or Course.DoesNotExist:
        return redirect('index')
    if request.user.id != course.teacher_id:
        return redirect('index')

    form = RatingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('edit-account')
    else:
        form = RatingForm(auto_id=False)
    return render(request, 'rating.html', {'form': form})


# Create your views here.
