from __future__ import absolute_import
# Copyright (c) 2010-2019 openpyexcel

from openpyexcel.xml.constants import CHART_NS

from openpyexcel.descriptors.serialisable import Serialisable
from openpyexcel.descriptors.excel import Relation


class ChartRelation(Serialisable):

    tagname = "chart"
    namespace = CHART_NS

    id = Relation()

    def __init__(self, id):
        self.id = id
