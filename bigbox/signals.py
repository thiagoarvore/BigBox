from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from bigbox.models import Kit


@receiver(m2m_changed, sender=Kit.content.through)
def kit_post_save(sender, instance, action, **kwargs):
    if action == 'post_add':
        for product in instance.content.all():
            product.amount -= 1
            product.save()

            