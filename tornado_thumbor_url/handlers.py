#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import tornado.web

from libthumbor.crypto import CryptoURL


HTTP_BAD_REQUEST = 400


class ThumborUrlException(Exception):
    pass


class GenerateThumborUrlHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        try:
            self.set_header('Content-Type', 'text/plain')
            self.write(self.thumbor_complete_url())
        except (ThumborUrlException, ValueError, KeyError) as e:
            self.set_status(HTTP_BAD_REQUEST)
            logging.warning(e.message)
            self.write(e.message)
        self.flush()

    def thumbor_complete_url(self):
        arguments = self.extract_arguments()
        params = self.build_crypto_params(arguments)
        return self.settings['thumbor_server_url'] + self.generate_url(params)

    def extract_arguments(self):
        accepted_arguments = [
            'width',
            'height',
            'crop_top',
            'crop_left',
            'crop_right',
            'crop_bottom',
            'meta',
            'filters',
            'smart',
            'halign',
            'valign',
            'flip',
            'flop',
            'image_url'
        ]
        arguments = {}
        for argument_name in accepted_arguments:
            value = self.get_argument(argument_name, None)
            if value != None:
                arguments[argument_name] = value
        return arguments

    def build_crypto_params(self, arguments):
        try:
            if 'width' in arguments:
                arguments['width'] = int(arguments['width'])
        except ValueError as e:
            raise ThumborUrlException("The width value '%s' is not an"\
                    " integer." % arguments['width'])

        try:
            if 'height' in arguments:
                arguments['height'] = int(arguments['height'])
        except ValueError as e:
            raise ThumborUrlException("The height value '%s' is not an"\
                    " integer." % arguments['height'])

        try:
            if 'crop_top' in arguments or 'crop_left' in arguments \
                    or 'crop_right' in arguments or 'crop_bottom' in arguments:
                arguments['crop'] = ((int(arguments['crop_left']), 
                    int(arguments['crop_top'])), (int(arguments['crop_right']),
                        int(arguments['crop_bottom'])))
        except KeyError as e:
            raise ThumborUrlException("Missing values for cropping. Expected "\
                    "all 'crop_left', 'crop_top', 'crop_right', 'crop_bottom'"\
                    " values.")
        except ValueError as e:
            raise ThumborUrlException("Invalid values for cropping. Expected "\
                    "all 'crop_left', 'crop_top', 'crop_right', 'crop_bottom'"\
                    " to be integers.")
        return arguments

    def generate_url(self, parameters):
        crypto = CryptoURL(self.settings['thumbor_security_key'])
        return crypto.generate(**parameters).strip("/")
