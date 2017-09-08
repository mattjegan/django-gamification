
from django.test import TestCase

from django_gamification.models import GamificationInterface, PointChange, BadgeDefinition, Badge, Progression, \
    UnlockableDefinition, Unlockable, Category


class GamificationInterfaceTest(TestCase):

    def test_points_default_to_zero(self):
        interface = GamificationInterface.objects.create()
        self.assertEqual(interface.points, 0)

    def test_points(self):
        interface = GamificationInterface.objects.create()

        PointChange.objects.create(
            amount=100,
            interface=interface
        )
        self.assertEqual(interface.points, 100)


class BadgeDefinitionTest(TestCase):

    def test_save(self):

        for i in range(2):
            GamificationInterface.objects.create()

        definition = BadgeDefinition.objects.create(
            name='mybadgedefinition',
            description='mybadgedescription',
            progression_target=100,
            category=Category.objects.create(name='category1', description='description1'),
            points=50
        )
        self.assertEqual(Badge.objects.filter(badge_definition=definition).count(),
                         GamificationInterface.objects.all().count())

        for badge in Badge.objects.filter(badge_definition=definition):
            self.assertEqual(badge.name, 'mybadgedefinition')
            self.assertEqual(badge.description, 'mybadgedescription')
            self.assertEqual(badge.progression.target, 100)
            self.assertEqual(badge.category.name, 'category1')
            self.assertEqual(badge.points, 50)

        definition.name = 'myaltereddefinition'
        definition.description = 'myaltereddescription'
        definition.progression_target = 50
        definition.category.name = 'category2'
        definition.category.save()
        definition.points = 75
        definition.save()

        for badge in Badge.objects.filter(badge_definition=definition):
            self.assertEqual(badge.name, 'myaltereddefinition')
            self.assertEqual(badge.description, 'myaltereddescription')
            self.assertEqual(badge.progression.target, 50)
            self.assertEqual(badge.category.name, 'category2')
            self.assertEqual(badge.points, 75)

        definition.progression_target = None
        definition.save()

        for badge in Badge.objects.filter(badge_definition=definition):
            self.assertEqual(badge.progression, None)


class BadgeTest(TestCase):

    def test_increment(self):
        interface = GamificationInterface.objects.create()
        BadgeDefinition.objects.create(
            name='mybadgedefinition',
            description='mybadgedescription'
        )
        badge = Badge.objects.get(interface=interface)
        badge.progression = Progression.objects.create(target=1)
        self.assertEqual(badge.progression.progress, 0)
        badge.increment()
        self.assertEqual(badge.progression.finished, True)
        self.assertEqual(badge.acquired, True)

    def test_award(self):
        interface = GamificationInterface.objects.create()
        BadgeDefinition.objects.create(
            name='mybadgedefinition',
            description='mybadgedescription'
        )
        badge = Badge.objects.get(interface=interface)
        badge.points = 10
        self.assertEqual(badge.acquired, False)
        self.assertEqual(PointChange.objects.all().count(), 0)
        badge.award()
        self.assertEqual(badge.acquired, True)
        self.assertEqual(PointChange.objects.all().count(), 1)
        self.assertEqual(interface.points, 10)


class UnlockableDefinitionTest(TestCase):

    def test_save(self):

        for i in range(2):
            GamificationInterface.objects.create()

        definition = UnlockableDefinition.objects.create(
            name='myunlockabledefinition',
            description='myunlockabledescription',
            points_required=10
        )
        self.assertEqual(Unlockable.objects.filter(unlockable_definition=definition).count(),
                         GamificationInterface.objects.all().count())

        for unlockable in Unlockable.objects.filter(unlockable_definition=definition):
            self.assertEqual(unlockable.name, 'myunlockabledefinition')

        definition.name = 'myaltereddefinition'
        definition.save()

        for unlockable in Unlockable.objects.filter(unlockable_definition=definition):
            self.assertEqual(unlockable.name, 'myaltereddefinition')