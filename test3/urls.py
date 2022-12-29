


from django.urls import include, path
from .views import *

app_name = 'test3'

urlpatterns = [
path('', CreateView.as_view(), name="CreateView"),
    ]