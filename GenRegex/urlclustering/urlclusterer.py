from __future__ import unicode_literals
import re
from collections import defaultdict
from urlclustering.urltree import URLTreeNode
from urlclustering.parsedurl import ParsedURL

def _cluster_same_signature_urls(parsed_urls, min_cluster_size):
    patterns = []
    if len(parsed_urls) == 0:
        return patterns
    max_reductions = len(parsed_urls[0].parts)
    root = URLTreeNode()
    for parsed in parsed_urls:
        root.add_url(parsed)
    leafs = root.leafs()
    while leafs:
        bestleaf = max(leafs,key=lambda x:len(x['urls']) * (max_reductions - x['reductions']) ** 2)
        if len(bestleaf['urls']) >= min_cluster_size:
            patterns.append((bestleaf['pattern'],bestleaf['h_pattern']))
        leafs.remove(bestleaf)
        remaining_leafs = []
        for leaf in leafs:
            leaf['urls'] -= bestleaf['urls']
            if leaf['urls']:
                remaining_leafs.append(leaf)
        leafs = remaining_leafs
    return patterns

def _cluster_same_domain_urls(parsed_urls, min_cluster_size):
    url_map = defaultdict(list)
    for parsed in parsed_urls:
        url_map[parsed.signature].append(parsed)
    clusters = defaultdict(list)
    unclustered = []
    for parsed_urls in url_map.values():
        if len(parsed_urls) < min_cluster_size:
            unclustered.extend([x.url for x in parsed_urls])
            continue
        patterns = _cluster_same_signature_urls(parsed_urls, min_cluster_size)
        for (pattern, h_pattern) in patterns:
            remaining_urls = []
            for parsed in parsed_urls:
                if re.search(pattern, parsed.url):
                    clusters[(pattern, h_pattern)].append(parsed.url)
                else:
                    remaining_urls.append(parsed)
            parsed_urls = remaining_urls
        unclustered.extend(x.url for x in parsed_urls)

    return {'clusters': clusters, 'unclustered': unclustered}

def cluster_urls(urls, min_cluster_size=10):
    if min_cluster_size < 2:
        min_cluster_size = 2
    res = {'clusters': {}, 'unclustered': []}
    parsed_urls = []
    for url in urls:
        parsed_urls.append(ParsedURL(url))
    by_domain = defaultdict(list)
    for parsed in parsed_urls:
        try:
            by_domain[parsed.domain].append(parsed)
        except:
            res['unclustered'].append(parsed.url)
    for domain, parsed_urls in by_domain.items():
        c_res = _cluster_same_domain_urls(parsed_urls, min_cluster_size)
        res['clusters'].update({('%s%s' % (domain, k[0]),'%s%s' % (domain, k[1])): v for k, v in c_res['clusters'].items()})
        res['unclustered'].extend(c_res['unclustered'])
    return res
