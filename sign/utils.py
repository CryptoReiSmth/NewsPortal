from django.contrib.auth.models import Group


def get_group(name):
    current_group, created = Group.objects.get_or_create(name=name)
    return current_group
