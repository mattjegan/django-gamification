
from django.test import TestCase

from django_gamification.models import GamificationInterface, PointChange, BadgeDefinition, Badge, Progression, \
    UnlockableDefinition, Unlockable, Category


class GamificationInterfaceTest(TestCase):
    """Tests for Gamification Interface"""
    
    def test_points_default_to_zero(self):
        """Tests that when an interface is created, the test-points are intialised to zero"""
        
        interface = GamificationInterface.objects.create()
        self.assertEqual(interface.points, 0)

    def test_points(self):
        """Tests that the change in points reflect in the Gamification Interface"""
        
        interface = GamificationInterface.objects.create()

        PointChange.objects.create(
            amount=100,
            interface=interface
        )
        self.assertEqual(interface.points, 100)


class BadgeDefinitionTest(TestCase):
    """Tests that check the badge definitions are correctly created, additional inerfaces can be added after some badgedefinitions 
      are already in existance, next_badge created is properly linked to The new badge definitions and all changes to the old 
      badgedefinitions are saved.
    """
        
    longMessage = True

    def runTest(self):
        self.test_save()

    def test_save(self):

        test_msg_0 = "test: creating GI badges for new badgedefinitions"
        for i in range(2):
            GamificationInterface.objects.create()

        definition1 = BadgeDefinition.objects.create(
            name='mybadgedefinition1',
            description='mybadgedescription1',
            progression_target=100,
            category=Category.objects.create(name='category1', description='description1'),
            points=50
        )
        self.assertEqual(Badge.objects.filter(badge_definition=definition1).count(),
                         GamificationInterface.objects.all().count(),
                         msg=test_msg_0)

        test_msg_1 = "test: add additional interfaces after some badge definitions already exist"
        GamificationInterface.objects.create()

        definition2a = BadgeDefinition.objects.create(
            name='mybadgedefinition2a',
            description='mybadgedescription2a',
            progression_target=100,
            category=Category.objects.create(name='category1', description='description1'),
            points=50
        )
        definition2b = BadgeDefinition.objects.create(
            name='mybadgedefinition2b',
            description='mybadgedescription2b',
            progression_target=200,
            next_badge=BadgeDefinition.objects.filter(name='mybadgedefinition2a').last(),
            category=Category.objects.filter(name='category1', description='description1').last(),
            points=100
        )

        # for new badgedefinition
        self.assertEqual(Badge.objects.filter(badge_definition=definition2b).count(),
                         GamificationInterface.objects.all().count(),
                         msg=test_msg_1)

        # for old badgedefinition
        # test_msg_2 = test_msg_1 + "this won't work until Issue #12 is handled"
        # self.assertEqual(Badge.objects.filter(badge_definition=definition1).count(),
        #                  GamificationInterface.objects.all().count(),
        #                  msg=test_msg_2)

        test_msg_3 = "test: check that next_badge is properly linked with a new badgedefinition; badge: {}; {} vs {}"
        for i, badge in enumerate(Badge.objects.filter(badge_definition=definition2b)):
            self.assertEqual(badge.name, 'mybadgedefinition2b', msg=test_msg_3.format(i, badge.name, 'mybadgedefinition2b'))
            self.assertEqual(badge.category.name, 'category1', msg=test_msg_3.format(i, badge.category.name, 'category1'))
            self.assertEqual(badge.next_badge.name, 'mybadgedefinition2a', msg=test_msg_3.format(i, badge.next_badge.name, 'mybadgedefinition2a'))

        test_msg_4 = "test: saving changes to old badgedefinition (incl. new next_badge); badge: {}; {} vs {}"
        definition3 = BadgeDefinition.objects.create(
            name='mybadgedefinition3',
            description='mybadgedescription3',
            progression_target=200,
            category=Category.objects.filter(name='category1', description='description1').last(),
            points=100
        )
        for badge in Badge.objects.filter(badge_definition=definition1):
            self.assertEqual(badge.name, 'mybadgedefinition1')
            self.assertEqual(badge.description, 'mybadgedescription1')
            self.assertEqual(badge.progression.target, 100)
            self.assertEqual(badge.category.name, 'category1')
            self.assertEqual(badge.points, 50)
            self.assertEqual(badge.next_badge, None)

        definition1.name = 'myaltereddefinition'
        definition1.description = 'myaltereddescription'
        definition1.progression_target = 50
        definition1.category.name = 'category2'
        definition1.next_badge = definition3
        definition1.category.save()
        definition1.points = 75
        definition1.save()

        for i, badge in enumerate(Badge.objects.filter(badge_definition=definition1)):
            self.assertEqual(badge.name, 'myaltereddefinition', msg=test_msg_4.format(i, badge.name, 'myaltereddefinition'))
            self.assertEqual(badge.description, 'myaltereddescription', msg=test_msg_4.format(i, badge.description, 'myaltereddescription'))
            self.assertEqual(badge.progression.target, 50, msg=test_msg_4.format(i, badge.progression.target, 50))
            self.assertEqual(badge.category.name, 'category2', msg=test_msg_4.format(i, badge.category.name, 'category2'))
            self.assertEqual(badge.next_badge.name, 'mybadgedefinition3', msg=test_msg_4.format(i, badge.next_badge.name, 'mybadgedefinition3'))
            self.assertEqual(type(badge.next_badge), type(badge), msg=test_msg_4.format(i, type(badge.next_badge), type(badge)))
            self.assertEqual(badge.points, 75, msg=test_msg_4.format(i, badge.points, 75))

        definition1.progression_target = None
        definition1.save()

        for badge in Badge.objects.filter(badge_definition=definition1):
            self.assertEqual(badge.progression, None, msg=test_msg_4)


class BadgeTest(TestCase):
    """Tests that check Badge progression and awards"""
    
    def test_increment(self):
        """Tests that badge progression(increment) works and bagde can be acquired"""
        
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
        """Tests that before badge is awarded, the badge is not acquired and PointChange model is not updated. And after the
        badge is awarded the badge is acquired and PointChange model is updated."""
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

    def test_revoke_acquired_objects(self):
        interface = GamificationInterface.objects.create()
        BadgeDefinition.objects.create(
            name='mybadgedefinition',
            description='mybadgedescription'
        )
        badge = Badge.objects.get(interface=interface)
        badge.points = 10
        self.assertEqual(badge.acquired, False)
        self.assertEqual(PointChange.objects.all().count(), 0)
        self.assertEqual(Badge.acquired_objects.count(), 0)
        badge.award()
        self.assertEqual(badge.acquired, True)
        self.assertEqual(badge.revoked, False)
        self.assertEqual(PointChange.objects.all().count(), 1)
        self.assertEqual(interface.points, 10)
        badge.force_revoke()
        self.assertEqual(badge.revoked, True)
        self.assertEqual(PointChange.objects.all().count(), 2)
        self.assertEqual(interface.points, 0)
        self.assertEqual(Badge.objects.all().count(), 1)
        badge.award()
        self.assertEqual(badge.acquired, True)
        self.assertEqual(badge.revoked, False)
        self.assertEqual(PointChange.objects.all().count(), 3)
        self.assertEqual(interface.points, 10)



class UnlockableDefinitionTest(TestCase):
    """Test that  Unlockable Definitions are created correctly."""
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
