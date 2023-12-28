from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

# from .views import register

from .views import register, logout_view

# from django.contrib.auth import logout

app_name = "users"


# def logout_view(request):
#     logout(request)
#     # Redirect to a success page.


urlpatterns = [
    # http://127.0.0.1:8000/users/
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    # path(
    #     "logout/",
    #     LogoutView.as_view(template_name="users/logout.html", next_page=None),
    #     name="logout",
    # ),
    path("logout/", logout_view, name="logout"),  # Временное решение
]
