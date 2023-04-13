from django.urls import path
from .views import register, endreg
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [

    path('signup/', register, name="register"),
    path('activation_code_form/', endreg, name="endreg"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
