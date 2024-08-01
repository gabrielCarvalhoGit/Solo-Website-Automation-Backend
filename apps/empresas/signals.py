from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User


@receiver(post_save, sender=User)
def add_user_group(sender, instance, created, **kwargs):
    if created and instance.is_admin_empresa:
        group = Group.objects.get(name='resp_empresa')
        instance.groups.add(group)