from django.shortcuts import render


def noEncontrado(request, exception):
    return render(request,'errorViews/noEncontrado.html')

