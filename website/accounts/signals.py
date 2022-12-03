from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from blog.models import Posts


@receiver(post_save, sender=Posts)
def my_handler(sender, **kwargs):
    print("hello", sender)


@receiver
def post_delete(sender, **kwargs):
    print("deleted : ", sender, kwargs)
