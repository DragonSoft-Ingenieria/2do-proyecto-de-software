from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import DateInput
from aplicacion.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from aplicacion.models import Course




class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Nombre de usuario', min_length=4, max_length=150)
    first_name = forms.CharField(label="Primer nombre",max_length=30, required=True)
    last_name = forms.CharField(label="Primer apellido",max_length=30, required=True )
    email = forms.EmailField(label="Ingrese un email",max_length=254)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma la contraseña', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields= ('language','birthdate')



class CrearClaseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['teacher']
        fields = ('id', 'title', 'description', 'level')
        widgets = {
            # 'teacher' : forms.Select(attrs={'class' : 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el nombre de la clase'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el nivel de la clase'}),

        }

        labels = {
            # 'teacher': _('Profesor'),
            'title': _('Titulo'),
            'description': _('Descripcion'),
            'level': _('Nivel'),
        }



