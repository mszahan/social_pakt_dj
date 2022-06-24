from urllib.request import urlopen,Request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from django.forms import fields, widgets
from .models import Image


class ImageCreationForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets={
            'url': forms.HiddenInput,
        }
    
# to only allow the certain image type
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extention = url.rsplit('.', 1)[1].lower()
        if extention not in valid_extensions:
            raise forms.ValidationError('The given url does not match valid image extension')
        return url

# to download the image file utomatically I guess
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreationForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = f"{slugify(image.title)}.{image_url.rsplit('.', 1)[1].lower()}"

        #download image from the given url
        req = Request(url=image_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        image.image.save(image_name, ContentFile(response.read()), save=False)


        if commit:
            image.save()
        return image