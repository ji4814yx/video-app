from urllib import parse
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

class Video(models.Model):
    # let's add the fields
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        # extract the video id from a youtube url
        url_components = parse.urlparse(self.url)

        if url_components.scheme != 'https':
            raise ValidationError(f'Not a YouTube URL {self.url}')

        if url_components.netloc != 'www.youtube.com':
            raise ValidationError(f'Not a YouTube URL {self.url}')

        if url_components.path != '/watch':
            raise ValidationError(f'Not a YouTube URL {self.url}')

        query_string = url_components.query  # it will show 'v=12345678'
        if not query_string:
            raise ValidationError(f'Invalid YouTube URL {self.url}')
        parameters = parse.parse_qs(query_string, strict_parsing=True)  # thi is a dictionary
        v_parameters_list = parameters.get('v')  # this will return None if no key found like abc=12345678
        if not v_parameters_list:  # this is checking if None or empty list
            raise ValidationError(f'Invalid YouTube URL, missing parameters {self.url}')
        self.video_id = v_parameters_list[0]  # This is a string

        super().save(*args, **kwargs)

    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url},Video ID: {self.video_id} Notes{self.notes[:200]}'
