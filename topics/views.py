from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, ListView

from .models import Topic, Moder, Message


class IndexView(ListView):
    model = Topic
    template_name = 'landing/landing_topics.html'
    context_object_name = 'topics'
    # template_name = 'index.html'


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


class MessageAddView(CreateView):
    template_name = 'add_message.html'
    model = Message
    fields = ('text', )

    def form_valid(self, form):
        message = form.save(commit=False)
        message.author = self.request.user
        pk = self.kwargs['pk']
        topic = get_object_or_404(Topic, pk=pk)
        message.topic = topic
        message.save()

        return redirect('/topics/%s' % pk)


class MessageListView(ListView):
    template_name = 'landing/landing_topic.html'
    model = Message
    context_object_name = 'messages'

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data()
        pk = self.kwargs['pk']
        topic = get_object_or_404(Topic, pk=pk)
        context['topic'] = topic

        return context

    def get_queryset(self):
        qs = super(MessageListView, self).get_queryset()
        pk = self.kwargs['pk']
        topic = get_object_or_404(Topic, pk=pk)
        qs = qs.filter(topic=topic)

        return qs
