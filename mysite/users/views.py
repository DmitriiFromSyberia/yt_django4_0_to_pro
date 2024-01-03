from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import NewUserForm

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("myapp:index")
    form = NewUserForm()
    context = {"form": form}
    return render(request, "users/register.html", context)


def logout_view(request):
    logout(request)
    return render(request, "users/logout.html")

    # if request.method == "GET":
    #     # Ваш код для обработки GET-запроса
    #     logout(request)
    #     # return HttpResponse("You have been logout")
    #     return render(request, "users/logout.html")

    # else:
    #     # Ваш код для обработки других методов (например, POST)
    #     return HttpResponse("Метод не разрешен для данного URL")


@login_required
def profile(request):
    return render(request, "users/profile.html")

def seller_profile(request, id):
    seller=User.objects.get(id=id)
    
    context = {"seller": seller}
    return render(request, "users/sellerprofile.html", context)
