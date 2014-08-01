
import re
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

class MobileParser(object):

    DEFAULT_UA_STRINGS = (
        'Android',
        'BlackBerry',
        'IEMobile',
        'Maemo',
        'Opera Mini',
        'SymbianOS',
        'WebOS',
        'Windows Phone',
        'iPhone',
        'iPod',
        'iPad'
    )

    BYPASS_URL = (
        r'^/admin/',
        r'^/api/',
        r'^/info/',
        r'^/u/',
    )

    WHITE_LIST = (
        r'^/$',
        r'^/photos$',
        r'^/pros$',
        r'^/products$',
        r'^/ideabooks',
        r'^/my$',
        r'^/advice$',
    )

    def __init__(self):
        self._cache = {}
        self._cache_url = {}
        self._cache_list = {}

    def detect_mobile(self, user_agent):
        try:
            return self._cache[user_agent]
        except KeyError:
            for lookup in MobileParser.DEFAULT_UA_STRINGS:
                if lookup in user_agent:
                    self._cache[user_agent] = True
                    break
            else:
                self._cache[user_agent] = False
        return self._cache[user_agent]

    def is_white_list(self, path):
        try:
            return self._cache_list[path]
        except KeyError:
            for lookup in MobileParser.WHITE_LIST:
                if re.match(lookup, path):
                    self._cache_list[path] = True
                    break
                else:
                    self._cache_list[path] = False
        return self._cache_list[path]

    def is_bypass(self, path):
        try:
            return self._cache_url[path]
        except KeyError:
            for lookup in MobileParser.BYPASS_URL:
                if re.match(lookup, path):
                    self._cache_url[path] = True
                    break
                else:
                    self._cache_url[path] = False
        return self._cache_url[path]

parser = MobileParser()

class MobileRedirectMiddleware(object):

    def process_request(self, request):

        DEBUG_INFO = False
        #DEBUG_INFO = True
        if DEBUG_INFO:
            print "headers:"
            for key in request.META:
                if key.startswith('HTTP'):
                    print key, request.META[key]
            print 'content-type', request.META.get('CONTENT_TYPE')
            print 'body:'
            print request.body

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_mobile = parser.detect_mobile(user_agent)
        template = 'web.html'
        if is_mobile:
            template = 'mobile.html'
        request.is_mobile = is_mobile

        if parser.is_white_list(request.path):
            return render_to_response(template)



