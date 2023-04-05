from django.urls import path
from django.views.generic import RedirectView

from .views import upload_parse, show_db, clear_db


urlpatterns = [
    path('parser/', upload_parse, name='load_parse'),
    path('showdb/', show_db, name='show_db'),
    path('cleardb/', clear_db, name='clear_db'),
    path('', RedirectView.as_view(pattern_name='load_parse'))
]

