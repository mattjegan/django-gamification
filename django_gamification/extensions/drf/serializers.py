from rest_framework import serializers

from django_gamification.models import GamificationInterface, Category, BadgeDefinition, Progression,\
    PointChange, Badge, UnlockableDefinition, Unlockable


class GamificationInterfaceSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = GamificationInterface
        fields = ('id', 'points')


class CategorySerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Category
        fields = '__all__'


class PointChangeSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = PointChange
        fields = '__all__'


class ProgressionSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Progression
        fields = ('id', 'progress', 'target', 'finished')


class BadgeDefinitionSerializer(serializers.ModelSerializer):
    """

    """
    category = CategorySerializer()

    class Meta:
        model = BadgeDefinition
        fields = '__all__'


class BadgeSerializer(serializers.ModelSerializer):
    """

    """
    progression = ProgressionSerializer()

    class Meta:
        model = Badge
        fields = '__all__'


class UnlockableDefinitionSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = UnlockableDefinition
        fields = '__all__'


class UnlockableSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Unlockable
        fields = '__all__'
