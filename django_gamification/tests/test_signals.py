
from django.test import TestCase

from django_gamification.models import PointChange, GamificationInterface, BadgeDefinition, Badge
from django_gamification.signals import check_unlockables


class CheckUnlockablesTest(TestCase):
    """ Tests that the interface being used has unlocked no Unlockables""" 
    def test_check_unlockables_no_instance(self):
        self.assertIsNone(check_unlockables(PointChange, instance=None))

        
class CheckGamificationInterfaceCreateTest(TestCase):
    """ Tests that new badges are created when a new interface is created """
    def test_badges_after_interface_create(self):
        BadgeDefinition.objects.create(
            name='mybadgedefinition',
            description='mybadgedescription'
        )
        self.assertEqual(Badge.objects.count(), 0)
        GamificationInterface.objects.create()
        self.assertEqual(Badge.objects.count(), 1)

    def test_badges_after_interface_save(self):
        interface = GamificationInterface.objects.create()
        BadgeDefinition.objects.create(
            name='mybadgedefinition',
            description='mybadgedescription'
        )
        Badge.objects.all().delete()
        interface.save()
        self.assertEqual(Badge.objects.count(), 0)
