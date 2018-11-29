from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import DateInput
from django.forms.widgets import NumberInput
from aplicacion.models import Profile, Take
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from aplicacion.models import Course
from django.utils.html import escape
from django.utils.safestring import mark_safe


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
    CHOICES = (
        ('eng', 'Inglés'),
        ('esp', 'Español'),
        ('syr', 'Sirio'),
    )
    profile_pic = forms.ImageField(label='Imagen de perfil', widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    language = forms.ChoiceField(label='Idioma', widget=forms.Select, choices=CHOICES)
    birthdate = forms.DateField(label='Fecha de nacimiento', widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ('language', 'birthdate', 'profile_pic')


class EditUserForm(forms.ModelForm):
    password1 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control', 'disabled': ''}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(EditUserForm, self).clean()
        pwd1 = cleaned_data.get('password1')
        pwd2 = cleaned_data.get('password2')
        if pwd1 != pwd2:
            self._errors['password2'] = self.error_class(['Las contraseñas no son iguales.'])
            del self.cleaned_data['password2']
        return cleaned_data


class Formulario(forms.Form):
    correo = forms.EmailField()
    mensaje = forms.CharField()


class CrearClaseForm(forms.ModelForm):
    CHOICES = (
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Noctuno', 'Nocturno'),
    )

    CHOICES2 = (
        ('Preescolar', 'Preescolar'),
        ('Primaria', 'Primaria'),
        ('Secundaria', 'Secundaria'),
        ('Preparatoria', 'Preparatoria'),
        ('Licenciatura', 'Licenciatura'),
        ('Maestria', 'Maestria'),
    )

    horario = forms.ChoiceField(label='Horario',widget=forms.Select, choices=CHOICES)
    level = forms.ChoiceField(label='Nivel',widget=forms.Select, choices=CHOICES2)
    class Meta:
        model = Course
        exclude = ['teacher']
        fields = ('id', 'title', 'description', 'level','horario','precio')
        widgets = {
            # 'teacher' : forms.Select(attrs={'class' : 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el nombre de la asesoria'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            #'level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el nivel de la asesoria'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el precio de la asesoria'}),

        }

        labels = {
            # 'teacher': _('Profesor'),
            'title': _('Titulo'),
            'description': _('Descripcion'),
            #'level': _('Nivel'),
            'precio':_('Precio'),
            #'horario': _('Horario'),
        }


class RatingForm(forms.ModelForm):
    CHOICES = (
        (1, 'One'),
        (2, 'Two'),
        (3, ''),
    )
    rate = forms.ChoiceField(label='Rad', widget=forms.RadioSelect, choices=CHOICES)
    rate5 = forms.ChoiceField(label='', widget=forms.RadioSelect, choices=[(5, 'Five')])

    class Meta:
        model = Take
        fields = ('student_rating', 'teacher_rating', 'rate', 'rate5')
