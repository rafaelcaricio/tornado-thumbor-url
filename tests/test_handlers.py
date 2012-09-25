#!/usr/bin/python
# -*- coding: utf-8 -*-

# libthumbor - python extension to thumbor
# http://github.com/rafaelcaricio/django-thumbor-url

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 Rafael Caricio rafael@caricio.com

import os
import urllib
import tornado.web

from libthumbor.crypto import CryptoURL
from tornado.testing import AsyncHTTPTestCase

from tornado_thumbor_url.handlers import GenerateThumborUrlHandler


HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405
HTTP_OK = 200
HTTP_BAD_REQUEST = 400

THUMBOR_SECURITY_KEY = 'my-security-key'
THUMBOR_SERVER = 'http://local.machine.com/'


class TestApp(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/gen_url/?', GenerateThumborUrlHandler),
        ]
        super(TestApp, self).__init__(handlers, **{
                'thumbor_server_url': THUMBOR_SERVER,
                'thumbor_security_key': THUMBOR_SECURITY_KEY
            })


class GenerateThumborUrlLHandlerTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return TestApp()

    def get(self, path, **querystring):
        url = self.get_url(path)
        if querystring:
            url = "%s?%s" % (url, urllib.urlencode(querystring))
        self.http_client.fetch(url, self.stop)
        return self.wait()

    def post(self, path, **querystring):
        url = self.get_url(path)
        if querystring:
            querystring = urllib.urlencode(querystring)
        self.http_client.fetch(url, self.stop, method='POST', body=querystring)
        return self.wait()

    def test_without_url_param(self):
        response = self.get('/gen_url/')
        assert HTTP_BAD_REQUEST == response.code, "Got %d" % response.code

    def test_generate_url_with_params_via_post(self):
        response = self.post('/gen_url/', image_url='globo.com/media/img/my_image.jpg')
        assert HTTP_METHOD_NOT_ALLOWED == response.code, "Got %d" % response.code

    def test_generate_url_with_params_via_get(self):
        crypto = CryptoURL(THUMBOR_SECURITY_KEY)

        response = self.get('/gen_url/', image_url='globo.com/media/img/my_image.jpg')

        assert HTTP_OK == response.code, "Got %d" % response.code
        assert response.body == THUMBOR_SERVER + crypto.generate(image_url='globo.com/media/img/my_image.jpg').strip("/")

    def test_passing_invalid_value_for_width(self):
        url_query = {
            'image_url': 'globo.com/media/img/my_image.jpg',
            'width': 1.2
        }

        response = self.get('/gen_url/', **url_query)

        assert HTTP_BAD_REQUEST == response.code, "Got %d" % response.code
        assert "The width value '1.2' is not an integer." == response.body

    def test_passing_invalid_value_for_height(self):
        url_query = {
            'image_url': 'globo.com/media/img/my_image.jpg',
            'height': 's'
        }

        response = self.get('/gen_url/', **url_query)

        assert HTTP_BAD_REQUEST == response.code, "Got %d" % response.code
        assert "The height value 's' is not an integer." == response.body

    def test_passing_invalid_aligns(self):
        url_query = {
            'image_url': 'globo.com/media/img/my_image.jpg',
            'halign': 'sss'
        }

        response = self.get('/gen_url/', **url_query)

        assert HTTP_BAD_REQUEST == response.code, "Got %d" % response.code

    def test_passing_only_one_crop_value(self):
        response = self.get('/gen_url/?', image_url='globo.com/media/img/my_image.jpg', crop_left=100)

        assert HTTP_BAD_REQUEST == response.code, "Got %d" % response.code
        assert "Missing values for cropping. Expected all 'crop_left', 'crop_top', 'crop_right', 'crop_bottom' values." == response.body

    def test_passing_only_one_crop_with_invalid_value(self):
        url_query = {
            'image_url': 'globo.com/media/img/my_image.jpg',
            'crop_top': 'bla',
            'crop_left': 200,
            'crop_right': '1',
            'crop_bottom': 'blas'
        }

        response = self.get('/gen_url/', **url_query)

        assert HTTP_BAD_REQUEST == response.code, "Got %d" % response.code
        assert "Invalid values for cropping. Expected all 'crop_left', 'crop_top', 'crop_right', 'crop_bottom' to be integers." == response.body

    def test_passing_various_erroneous_values(self):
        url_query = {
            'image_url': 'globo.com/media/img/my_image.jpg',
            'crop_left': 100,
            'width': 'aaa',
            'height': 123
        }

        response = self.get('/gen_url/', **url_query)

        assert HTTP_BAD_REQUEST == response.code, "Got %d" % response.code

    def test_passing_all_params(self):
        image_args = {
            'image_url': 'globo.com/media/img/my_image.jpg',
            'halign': 'left',
            'valign': 'middle',
            'meta': True,
            'smart': True,
            'width': 400,
            'height': 400,
            'flip': True,
            'flop': True
        }
        url_query = {}
        url_query.update(image_args)
        url_query.update({
            'crop_top': 100,
            'crop_left': 100,
            'crop_bottom': 200,
            'crop_right': 200
        })
        image_args.update({'crop': ((100,100), (200,200)) })

        crypto = CryptoURL(THUMBOR_SECURITY_KEY)

        response = self.get('/gen_url/', **url_query)

        assert HTTP_OK == response.code, "Got %d" % response.code
        assert response.body == THUMBOR_SERVER + crypto.generate(**image_args).strip("/")

