from django.db import models


class GamificationInterface(models.Model):
    """
    A user should have a foreign key to a GamificationInterface to keep track of all gamification
    related objects.
    
    game_tracking = ForeignKey(GamificationInterface)
    """
    pass


class BadgeDefinition(models.Model):
    """

    """
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        We made this method expensive as it is likely to be used very rarely (creation of new types of Badges).
        By doing so we save having to do expensive joins for filters that look at the badge name or definition.

        This may be simplified in the future if users opt to use Badge.objects.filter(badge_definition__name=...)
        whereas we wanted it to be simpler syntax as the current Badge.objects.filter(name=...)

        :param args: 
        :param kwargs: 
        :return: 
        """

        # If this is a new BadgeDefinition
        if not hasattr(self, 'pk'):
            super(BadgeDefinition, self).save(*args, **kwargs)

            # Create Badges for all GamificationInterfaces
            for interface in GamificationInterface.objects.all():
                Badge.objects.create(
                    interface=interface,
                    name=self.name,
                    description=self.description,
                    badge_definition=self
                )

        else:
            super(BadgeDefinition, self).save(*args, **kwargs)

            # Update all Badges that use this definition
            Badge.objects.filter(badge_definition=self).update(
                name=self.name,
                description=self.description
            )


class Progression(models.Model):
    """
    
    """
    progress = models.IntegerField(default=0, null=False, blank=False)
    target = models.IntegerField(null=False, blank=False)

    def increment(self):
        self.progress += 1

    @property
    def finished(self):
        return self.progress >= self.target


class Category(models.Model):
    """
    
    """
    name = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Badge(models.Model):
    """

    """
    badge_definition = models.ForeignKey(BadgeDefinition)
    acquired = models.BooleanField(default=False)
    interface = models.ForeignKey(GamificationInterface)

    # These should be populated by the BadgeDefinition that generates this
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    progression = models.ForeignKey(Progression, null=True)
    next_badge = models.ForeignKey('self', null=True)
    category = models.ForeignKey(Category, null=True)

    def increment(self):
        if self.progression:
            self.progression.increment()
            if self.progression.finished:
                self.acquired = True

    def award(self):
        if not self.progression or self.progression.finished:
            self.acquired = True