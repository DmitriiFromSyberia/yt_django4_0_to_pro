from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


# Create your views here.
def index(request):
    items = Product.objects.all()
    # return HttpResponse(items)
    context = {"items": items}
    return render(request, "myapp/index.html", context)


def indexItem(request, my_id):
    item = Product.objects.get(id=my_id)
    # return HttpResponse('Your item id is:'+ str(my_id))
    context = {"item": item}
    return render(request, "myapp/detail.html", context)


# def contacts (request):
#     return render(request,'myapp/contacts.html')
