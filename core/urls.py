from django.urls import path

from core.views import UrlShortenerView

urlpatterns = [
    path("shorten/", UrlShortenerView.as_view()),
    path("<str:short_code>", UrlShortenerView.as_view()),
]
