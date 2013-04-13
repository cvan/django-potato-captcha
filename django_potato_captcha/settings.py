DATABASES = {
    'default': {
        'NAME': 'test-potato',
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}

INSTALLED_APPS = ['django.contrib.sessions']

DJANGO_PARANOIA_REPORTERS = ['django_paranoia.reporters.log']
