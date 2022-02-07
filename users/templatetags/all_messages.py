from atexit import register
from django.template import Library

register = Library()



@register.filter
def all_messages(qs):
    count = 0
    for i in qs.chat_set.all():
        count += i.message_set.all().filter(is_readed=False).exclude(author=qs).count()
    return count
    
@register.filter
def count_unread(qs, user):
    count_unread = qs.message_set.all().filter(is_readed=False).exclude(author=user)
    return count_unread.count()


