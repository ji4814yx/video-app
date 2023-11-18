from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from .forms import VideoForm, SearchForm
from .models import Video


# Create your views here: home page view
def home(request):
    app_name = 'Exercise Video'  # put your own category here
    return render(request, 'video_collection/home.html', {'app_name': app_name})


def add(request):  # create add function

    if request.method == "POST":
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            try:
                new_video_form.save()
                return redirect('video_list')
            # messages.info(request, 'New video saved!')
            # todo show success message or redirect to list of videos
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError:
                messages.warning(request, 'You already added that video')
            # I removed else from here and indent line 29 and 30
        messages.warning(request, 'Please check the data entered.')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

    new_video_form = VideoForm()  # make a new video form
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})


def video_list(request):
    search_form = SearchForm(request.GET)  # build form from data user has sent to app

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']  # we can use this search term to search db e.g 'yoga'
        # or 'squats'

        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name'))  # to run the video

    else:  # form is not filled in or this is the first time the user sees the page
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))

    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})
