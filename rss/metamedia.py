#! /usr/bin/env python

# Author: Victor Terron (c) 2013
# License: GNU GPLv3

import collections
import json
import requests

class MetaMedia(object):
    """ Python interface to the MetaMedia API """

    AXES_URL = "http://localhost/index.php/api/get-axes"
    LICENSES_URL = "http://localhost/index.php/api/get-licenses"
    PUT_MEDIA_URL = "http://localhost/index.php/api/put-media"

    def __init__(self, user, password):
        self.auth_data = {'user' : user, 'password' : password}

    def get_axes(self):
        """ A generator that yields the axes as named tuples """

        data = 'json=' + json.dumps(self.auth_data)
        headers = {'Content-Type': 'application/json'}
        kwargs = dict(headers=headers, data=data)
        r = requests.get(self.AXES_URL, **kwargs)
        axes = r.json()

        Axis = collections.namedtuple('Axis', axes[0].keys())
        for axis in axes:
            yield Axis(*axis.values())

    def get_licenses(self):
        """ A generator that yields the licenses as named tuples """

        data = 'json=' + json.dumps(self.auth_data)
        headers = {'Content-Type': 'application/json'}
        kwargs = dict(headers=headers, data=data)
        r = requests.get(self.LICENSES_URL, **kwargs)
        licenses = r.json()

        License = collections.namedtuple('License', licenses[0].keys())
        for license in licenses:
            yield License(*license.values())

    def put_media(self, title, excerpt, content, creator, url, license, lang):
        """ Add a media to the database.

        The 'title', 'excerpt', 'content', 'creator' (refers to the original
        author) and 'url' arguments are expected to be strings. 'license' must
        be an object of the class License (see MetaMedia.get_license() method)
        or, at the very least, have an attribute named 'id' which stores the ID
        of the license in the database. Finally, 'lang' must be a string with
        the two-letter code, in upper-case ('EN', 'DE', 'ES') of the language
        of the media.

        """

        request_data = {'type' : 1, 'title' : title, 'excerpt' : excerpt,
                        'content' : content, 'original-creator' : creator,
                        'original-url' : url, 'license-id' : license.id,
                        'language' : lang}

        request_data.update(self.auth_data)
        data = 'json=' + json.dumps(request_data)
        headers = {'Content-Type': 'application/json'}
        kwargs = dict(headers=headers, data=data)
        requests.put(self.PUT_MEDIA_URL, **kwargs)

if __name__ == "__main__":

    metamedia = MetaMedia('anonymous', 'qwerty')

    print "Axes:"
    for axis in metamedia.get_axes():
        print axis.name, axis.left_term, axis.right_term

    print
    print "Licenses:"
    for license in metamedia.get_licenses():
        print license.name, license.url

