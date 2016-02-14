from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import MessageModelForm, TopicModelForm
from .models import Topic, Moder, Message


def index(request):
    return render(request, "index.html", {
        'topics': Topic.objects.all()
    })


def add(request):
    if request.method == 'POST':
        user = request.user
        if user.is_anonymous():
            return redirect('/topics/login/')

        add_form = TopicModelForm(request.POST)

        if add_form.is_valid():
            pre_saved_form = add_form.save(commit=False)

            moder = Moder.objects.get(id=1)
            pre_saved_form.author = user
            pre_saved_form.moder = moder
            pre_saved_form.save()

            return redirect('/topics/index')
    else:
        add_form = TopicModelForm()

    return render(request, 'add.html', {
        'add_form': add_form,
    })


def detail(request, id):
    try:
        topic = Topic.objects.get(id=int(id))
    except ObjectDoesNotExist:
        raise Http404

    messages = Message.objects.filter(topic=topic)

    if request.method == 'POST':
        form = MessageModelForm(request.POST)
        user = request.user

        if form.is_valid():
            pre_saved_form = form.save(commit=False)
            
            pre_saved_form.topic = topic
            pre_saved_form.author = user
            pre_saved_form.save()
            
            return redirect('/topics/%s' % id)

    else:
        form = MessageModelForm()

    return render(request, 'detail.html', {
        'topic': topic,
        'messages': messages,
        'message_form': form
    })
