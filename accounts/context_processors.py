from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import UserMessages


def messages(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated():
        user_messages = UserMessages.objects.filter(receiver=user)

        new_messages = user_messages.filter(read=False)
        context = {'new_incoming': new_messages, }

        if hasattr(request, 'resolver_match'):
            sender = request.resolver_match.kwargs.get('username')
            if sender:
                try:
                    sender = User.objects.get(username=sender)
                    context['history'] = UserMessages.objects.filter(receiver=user,
                                                                     sender=sender)
                except User.DoesNotExist:
                    pass

        return context

    else:
        return {}
