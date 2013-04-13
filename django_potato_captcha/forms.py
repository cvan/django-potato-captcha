import logging

from django import forms
from django.utils.translation import ugettext as _

log = logging.getLogger('captcha')


class PotatoCaptcha(object):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(PotatoCaptcha, self).__init__(*args, **kwargs)

        self.has_potato_recaptcha = True

        # Skip PotatoCaptcha for authenticated users. `self.request.user`
        # refers to an instance of `django.contrib.auth.models.user`.
        if self.request and self.request.user.is_authenticated():
            del self.fields['tuber']
            del self.fields['sprout']
            self.has_potato_recaptcha = False

    def clean(self):
        data = self.cleaned_data

        if (self.has_potato_recaptcha and
            (data.get('tuber') or data.get('sprout') != 'potato')):
            log.info(u'Spammer thwarted: %s' %
                     self.request.META.get('REMOTE_ADDR'))
            raise forms.ValidationError(_('Form could not be submitted.'))

        return data


PotatoInput = lambda: forms.TextInput(attrs={'class': 'potato-captcha'})


class PotatoCaptchaForm(PotatoCaptcha, forms.Form):
    # This field's value should always be blank (spammers are dumb).
    tuber = forms.CharField(required=False, label=None, widget=PotatoInput())

    # This field's value should always be 'potato' (set by JS).
    sprout = forms.CharField(required=False, label=None, widget=PotatoInput())


class PotatoCaptchaModelForm(PotatoCaptcha, forms.ModelForm):
    tuber = forms.CharField(required=False, label=None, widget=PotatoInput())
    sprout = forms.CharField(required=False, label=None, widget=PotatoInput())
