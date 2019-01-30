from __future__ import absolute_import
# Copyright (c) 2010-2019 openpyexcel


def namespaced(obj, tagname, namespace=None):
    """
    Utility to create a namespaced tag for an object
    """

    namespace = getattr(obj, "namespace", namespace)
    if namespace is not None:
        tagname = "{%s}%s" % (namespace, tagname)
    return tagname
