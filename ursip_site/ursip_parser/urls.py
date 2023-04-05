from django.urls import path, include

from .views import upload_parse

urlpatterns = [
    path('', upload_parse, name='load_parse')
]

