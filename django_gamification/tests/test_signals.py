
from django.test import TestCase

from django_gamification.models import PointChange
from django_gamification.signals import check_unlockables


class CheckUnlockablesTest(TestCase):
    """ Tests that the interface being used has unlocked no Unlockables""" 
    def test_check_unlockables_no_instance(self):
        self.assertIsNone(check_unlockables(PointChange, instance=None))
