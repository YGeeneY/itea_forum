from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import MessageForm, TopicModelForm
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
            topic = add_form.save(commit=False)

            moder = Moder.objects.get(id=1)
            topic.author = user
            topic.moder = moder
            topic.save()

            return redirect('/topics/index')
    else:
        add_form = TopicModelForm()
    return render(request, 'add.html', {
        'add_form': add_form,
    })


def detail(request, id):
    try:
        topic = Topic.objects.get(id=int(id))
        messages = Message.objects.filter(topic=topic)
    except ObjectDoesNotExist:
        raise Http404

    form = MessageForm()

    if request.method == 'GET':
        return render(request, 'detail.html', {
            'topic': topic,
            'messages': messages,
            'message_form': form
        })

    elif request.method == 'POST':
        form = MessageForm(request.POST)

        user = request.user

        if form.is_valid():
            Message.objects.create(
                topic=topic,
                text=request.POST['text'],
                author=user,
            )
            return redirect('/topics/%s' % id)

        else:
            return render(request, 'detail.html', {
                'topic': topic,
                'messages': messages,
                'message_form': form
            })
