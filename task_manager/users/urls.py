from django.urls import path
from .views import signin, signup

urlpatterns = [
    path('signup/', signup, name='sign_up'),
    path('signin/', signin, name='sign_in'),

]
