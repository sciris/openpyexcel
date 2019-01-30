from __future__ import absolute_import
# Copyright (c) 2010-2019 openpyexcel

from openpyexcel.compat import unicode

from openpyexcel.descriptors.serialisable import Serialisable
from openpyexcel.descriptors import (
    Sequence,
    Alias
)


class AuthorList(Serialisable):

    tagname = "authors"

    author = Sequence(expected_type=unicode)
    authors = Alias("author")

    def __init__(self,
                 author=(),
                ):
        self.author = author
