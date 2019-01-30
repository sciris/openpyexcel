.. image:: https://coveralls.io/repos/bitbucket/openpyexcel/openpyexcel/badge.svg?branch=default
    :target: https://coveralls.io/bitbucket/openpyexcel/openpyexcel?branch=default
    :alt: coverage status

Introduction
------------

openpyexcel is a Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.

It was born from lack of existing library to read/write natively from Python
the Office Open XML format.

All kudos to the PHPExcel team as openpyexcel was initially based on PHPExcel.


Security
--------

By default openpyexcel does not guard against quadratic blowup or billion laughs
xml attacks. To guard against these attacks install defusedxml.

Mailing List
------------

The user list can be found on http://groups.google.com/group/openpyexcel-users


Sample code::

    from openpyexcel import Workbook
    wb = Workbook()

    # grab the active worksheet
    ws = wb.active

    # Data can be assigned directly to cells
    ws['A1'] = 42

    # Rows can also be appended
    ws.append([1, 2, 3])

    # Python types will automatically be converted
    import datetime
    ws['A2'] = datetime.datetime.now()

    # Save the file
    wb.save("sample.xlsx")


Documentation
-------------

The documentation is at: https://openpyexcel.readthedocs.io

* installation methods
* code examples
* instructions for contributing

Release notes: https://openpyexcel.readthedocs.io/en/stable/changes.html
