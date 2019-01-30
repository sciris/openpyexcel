# Copyright (c) 2010-2019 openpyexcel


from openpyexcel.compat.numbers import NUMPY, PANDAS
from openpyexcel.xml import DEFUSEDXML, LXML
from openpyexcel.workbook import Workbook
from openpyexcel.reader.excel import load_workbook
import openpyexcel._constants as constants

# Expose constants especially the version number

__author__ = constants.__author__
__author_email__ = constants.__author_email__
__license__ = constants.__license__
__maintainer_email__ = constants.__maintainer_email__
__url__ = constants.__url__
__version__ = constants.__version__
