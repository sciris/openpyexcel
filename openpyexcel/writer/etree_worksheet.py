from __future__ import absolute_import
# Copyright (c) 2010-2019 openpyexcel

from operator import itemgetter

from openpyexcel.compat import safe_string
from openpyexcel.comments.comment_sheet import CommentRecord
from openpyexcel.xml.functions import Element, SubElement
from openpyexcel import LXML
from openpyexcel.utils.datetime import to_excel, days_to_time
from datetime import timedelta


def get_rows_to_write(worksheet):
    """Return all rows, and any cells that they contain"""
    # order cells by row
    rows = {}
    for (row, col), cell in worksheet._cells.items():
        rows.setdefault(row, []).append((col, cell))

    # add empty rows if styling has been applied
    for row_idx in worksheet.row_dimensions:
        if row_idx not in rows:
            rows[row_idx] = []

    return sorted(rows.items())


def write_rows(xf, worksheet):
    """Write worksheet data to xml."""

    all_rows = get_rows_to_write(worksheet)
    max_column = worksheet.max_column

    with xf.element("sheetData"):
        for row_idx, row in sorted(all_rows):
            row = sorted(row, key=itemgetter(0))
            write_row(xf, worksheet, row, row_idx, max_column)


def write_row(xf, worksheet, row, row_idx, max_column):

    attrs = {'r': '%d' % row_idx, 'spans': '1:%d' % max_column}
    dims = worksheet.row_dimensions
    if row_idx in dims:
        row_dimension = dims[row_idx]
        attrs.update(dict(row_dimension))

    with xf.element("row", attrs):

        for col, cell in row:
            if (
                cell._value is None
                and not cell.has_style
                and not cell._comment
                ):
                continue
            write_cell(xf, worksheet, cell, cell.has_style)


def etree_write_cell(xf, worksheet, cell, styled=None):

    coordinate = cell.coordinate
    attributes = {'r': coordinate}
    if styled:
        attributes['s'] = '%d' % cell.style_id

    value = cell._value
    
    if cell.data_type != 'f':
        attributes['t'] = cell.data_type
    else:
        if isinstance(value, tuple): # CK: fix up data types for formulas
            tmpval,data_type = cell._bind_value(value[1], return_output=True) # WARNING, HACKY
            attributes['t'] = data_type

    if cell.data_type == "d":
        if cell.parent.parent.iso_dates:
            if isinstance(value, timedelta):
                value = days_to_time(value)
            value = value.isoformat()
        else:
            attributes['t'] = "n"
            value = to_excel(value, worksheet.parent.epoch)

    if cell._comment is not None:
        comment = CommentRecord.from_cell(cell)
        worksheet._comments.append(comment)

    el = Element("c", attributes)
    if value is None or value == "":
        xf.write(el)
        return

    if cell.data_type == 'f':
        shared_formula = worksheet.formula_attributes.get(coordinate, {})
        formula = SubElement(el, 'f', shared_formula)
        if value is not None: # CK: Allow writing formulas and values
            if isinstance(value, tuple):
                formula.text = value[0][1:]
                value = cell._infer_value(value[1])
            else:
                formula.text = value[1:]
                value = None

    if cell.data_type == 's':
        value = worksheet.parent.shared_strings.add(value)
    cell_content = SubElement(el, 'v')
    if value is not None:
        cell_content.text = safe_string(value)

    if cell.hyperlink:
        worksheet._hyperlinks.append(cell.hyperlink)

    xf.write(el)


def lxml_write_cell(xf, worksheet, cell, styled=False):
    coordinate = cell.coordinate
    attributes = {'r': coordinate}
    if styled:
        attributes['s'] = '%d' % cell.style_id

    value = cell._value
    
    if cell.data_type != 'f':
        attributes['t'] = cell.data_type
    else:
        if isinstance(value, tuple): # CK: fix up data types for formulas -- WARNING, HACKY
            tmpval,data_type = cell._infer_value(value[1], return_output=True)
            attributes['t'] = data_type
            if attributes['t'] == 'f':
                attributes['t'] = 'inlineStr'

    if cell.data_type == "d":
        if cell.parent.parent.iso_dates:
            if isinstance(value, timedelta):
                value = days_to_time(value)
            value = value.isoformat()
        else:
            attributes['t'] = "n"
            value = to_excel(value, worksheet.parent.epoch)

    if cell._comment is not None:
        comment = CommentRecord.from_cell(cell)
        worksheet._comments.append(comment)

    if value == '' or value is None:
        with xf.element("c", attributes):
            return

    with xf.element('c', attributes):
        if cell.data_type == 'f':
            shared_formula = worksheet.formula_attributes.get(coordinate, {})
            
            if value is not None: # CK: Allow writing formulas and values
                if isinstance(value, tuple):
                    formulatext = value[0][1:]
                    value,tmp_datatype  = cell._infer_value(value[1], return_output=True) # WARNING, HACKY
                else:
                    formulatext = value[1:]
                    value = None
            with xf.element('f', shared_formula):
                xf.write(formulatext)

        if cell.data_type == 's':
            value = worksheet.parent.shared_strings.add(value)
        with xf.element("v"):
            if value is not None:
                xf.write(safe_string(value))

        if cell.hyperlink:
            worksheet._hyperlinks.append(cell.hyperlink)


if LXML:
    write_cell = lxml_write_cell
else:
    write_cell = etree_write_cell
