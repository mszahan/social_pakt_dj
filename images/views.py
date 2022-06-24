from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import re_words
from .forms import ImageCreationForm
from .models import *
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from actions.utils import create_action
import redis
from django.conf import settings



# connect to redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)






@login_required
def image_create(request):
    """
    view for creating an Image using the JavaScript Bookmarklet.
    """
    if request.method == 'POST':
        #form is sent
        form = ImageCreationForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            #assign current user to the item
            new_item.user = request.user
            new_item.save()
            # the action for news feed I guess
            create_action(request.user, 'bookmarked image', new_item)
            # messages.success(request, 'Image added successfully')
            return redirect(new_item)
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreationForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form':form})



def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 6)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section':'images', 'images':images})
    return render(request, 'images/image/list.html', {'section':'images', 'images':images})
    





def image_detail(request, pk, slug):
    image = get_object_or_404(Image, pk=pk, slug=slug)
    # increamenting the image vies by visitor by 1
    total_views = r.incr(f'image:{image.id}:views')
    # increament image ranking by 1
    r.zincrby('image_ranking', 1, image.id)
    return render(request, 'images/image/detail.html', {'section':'images', 'image':image, 'total_views':total_views})


@login_required
def image_ranking(request):
    #get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]

    #get most viewd image
    most_viewd = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewd.sort(key=lambda x: image_ranking_ids.index(x.id))

    return render(request, 'images/image/ranking.html', {'section':'images_rank', 'most_viewd':most_viewd})


@login_required
@require_POST
@ajax_required
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})