# Django Gamification
[![PyPI version](https://badge.fury.io/py/django-gamification.svg)](https://badge.fury.io/py/django-gamification)

Django Gamification aims to fill the gamification sized whole in the Django package ecosystem. In the current state, Django Gamification provides a set of models that can be used to implement gamification features in your application. These include a centralised interface for keeping track of all gamification related objects including badges, points, and unlockables.

## Installation

```
pip install django_gamification
```

## Features and Examples
### Concepts
Django Gamification requires the understanding of a few core concepts.
- **BadgeDefinitions:** A template used to create new Badges and update existing Badges.
- **Badge:** An object that represents some achievable objective in the system that can award points and track its own progression.
- **UnlockableDefinition:** A template used to create new Unlockables and update existing Unlockables.
- **Unlockable:** An object that is achieved by some accumulation of points.
- **Category:** An object used to label other objects like Badges via their BadgeDefinition.

### Interfaces
#### Creating an interface
```python

from django.contrib.auth.models import User
from django.db import models
from django_gamification.models import GamificationInterface

class YourUserModel(models.User):
    # Your user fields here
    
    # The gamification interface
    interface = models.ForeignKey(GamificationInterface)
```

### BadgeDefinitions and Badges
### Creating a new badge
By creating a new `BadgeDefinition`, Django Gamification will automatically create `Badge` instances for all your current `GamificationInterfaces` with `Badge.name`, `Badge.description`, `Badge.points`, `Badge.progression` and `Badge.category` mimicking the fields on the `BadgeDefinition`.

```python
from django_gamification.models import BadgeDefinition, Category

BadgeDefinition.objects.create(
    name='Badge of Awesome',
    description='You proved your awesomeness',
    points=50,
    progression_target=100,
    category=Category.objects.create(name='Gold Badges', description='These are the top badges'),
)
```

### Awarding a badge
You can manually award a `Badge` instance using `Badge.award()`.

```python
from django_gamification.models import Badge

badge = Badge.objects.first()
# badge.acquired = False

badge.award()
# badge.acquired = True
```

### UnlockableDefinitions and Unlockables
### Creating a new unlockable
By creating a new `UnlockableDefinition`, Django Gamification will automatically create `Unlockable` instances for all your current `GamificationInterfaces` with `Unlockable.name`, `Unlockable.description`, `Unlockable.points_required` mimicking the fields on the `UnlockableDefinition`.

```python
from django_gamification.models import UnlockableDefinition

UnlockableDefinition.objects.create(
    name='Some super sort after feature',
    description='You unlocked a super sort after feature',
    points_required=100
)
```
