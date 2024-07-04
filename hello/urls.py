from django.urls import path
from .views import HelloView

urlpatterns = [
    path('api/hello?visitor_name="Mark"', HelloView.as_view(), name='hello'),
]