
from datetime import datetime

from django.test import TestCase

from django_gamification.models import GamificationInterface, PointChange


class GamificationInterfaceTest(TestCase):

    def test_init(self):
        interface = GamificationInterface()
        assert interface is not None

    def test_points_default_to_zero(self):
        interface = GamificationInterface()
        assert interface.points == 0, interface.points

    def test_points(self):
        interface = GamificationInterface()
        interface.save()

        PointChange.objects.create(
            amount=100,
            interface=interface
        )
        assert interface.points == 100, interface.points
