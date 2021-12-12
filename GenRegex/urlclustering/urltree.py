from __future__ import unicode_literals
import re

class URLTreeNode(dict):
    REDUCED_NUM_LITERAL = '(.+)'
    REDUCED_PATH_LITERAL = '([^/]+)'
    REDUCED_PARAM_LITERAL = '([^&=?]+)'
    def __init__(self, iterable=(), r='', h='', reductions=0):
        self.r = r 
        self.h = h  
        self.urls = set()  
        self.reductions = reductions  
        dict.__init__(self, iterable)
    def __repr__(self):
        if len(self) == 0:
            return '%s -> %s urls with %s reductions' % (
                self.r, len(self.urls), self.reductions)
        return '\n'.join(repr(self[k]) for k in self)

    def leafs(self):
        leafs = []
        if len(self) == 0:
            return [{'pattern': self.r,
                     'h_pattern': self.h,
                     'urls': self.urls,
                     'reductions': self.reductions}]
        for key in self:
            leafs.extend(self[key].leafs())
        return leafs

    def _reduced(self, elem, separator):
        if re.search(r'^.+$', elem):
            return URLTreeNode.REDUCED_NUM_LITERAL, '[..]'
        elif separator == '/':
            return URLTreeNode.REDUCED_PATH_LITERAL, '[...]'
        else:
            return URLTreeNode.REDUCED_PARAM_LITERAL, '[...]'

    def _re_sep(self, separator):
        return '/?\?' if separator == '?' else separator

    def add_url(self, parsed_url, position=0):
        if position >= len(parsed_url.parts):
            self.urls.add(parsed_url.url)
        else:
            sep, elem = parsed_url.parts[position]
            if elem not in self:
                self[elem] = URLTreeNode(
                    r='%s%s%s' % (self.r, self._re_sep(sep), re.escape(elem)),
                    h='%s%s%s' % (self.h, sep, elem),
                    reductions=self.reductions
                )
            self[elem].add_url(parsed_url, position+1)
            reduced, reduced_h = self._reduced(elem, sep)
            if reduced not in self:
                self[reduced] = URLTreeNode(
                    r='%s%s%s' % (self.r, self._re_sep(sep), reduced),
                    h='%s%s%s' % (self.h, sep, reduced_h),
                    reductions=self.reductions+1
                )
            self[reduced].add_url(parsed_url, position+1)
