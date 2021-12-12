from __future__ import unicode_literals
import re


class ParsedURL():
    _parts = []
    _signature = (0, 0) 
    _domain = None
    def __init__(self, url):
        self.url = url
        self._parts = []
        path_re = re.search(r'https?://[^/?#]+/([^?#]+)', url)
        if path_re:
            elems = path_re.group(1).strip('/').split('/')
            self._parts = list(zip(['/'] * len(elems), elems))
        path_parts = len(self._parts)
        qs_re = re.search(r'https?://[^?#]+\?([^#]+)', url)
        if qs_re:
            elems = qs_re.group(1).strip('=?&').split('&')
            for i, part in enumerate(elems):
                sep = '?' if i == 0 else '&'
                if '=' in part:
                    par, val = part.split('=')
                    self._parts.append((sep, par))
                    self._parts.append(('=', val))
                else:
                    self._parts.append((sep, part))
        self._signature = (path_parts, len(self._parts) - path_parts)
        self._domain = None
        domain_re = re.search(r'^((https?://)[^/\?\#]+)', url, re.U)
        if domain_re:
            self._domain = domain_re.group(1)

    @property
    def parts(self):
        return self._parts

    @property
    def signature(self):
        return self._signature

    @property
    def domain(self):
        return self._domain
