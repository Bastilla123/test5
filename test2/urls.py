
from django.urls import include, path


urlpatterns = [


    path('test3/', include('test3.urls', namespace='test3')),
]
