from .models import UserMessages


def messages(request):
    user = request.user
    if user.is_authenticated():
        new_messages = UserMessages.objects.filter(read=False)
        new_incoming = new_messages.filter(receiver=user)
        return {'new_incoming': new_incoming}
    else:
        return {}