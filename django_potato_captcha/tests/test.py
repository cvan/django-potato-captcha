# Initialize Django settings and test environment.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_potato_captcha.settings'

from django.test.utils import setup_test_environment
setup_test_environment()

from django import forms
from django.db import models
from django.test import TestCase

import mock

from django_potato_captcha.forms import (PotatoCaptchaForm,
                                         PotatoCaptchaModelForm)


class Potato(models.Model):
    spud = models.TextField(null=True, blank=True)


class FormWithPotatoCaptcha(PotatoCaptchaForm):
    message = forms.CharField(required=False)


class ModelFormWithPotatoCaptcha(PotatoCaptchaModelForm):
    message = forms.CharField(required=False)

    class Meta:
        model = Potato


class PotatoCaptchaTestCase(TestCase):

    def setUp(self):
        self.request = mock.Mock()
        self.request.META = {'REMOTE_ADDR': '86.75.3.09'}
        self.request.user.is_authenticated.return_value = False
        self.data = {'tuber': '', 'sprout': 'potato'}


class TestPotatoCaptchaForm(PotatoCaptchaTestCase):
    form_class = FormWithPotatoCaptcha

    @property
    def form(self):
        if not hasattr(self, '_form'):
            self._form = self.form_class(self.data, request=self.request)
        return self._form

    def test_success_authenticated(self):
        self.request.user.is_authenticated.return_value = True
        self.data = {}
        self.assertEqual(self.form.is_valid(), True, self.form.errors)
        self.assertEqual(self.form.has_potato_recaptcha, False)

    def test_success_anonymous(self):
        self.assertEqual(self.form.is_valid(), True, self.form.errors)
        self.assertEqual(self.form.has_potato_recaptcha, True)

    def test_success_with_message_authenticated(self):
        self.request.user.is_authenticated.return_value = True
        self.data = {'message': 'yolo'}
        self.assertEqual(self.form.is_valid(), True, self.form.errors)

    def test_success_with_message_anonymous(self):
        self.data['message'] = 'yolo'
        self.assertEqual(self.form.is_valid(), True, self.form.errors)

    @mock.patch('django_potato_captcha.forms.log.info')
    def test_error_anonymous_bad_tuber(self, log_info_mock):
        self.data['tuber'] = 'HAMMMMMMMMMMMMM'
        self.assertEqual(self.form.is_valid(), False)
        log_info_mock.assert_called_with('Spammer thwarted: 86.75.3.09')

    def test_error_anonymous_bad_sprout(self):
        self.data['sprout'] = ''
        self.assertEqual(self.form.is_valid(), False)

    def test_error_anonymous_bad_tuber_and_sprout(self):
        self.data = {}
        self.assertEqual(self.form.is_valid(), False)


class TestPotatoCaptchaModelForm(TestPotatoCaptchaForm):
    form_class = ModelFormWithPotatoCaptcha

    def test_success_with_model_change_authenticated(self):
        self.request.user.is_authenticated.return_value = True
        self.data = {'message': 'yolo', 'spud': 'swag'}
        self.assertEqual(self.form.is_valid(), True, self.form.errors)

    def test_success_with_model_change_anonymous(self):
        self.data.update(message='yolo', spud='swag')
        self.assertEqual(self.form.is_valid(), True, self.form.errors)
