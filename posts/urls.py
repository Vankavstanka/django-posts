from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("",           views.post_list,   name="list"),
    path("<int:pk>/",  views.post_detail, name="detail"),
]
