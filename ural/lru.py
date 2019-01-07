# =============================================================================
# Ural LRU Function
# =============================================================================
#
# A function returning the url parts in the hierarchical order.
#
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

from ural.ensure_protocol import ensure_protocol
from ural.patterns import IRRELEVANT_QUERY_COMBOS, IRRELEVANT_QUERY_RE, IRRELEVANT_SUBDOMAIN_RE


def parsed_url_to_lru(parsed_url):
    scheme, netloc, path, query, fragment = parsed_url
    lru = []
    lru.append('s:' + scheme)

    # Parsing domain & port
    netloc = netloc.split(':')
    if len(netloc) == 2:
        port = netloc[1]
        lru.append('t:' + port)
    for element in reversed(netloc[0].split('.')):
        lru.append('h:' + element)

    # Parsing the path
    for element in path.split('/'):
        if element:
            lru.append('p:' + element)
    if query and query[0]:
        for element in query.split('&'):
            lru.append('q:' + element)
    if fragment and fragment[0]:
        lru.append('f:' + fragment)

    return lru


def lru(url, default_protocol='http'):
    """
    Function returning the parts of the given url in the hierarchical order (lru).

    Args:
        url (str): Target URL as a string.
        default_protocol (str, optional): Protocol to add if there is none.
            Defaults to `'http'`.

    Returns:
        list: The lru, with a prefix identifying the type of each part.
    """

    full_url = ensure_protocol(url, protocol=default_protocol)
    return parsed_url_to_lru(urlsplit(full_url))
