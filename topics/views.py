from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import MessageModelForm
from .models import Topic, Moder, Message


def index(request):
    return render(request, "index.html", {
        'topics': Topic.objects.all()
    })


class AddView(CreateView):
    template_name = 'add.html'
    success_url = '/topics/index'
    model = Topic

    fields = ('name', )

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.author = self.request.user
        topic.moder = Moder.objects.get(pk=1)
        topic.save()

        return redirect(self.success_url)


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
