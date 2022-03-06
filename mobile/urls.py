from django.urls import path
from mobile.views import index

urlpatterns = [
    path('', index.index,name='index'),
]
