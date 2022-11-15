from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:article_pk>/delete/", views.delete, name="delete"),
    path("<int:article_pk>/", views.detail, name="detail"),
]
