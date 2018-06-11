# Copyright (C) 2018 OpenIO SAS, as part of OpenIO SDS
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.

from urllib import quote_plus, unquote_plus


def encode_fullpath(account, container, path, version, content_id):
    if not account or not container or not path or not version \
            or not content_id:
        raise ValueError("Can't encode fullpath")
    return '{0}/{1}/{2}/{3}/{4}'.format(quote_plus(account),
                                        quote_plus(container),
                                        quote_plus(path),
                                        quote_plus(str(version)),
                                        quote_plus(content_id))


def decode_fullpath(fullpath):
    fp = fullpath.split('/')
    if len(fp) != 5:
        raise ValueError("'fullpath': Wrong format")
    decoded = list()
    for part in fp:
        decoded.append(unquote_plus(part))
    return tuple(decoded)