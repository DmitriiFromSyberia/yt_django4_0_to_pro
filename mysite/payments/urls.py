from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("config/", views.stripe_config),  # new
    path(
        "create-checkout-session/<int:index>/",
        views.create_checkout_session,
        name="create-checkout-session",
    ),  # new
    path("success/", views.SuccessView.as_view()),  # new
    path("cancelled/", views.CancelledView.as_view()),  # new
    path("webhook/", views.stripe_webhook),  # new
]
