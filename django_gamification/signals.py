
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_gamification.models import PointChange, Unlockable


@receiver(post_save, sender=PointChange)
def check_unlockables(sender, instance=None, **kwargs):
    """
    Checks if the interface being used has unlocked any new Unlockables

    :param sender: 
    :param kwargs: 
    :return: 
    """
    if instance is None:
        return

    # Find all unlockables for the interface that have less points
    # then the current interface, and update them to be unlocked
    Unlockable.objects.filter(
        interface=instance.interface,
        points_required__lte=instance.interface.points
    ).update(
        acquired=True
    )
