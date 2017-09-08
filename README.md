# Django Gamification
[![PyPI version](https://badge.fury.io/py/django-gamification.svg)](https://badge.fury.io/py/django-gamification)

Django Gamification aims to fill the gamification sized whole in the Django package ecosystem. In the current state, Django Gamification provides a set of models that can be used to implement gamification features in your application. These include a centralised interface for keeping track of all gamification related objects including badges, points, and unlockables.

## Installation

```
pip install django_gamification
```

## Features and Examples
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
By creating a new `BadgeDefinition`, Django Gamification will automatically create `Badge` instances for all your current `GamificationInterfaces` with `Badge.name`, `Badge.description`, `Badge.points` mimicking the fields on the `BadgeDefinition`.

```python
from django_gamification.models import BadgeDefinition

BadgeDefinition.objects.create(
    name='Badge of Awesome',
    description='You proved your awesomeness',
    points=50
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

**Badges**
- [x] Instant Award
- [x] Progressive Award
- [x] Chained Badges
- [x] Badge Categories

**Points**
- [x] Manually Awardable
- [x] Rewarded Points from Badges
- [x] Manual Setbacks (via negative PointChange)
- [x] Log of point changes

**Unlockables**
- [x] Unlockable via Points

**Views**
- [ ] Auto-update Badges
- [ ] Auto-update Points
- [ ] Auto-update Unlockables

**Django REST Framework**
- [ ] Gamification Serializers
- [ ] Gamification Views

**Misc**
- [ ] Gamification Notification List
- [ ] Player reset
