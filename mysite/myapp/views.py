from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    items = Product.objects.all()
    paginator = Paginator(items, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # return HttpResponse(items)
    context = {"page_obj": page_obj}
    return render(request, "myapp/index.html", context)


class ProductListView(ListView):
    model = Product
    template_name = "myapp/index.html"
    context_object_name = "items"
    paginate_by = 2


# def indexItem(request, my_id):
#     item = Product.objects.get(id=my_id)
#     # return HttpResponse('Your item id is:'+ str(my_id))
#     context = {"item": item}
#     return render(request, "myapp/detail.html", context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "myapp/detail.html"
    context_object_name = "item"


@login_required
def add_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES["upload"]
        seller = request.user
        item = Product(
            name=name, price=price, description=description, image=image, seller=seller
        )
        item.save()
    return render(request, "myapp/additem.html")


def update_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.description = request.POST.get("description")
        item.image = request.FILES.get("upload", item.image)
        item.save()
        return redirect("/myapp/")
    context = {"item": item}
    return render(request, "myapp/updateitem.html", context)


def delete_item(request, my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.delete()
        return redirect("/myapp/")
    context = {"item": item}
    return render(request, "myapp/deleteitem.html", context)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "myapp/deleteitem.html"
    success_url = "/myapp/"


# def contacts (request):
#     return render(request,'myapp/contacts.html')
