#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import tornado.web

from libthumbor.crypto import CryptoURL


HTTP_BAD_REQUEST = 400


class GenerateThumborUrlHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        crypto = CryptoURL(self.settings['thumbor_security_key'])

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
        arguments= {}
        for argument_name in accepted_arguments:
            argument = self.get_argument(argument_name, None)
            if argument != None:
                arguments[argument_name] = argument

        error_message = None

        try:
            if 'width' in arguments:
                arguments['width'] = int(arguments['width'])
        except ValueError, e:
            error_message = "The width value '%s' is not an integer." % \
                arguments['width']

        try:
            if 'height' in arguments:
                arguments['height'] = int(arguments['height'])
        except ValueError, e:
            error_message = "The height value '%s' is not an integer." % \
                arguments['height']

        try:
            if 'crop_top' in arguments or 'crop_left' in arguments or 'crop_right' in arguments or 'crop_bottom' in arguments:
                arguments['crop'] = ((int(arguments['crop_left']), int(arguments['crop_top'])),
                        (int(arguments['crop_right']), int(arguments['crop_bottom'])))
        except KeyError, e:
            error_message = "Missing values for cropping. Expected all 'crop_left', 'crop_top', 'crop_right', 'crop_bottom' values."
        except ValueError, e:
            error_message = "Invalid values for cropping. Expected all 'crop_left', 'crop_top', 'crop_right', 'crop_bottom' to be integers."

        if error_message is not None:
            logging.warning(error_message)
            self.set_status(HTTP_BAD_REQUEST)
            self.write(error_message)
        else:
            try:
                self.set_header('Content-Type', 'text/plain')
                self.write(self.settings['thumbor_server_url'] + crypto.generate(**arguments).strip("/"))
            except (ValueError, KeyError), e:
                error_message = str(e)
                self.set_status(HTTP_BAD_REQUEST)
                logging.warning(error_message)
                self.write(error_message)
        self.flush()
