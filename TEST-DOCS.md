# Test Docs for Contribution

The Tests are integrated with Coverage.py . To install Coverage.py, follow this link : [Coverage](https://pypi.python.org/pypi/coverage)

To run all the tests found within the django-gamification package :
```
coverage run --source='.' manage.py test django-gamification
```
To run all tests for Interfaces :
```
coverage run --source='.' manage.py test GamificationInterfaceTest
```
To test if Test points default to zero :
```
coverage run --source='.' manage.py test test_points_default_to_zero
```
To test Test-points :
```
coverage run --source='.' manage.py test test_points
```
To run all the tests regarding Badge Definition:
```
coverage run --source='.' manage.py test BadgeDefinitionTest
```
To run all the tests regarding Badges made:
```
coverage run --source='.' manage.py test BadgeTest
```
To test Test-Incremenents:
```
coverage run --source='.' manage.py test test_increment
```
To test Test-Awards:
```
coverage run --source='.' manage.py test test_award
```
To Test Unlockable Definitions :
```
coverage run --source='.' manage.py test UnlockableDefinitionTest
```
