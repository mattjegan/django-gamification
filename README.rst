Django Gamification
===================

|PyPI version| |Build Status|

Django Gamification aims to fill the gamification sized hole in the
Django package ecosystem. In the current state, Django Gamification
provides a set of models that can be used to implement gamification
features in your application. These include a centralised interface for
keeping track of all gamification related objects including badges,
points, and unlockables.

Installation
------------

Download from PyPI:

::

    pip install django-gamification

And add to your ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        .
        .
        .
        'django_gamification'
    ]

Features and Examples
---------------------

Concepts
~~~~~~~~

Django Gamification requires the understanding of a few core concepts.

- **BadgeDefinitions:** A template used to create new Badges and update existing Badges.
- **Badge:** An object that represents some achievable objective in the system that can award points and track its own progression.
- **UnlockableDefinition:** A template used to create new Unlockables and update existing Unlockables.
- **Unlockable:** An object that is achieved by some accumulation of points.
- **Category:** An object used to label other objects like Badges via their BadgeDefinition.

Interfaces
~~~~~~~~~~

Creating an interface
^^^^^^^^^^^^^^^^^^^^^

.. code:: python


    from django.contrib.auth.models import User
    from django.db import models
    from django_gamification.models import GamificationInterface

    class YourUserModel(models.User):
        # Your user fields here

        # The gamification interface
        interface = models.ForeignKey(GamificationInterface)

BadgeDefinitions and Badges
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creating a new badge
~~~~~~~~~~~~~~~~~~~~

By creating a new ``BadgeDefinition``, Django Gamification will
automatically create ``Badge`` instances for all your current
``GamificationInterfaces`` with ``Badge.name``, ``Badge.description``,
``Badge.points``, ``Badge.progression`` and ``Badge.category`` mimicking
the fields on the ``BadgeDefinition``.

.. code:: python

    from django_gamification.models import BadgeDefinition, Category

    BadgeDefinition.objects.create(
        name='Badge of Awesome',
        description='You proved your awesomeness',
        points=50,
        progression_target=100,
        category=Category.objects.create(name='Gold Badges', description='These are the top badges'),
    )

Awarding a badge
~~~~~~~~~~~~~~~~

You can manually award a ``Badge`` instance using ``Badge.award()``.

.. code:: python

    from django_gamification.models import Badge

    badge = Badge.objects.first()
    # badge.acquired = False

    badge.award()
    # badge.acquired = True

UnlockableDefinitions and Unlockables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creating a new unlockable
~~~~~~~~~~~~~~~~~~~~~~~~~

By creating a new ``UnlockableDefinition``, Django Gamification will
automatically create ``Unlockable`` instances for all your current
``GamificationInterfaces`` with ``Unlockable.name``,
``Unlockable.description``, ``Unlockable.points_required`` mimicking the
fields on the ``UnlockableDefinition``.

.. code:: python

    from django_gamification.models import UnlockableDefinition

    UnlockableDefinition.objects.create(
        name='Some super sought after feature',
        description='You unlocked a super sought after feature',
        points_required=100
    )

Contributing
------------

Submitting an issue or feature request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you find an issue or have a feature request please open an issue at
`Github Django Gamification
Repo <https://github.com/mattjegan/django-gamification>`__.

Working on issues
~~~~~~~~~~~~~~~~~

If you think that you can fix an issue or implement a feature, please
make sure that it isn't assigned to someone or if it is you may ask for
an update.

Once an issue is complete, open a pull request so that your contribution
can be reviewed. A TravisCI build will run and be attached to your pull
request. Your code must pass these checks.

Get Started!
~~~~~~~~~~~~

Ready to contribute? Here's how to set up `django-gamification` for local
development.

1. Fork the `django-gamification` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/django-gamification.git

3. Install your local copy into a virtualenv. Assuming you have
   virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv django-gamification
    $ cd django-gamification/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

        $ py.test
        $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.


Helping others
~~~~~~~~~~~~~~

At all times, please be polite with others who are working on issues. It
may be their first ever patch and we want to foster a friendly and
familiar open source environment.

.. |PyPI version| image:: https://badge.fury.io/py/django-gamification.svg
   :target: https://badge.fury.io/py/django-gamification
.. |Build Status| image:: https://travis-ci.org/mattjegan/django-gamification.svg?branch=master
   :target: https://travis-ci.org/mattjegan/django-gamification
