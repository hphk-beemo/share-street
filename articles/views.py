import os
import io
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.images import ImageFile
from .models import *
from dotenv import load_dotenv


def index(request):
    articles = Article.objects.order_by("-pk")
    return render(
        request,
        "index.html",
        context={
            "articles": articles,
        },
    )


def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    return render(request, "detail.html", {"article": article})


@login_required
def create(request):
    load_dotenv()
    MAP_API_KEY = os.getenv("MAP_API_KEY")
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        pitch = request.POST.get("pitch")
        heading = request.POST.get("heading")

        article = Article()
        article.title = title
        article.content = content
        article.lat = lat
        article.lng = lng
        article.pitch = pitch
        article.heading = heading
        article.user = request.user
        article.save()

        URL = f"https://maps.googleapis.com/maps/api/streetview?size=400x400&location={lat},{lng}&fov=80&heading={heading}&pitch={pitch}&key={MAP_API_KEY}"
        image = requests.get(URL)

        article.thumbnail = ImageFile(
            io.BytesIO(image.content), name=f"{article.pk}.jpg"
        )

        article.save()

        return redirect("index")

    else:
        API_KEY = os.getenv("MAP_API_KEY")
        return render(
            request,
            "create.html",
            {
                "API_KEY": API_KEY,
            },
        )


@login_required
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    if article.user == request.user:
        article.delete()
        return redirect("index")

    return redirect("detail", article_pk)
