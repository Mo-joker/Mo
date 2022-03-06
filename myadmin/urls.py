from django.urls import path
from myadmin.views import index

urlpatterns = [
    path('', index.index,name='myadmin_index'),
]
