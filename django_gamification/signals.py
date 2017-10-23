
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_gamification.models import PointChange, Unlockable, \
    GamificationInterface, BadgeDefinition, Badge, UnlockableDefinition


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


@receiver(post_save, sender=GamificationInterface)
def create_badges_and_unlockables_from_new_interface(
        sender, instance, created, **kwargs):
    """
    Creates new badges from all definitions for the new interface.

    :param sender:
    :param created:
    :param kwargs:
    :return:
    """

    if not created:
        return

    for definition in BadgeDefinition.objects.all():
        Badge.objects.create_badge(definition, instance)

    for definition in UnlockableDefinition.objects.all():
        Unlockable.objects.create_unlockable(definition, instance)
