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
    CHOICES = (
        ('eng', 'Inglés'),
        ('esp', 'Español'),
        ('syr', 'Sirio'),
    )
    language = forms.ChoiceField(widget=forms.Select, choices=CHOICES)

    class Meta:
        model = Profile
        fields= ('language','birthdate','profile_pic')


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
            print('cleaning')
            self._errors['password2'] = self.error_class(['Las contraseñas no son iguales.'])
            del self.cleaned_data['password2']
        return cleaned_data


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



