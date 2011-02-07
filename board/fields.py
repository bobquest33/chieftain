#!/usr/bin/env python
# encoding: utf-8
"""
fields.py

Created by Paul Bagwell on 2011-02-07.
Copyright (c) 2011 Paul Bagwell. All rights reserved.
"""

from django.conf import settings
from django import forms
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from board.widgets import ReCaptcha, captcha

__all__ = ['ReCaptchaField']

class ReCaptchaField(forms.CharField):
    default_error_messages = {
        'captcha_invalid': _(u'Invalid captcha')
    }

    def __init__(self, *args, **kwargs):
        self.widget = ReCaptcha
        self.required = True
        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, values):
        super(ReCaptchaField, self).clean(values[1])
        recaptcha_challenge_value = smart_unicode(values[0])
        recaptcha_response_value = smart_unicode(values[1])
        print recaptcha_challenge_value, \
            recaptcha_response_value, settings.RECAPTCHA_PRIVATE_KEY
        check_captcha = captcha.submit(recaptcha_challenge_value, 
            recaptcha_response_value, settings.RECAPTCHA_PRIVATE_KEY, {})
        if not check_captcha.is_valid:
            raise forms.util.ValidationError(self.error_messages['captcha_invalid'])
        return values[0]