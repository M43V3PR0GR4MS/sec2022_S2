from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from seguridad import settings
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, "auth/index.html")

def ecomm(request):
    return render(request, "auth/ecomm.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "El nombre de usuario ya está ocupado.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "El email ya está en uso!")
            return redirect('signup')
        
        if len(username)>20:
            messages.error(request, "Usuario no deben contener más de 20 caracteres!!")
            return redirect('signup')

        if len(username)<3:
            messages.error(request, "Usuario no deben contener mmenos de 3 caracteres!!")
            return redirect('signup')

        if len(pass1)<8:
            messages.error(request, "Contraseñas deben tener más de 8 caracteres!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Las contraseñas no son iguales!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Usuarios deben usar solo letras o numeros!!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Tu cuenta ha sido creada exitosamente.")

        return redirect('signin')

    return render(request, "auth/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            usern = user.username
            return render(request, "auth/index.html",{"usern":usern})
        else:
            messages.error(request, "Datos incorrectos")
            return redirect('home')

    return render(request, "auth/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Ha cerrado la sesión correctamente!!")
    return redirect('home')