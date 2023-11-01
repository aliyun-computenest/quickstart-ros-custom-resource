# -*- coding: utf-8 -*-

import re


SPLIT_PATTERN = re.compile('([A-Z]+)')


def camel_style_to_c_style(s):
    if not s:
        return s
    tokens = []
    for i, token in enumerate(SPLIT_PATTERN.split(s)):
        if i % 2 == 0:
            tokens.append(token)
        else:
            if i > 1:
                tokens.append('_')
            tokens.append(token.lower())
    return ''.join(tokens)
