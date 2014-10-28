=====================
django-potato-captcha
=====================

A very simple, clever Django captcha application. This provides a wrapper
around ``django.forms.Form`` and ``django.forms.ModelForm``, which creates
two honeypot fields:


1. ``tuber``: This field should always be blank.
2. ``sprout``: This field's value should always be ``potato``, which should
   get set by JavaScript in your template.


Usage
-----

In your ``forms.py``::

    from django.forms import forms
    from django_potato_captcha.forms import (PotatoCaptchaForm,
                                             PotatoCaptchaModelForm)


    class FrenchFriedForm(PotatoCaptchaForm):
        text = forms.CharField()


    class FrenchFriedModelForm(PotatoCaptchaForm):
        text = forms.CharField()

        class Meta:
            model = Fry


In your template::

        <style type="text/css">
            .potato-captcha {
                left: -9999px;
                opacity: 0;
                position: absolute;
                visibility: hidden;
            }
        </style>
        <form method="post">
            {% csrf_token %}
            {{ form.tuber }}
            {{ form.sprout }}
            <button type="submit">{{ _('Submit') }}</button>
        </form>
        <script type="text/javascript">
            document.querySelector('input[name=sprout]').value = 'potato';
        </script>


Installation
------------

Make sure you have ``homebrew`` and ``virtualenv``/``virtualenvwrapper``
installed::

    curl -s https://raw.github.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL
    source ~/.profile

Then install::

    mkvirtualenv --no-site-packages potato
    workon potato
    python setup.py install

Or install directly from PyPi::

    pip install django_potato_captcha


Testing
-------

Simply run this command::

    nosetests
