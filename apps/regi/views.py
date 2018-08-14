from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, ("regi/index.html"))

def success(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        id=request.session["user_id"]
        return render(request, ("regi/success.html"), {"stuff":User.objects.get(id=id)})

def register(request):
    if request.method =="POST":
        errors = User.objects.validator(request.POST)
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']

        EmailExists= User.objects.filter(email=request.POST['email'])
        if not len(EmailExists) == 0:
            print("email exists error")
            messages.error(request, "Email " + request.POST['email'] + " is already registered")
            return redirect('/')

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            pwhashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

            User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pwhashed) 
            messages.success(request, "Successfully added")
            request.session.clear()
            return redirect('/')
    return redirect("/")

def login(request):
    if request.method =="POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email = email)
            if user:
                if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                    id= user.id
                    messages.success(request, "Login Success")
                    request.session['user_id'] = id
                    return redirect('/success')
                else:
                    messages.error(request, "Login Fail")
                    return redirect("/")
        except:
            messages.error(request, "Login Fail")
            return redirect("/")
    return redirect("/")

def clear(request):
    request.session.clear()
    print("Session Cleared")
    messages.success(request, "Session Cleared")
    return redirect ("/")