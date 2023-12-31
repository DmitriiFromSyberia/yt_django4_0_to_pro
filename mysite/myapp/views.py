import json
import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Product, OrderDetails


# Create your views here.
def index(request):
    page_obj = items = Product.objects.all()
    item_name = request.GET.get("search")
    if item_name != "" and item_name is not None:
        page_obj = items.filter(name__icontains=item_name)
    paginator = Paginator(page_obj, 2)
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
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["stripe_publishable_key"] = settings.STRIPE_PUBLISHABLE_KEY
        return context


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
# @csrf_exempt
# def create_checkout_session(request, id):
#     product = get_object_or_404(Product, pk=id)
#     stripe.api_key = settings.STRIPE_SECRET_KEY

#     checkout_session = stripe.checkout.Session.create(
#         # customer_email=request.user.email,
#         payment_method_types=["card"],
#         line_items=[
#             {
#                 "price_data": {
#                     "currency": "usd",
#                     "product_data": {
#                         "name": product.name,
#                     },
#                     "unit_amount": int(product.price * 100),
#                 },
#                 "quantity": 1,
#             }
#         ],
#         mode="payment",
#         success_url=request.build_absolute_uri(reverse("myapp:success"))
#         + "?session_id+{CHECKOUT_SESSION_ID}",
#         cancel_url=request.build_absolute_uri(reverse("myapp:failed")),
#     )
#     order = OrderDetails()
#     # order.customer_username = request.user.username
#     order.product = product
#     order.stripe_payment_intent = checkout_session["payment_intent"]
#     order.amount = int(product.price * 100)
#     order.save()
#     return JsonResponse({"sessionId": checkout_session.id})


# class PaymentSuccessView(TemplateView):
#     template_name = "myapp/payment_success.html"

#     def get(self, request, *args, **kwargs):
#         session_id = request.GET.get("session_id")
#         if session_id is None:
#             return HttpResponseNotFound()

#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         session = stripe.checkout.Session.retrieve(session_id)

#         order = get_object_or_404(
#             OrderDetails, stripe_payment_intent=session.payment_intent
#         )
#         order.has_paid = True
#         order.save()
#         return render(request, self.template_name)


# class PaymentFailedView(TemplateView):
#     template_name = "myapp/payment_failed.html"
# """ def item_details(request, item_id):
#     # Ваш код для обработки запроса с использованием item_id
#     return render(request, "myapp/detail.html", {"item_id": item_id})
#  """
