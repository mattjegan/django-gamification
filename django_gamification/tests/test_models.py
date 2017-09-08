
from datetime import datetime

from django.test import TestCase

from django_gamification.models import GamificationInterface, PointChange, BadgeDefinition, Badge


class GamificationInterfaceTest(TestCase):

    def test_points_default_to_zero(self):
        interface = GamificationInterface()
        self.assertEqual(interface.points, 0)

    def test_points(self):
        interface = GamificationInterface()
        interface.save()

        PointChange.objects.create(
            amount=100,
            interface=interface
        )
        self.assertEqual(interface.points, 100)


class BadgeDefinitionTest(TestCase):

    def test_save(self):

        for i in range(2):
            GamificationInterface.objects.create()

        definition = BadgeDefinition(
            name='mybadgedefinition',
            description='mybadgedescription'
        )
        definition.save()
        self.assertEqual(Badge.objects.filter(badge_definition=definition).count(),
                         GamificationInterface.objects.all().count())

        for badge in Badge.objects.filter(badge_definition=definition):
            self.assertEqual(badge.name, 'mybadgedefinition')

        definition.name = 'myaltereddefinition'
        definition.save()

        for badge in Badge.objects.filter(badge_definition=definition):
            self.assertEqual(badge.name, 'myaltereddefinition')
