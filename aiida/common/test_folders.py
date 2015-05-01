# -*- coding: utf-8 -*-
import unittest

__copyright__ = u"Copyright (c), 2015, ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE (Theory and Simulation of Materials (THEOS) and National Centre for Computational Design and Discovery of Novel Materials (NCCR MARVEL)), Switzerland and ROBERT BOSCH LLC, USA. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.4.1"
__contributors__ = "Andrea Cepellotti, Giovanni Pizzi, Andrius Merkys"


class FoldersTest(unittest.TestCase):
    """
    Tests for the Folder class.
    """

    def test_unicode(self):
        from aiida.common.folders import Folder
        import os, tempfile

        tmpsource = tempfile.mkdtemp()
        tmpdest = tempfile.mkdtemp()
        with open(os.path.join(tmpsource, "sąžininga"), 'w') as f:
            f.write("test")
        with open(os.path.join(tmpsource, "žąsis"), 'w') as f:
            f.write("test")
        fd = Folder(tmpdest)
        fd.insert_path(tmpsource, "destination")
        fd.insert_path(tmpsource, u"šaltinis")

        fd = Folder(os.path.join(tmpsource, u"šaltinis"))
        fd.insert_path(tmpsource, "destination")
        fd.insert_path(tmpdest, u"kitas-šaltinis")