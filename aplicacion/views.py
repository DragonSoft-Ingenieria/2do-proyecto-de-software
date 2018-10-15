from django.contrib.auth import login
from django.http import HttpResponse
from aplicacion.models import Profile, Course, Take
from aplicacion.serializers import UserSerializer, CourseSerializer, TakeSerializer
from rest_framework import generics
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import login, authenticate
from aplicacion.forms import SignUpForm, CrearClaseForm, ProfileForm, EditUserForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import DetailView


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


def signup(request):
    if request.method == 'POST':
        form1 = SignUpForm(request.POST)
        form2 = ProfileForm(request.POST)
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

@login_required
def modoProfesor(request):
    return render(request,'teacherMode/profesor.html')

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
    return render(request, 'crearClase.html', {'form': form})

@login_required
def edit_account(request, pk):
    u = User.objects.get(id=pk)
    profile = u.profile
    if request.method == 'POST':
        POST = request.POST.copy()
        POST['username'] = u.username # No se puede cambiar el username y django no rellena este campo automágicamente
        form1 = EditUserForm(POST, instance=u)
        form2 = ProfileForm(POST, instance=profile)
        if form2.is_valid() and form1.is_valid():
            form1.save()
            form2.save()
            u.set_password(form1.cleaned_data.get('password1'))
            if form1.cleaned_data.get('password1'):
                u.save()
            return redirect('index')
    else:
        form1 = EditUserForm(instance=u)
        form2 = ProfileForm(instance=profile)
    return render(request, 'registration/edit-account.html', {'form1': form1, 'form2': form2})

# Create your views here.
