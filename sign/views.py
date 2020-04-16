from django.shortcuts import render,HttpResponse,redirect
from .models import User
import bcrypt


def index(request):
    return render(request,'index.html')


def register(request):
    errors=User.objects.validator(request.POST)
    if len(errors):
        for tag,error in error.iteritems():
            messages.error(request,error,extra_tags=tag)
        return redirect('/')

    hashed_password=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
    user=User.objects.create(username=request.POST['username'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],password=hashed_password,email=request.POST['email'])
    user.save()
    request.session['id']=user.id
    return redirect('/success')

def success(request):
    user=User.objects.get(id=request.session['id'])
    context={
        "user":user
    }
    return render(request,context)