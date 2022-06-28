from django.contrib.auth.models import Group,User
from django.db.models.signals import post_save
from .models import Author
from django.dispatch import receiver

def customer_created(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Author.objects.create(
            user=instance
        )

        print('Profile created')

post_save.connect(customer_created, sender=User)
