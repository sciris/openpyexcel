from __future__ import absolute_import
# Copyright (c) 2010-2019 openpyexcel

from openpyexcel.descriptors.serialisable import Serialisable
from openpyexcel.descriptors import (
    Sequence
)
from openpyexcel.descriptors.excel import (
    Relation,
)

class ExternalReference(Serialisable):

    tagname = "externalReference"

    id = Relation()

    def __init__(self, id):
        self.id = id
