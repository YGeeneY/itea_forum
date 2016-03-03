from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, ListView

from section.models import Section
from .models import Topic, Moder, Message


class TopicView(ListView):
    model = Topic
    template_name = 'landing/topic.html'
    context_object_name = 'topics'
    paginate_by = 5

    def get_queryset(self):
        qs = super(TopicView, self).get_queryset()
        slug = self.kwargs['slug']
        qs = qs.filter(section__slug=slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super(TopicView, self).get_context_data()
        slug = self.kwargs['slug']
        context['slug'] = slug
        context['section'] = get_object_or_404(Section, slug=slug)
        return context


class TopAddView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = 'landing/add_new_topic.html'
    model = Topic
    fields = ('name', 'short_description')

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.author = self.request.user
        topic.moder = Moder.objects.get(pk=1)
        slug = self.kwargs['slug']
        topic.section = get_object_or_404(Section, slug=slug)
        messages.info(self.request, 'Тема успешно добавлена!')

        topic.save()

        return redirect(
            reverse_lazy('topic', kwargs={'slug': slug})
        )


class MessageAddView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = 'landing/add_new_message.html'
    model = Message
    fields = ('title', 'text',)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.author = self.request.user
        pk = self.kwargs['pk']
        slug = self.kwargs['slug']
        topic = get_object_or_404(Topic, pk=pk)
        message.topic = topic

        if not message.title:
            if topic.message_set.count() == 0:
                prefix = ''
            else:
                prefix = 'RE:'
            message.title = '%s %s' % (prefix,topic.name,)

        message.save()
        messages.info(self.request, 'Сообщение успешно добавлено')

        return redirect(
            reverse_lazy('topic_messages', kwargs={'slug': slug, 'pk': pk})
        )


class MessageListView(ListView):
    template_name = 'landing/messages.html'
    model = Message
    context_object_name = 'topic_messages'
    paginate_by = 10

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
