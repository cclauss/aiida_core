# -*- coding: utf8 -*-
from __future__ import absolute_import
from aiida.backends.testbase import AiidaTestCase
from aiida.cmdline.params.types import ComputerParamType
from aiida.orm.utils.loaders import OrmEntityLoader


class TestComputerParamType(AiidaTestCase):

    @classmethod
    def setUpClass(cls):
        """
        Create some computers to test the ComputerParamType parameter type for the command line infrastructure
        We create an initial computer with a random name and then on purpose create two computers with a name
        that matches exactly the ID and UUID, respectively, of the first one. This allows us to test
        the rules implemented to solve ambiguities that arise when determing the identifier type
        """
        super(TestComputerParamType, cls).setUpClass()

        kwargs = {
            'hostname': 'localhost',
            'transport_type': 'local',
            'scheduler_type': 'direct',
            'workdir': '/tmp/aiida'
        }

        cls.param = ComputerParamType()
        cls.entity_01 = cls.backend.computers.create(name='computer_01', **kwargs).store()
        cls.entity_02 = cls.backend.computers.create(name=str(cls.entity_01.pk), **kwargs).store()
        cls.entity_03 = cls.backend.computers.create(name=str(cls.entity_01.uuid), **kwargs).store()

    def test_get_by_id(self):
        """
        Verify that using the ID will retrieve the correct entity
        """
        identifier = '{}'.format(self.entity_01.pk)
        result = self.param.convert(identifier, None, None)
        self.assertEquals(result.uuid, self.entity_01.uuid)

    def test_get_by_uuid(self):
        """
        Verify that using the UUID will retrieve the correct entity
        """
        identifier = '{}'.format(self.entity_01.uuid)
        result = self.param.convert(identifier, None, None)
        self.assertEquals(result.uuid, self.entity_01.uuid)

    def test_get_by_label(self):
        """
        Verify that using the LABEL will retrieve the correct entity
        """
        identifier = '{}'.format(self.entity_01.name)
        result = self.param.convert(identifier, None, None)
        self.assertEquals(result.uuid, self.entity_01.uuid)

    def test_ambiguous_label_pk(self):
        """
        Situation: LABEL of entity_02 is exactly equal to ID of entity_01

        Verify that using an ambiguous identifier gives precedence to the ID interpretation
        Appending the special ambiguity breaker character will force the identifier to be treated as a LABEL
        """
        identifier = '{}'.format(self.entity_02.name)
        result = self.param.convert(identifier, None, None)
        self.assertEquals(result.uuid, self.entity_01.uuid)

        identifier = '{}{}'.format(self.entity_02.name, OrmEntityLoader.LABEL_AMBIGUITY_BREAKER_CHARACTER)
        result = self.param.convert(identifier, None, None)
        self.assertEquals(result.uuid, self.entity_02.uuid)

    def test_ambiguous_label_uuid(self):
        """
        Situation: LABEL of entity_03 is exactly equal to UUID of entity_01

        Verify that using an ambiguous identifier gives precedence to the UUID interpretation
        Appending the special ambiguity breaker character will force the identifier to be treated as a LABEL
        """
        identifier = '{}'.format(self.entity_03.name)
        result = self.param.convert(identifier, None, None)
        self.assertEquals(result.uuid, self.entity_01.uuid)

        identifier = '{}{}'.format(self.entity_03.name, OrmEntityLoader.LABEL_AMBIGUITY_BREAKER_CHARACTER)
        result = self.param.convert(identifier, None, None)
        self.assertEquals(result.uuid, self.entity_03.uuid)
