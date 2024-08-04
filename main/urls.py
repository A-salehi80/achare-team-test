from django.urls import path
from .views import LoginView, IdentifyView, SendVerificationCodeView, RegisterView
app_name = 'main'
urlpatterns = [
    path('identify/', IdentifyView.as_view(), name='identify'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify/', SendVerificationCodeView.as_view(), name='verify'),
    path('register/', RegisterView.as_view(), name='register'),

]