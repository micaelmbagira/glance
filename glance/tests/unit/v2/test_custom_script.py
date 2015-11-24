__author__ = 'stack'

__author__ = 'stack'

import datetime
import uuid

from oslo_config import cfg
from oslo_serialization import jsonutils
from oslo_utils import timeutils
import routes
import six
import webob

import glance.api.common
import glance.common.config
import glance.context
from glance.db.discovery import api as db_api
from glance.db.sqlalchemy import models as db_models
from glance.registry.api import v2 as rserver
from glance.tests.unit import base
from glance.tests import utils as test_utils

CONF = cfg.CONF

_gen_uuid = lambda: str(uuid.uuid4())

UUID1 = _gen_uuid()
UUID2 = _gen_uuid()


class TestCustomScript(base.IsolatedUnitTest):
    def setUp(self):
        super(TestCustomScript, self).setUp()
        self.mapper = routes.Mapper()
        self.api = test_utils.FakeAuthMiddleware(rserver.API(self.mapper),
                                                 is_admin=True)

        uuid1_time = timeutils.utcnow()
        uuid2_time = uuid1_time + datetime.timedelta(seconds=5)

        self.FIXTURES = [
            {'id': UUID1,
             'name': 'fake image #1',
             'status': 'active',
             'disk_format': 'ami',
             'container_format': 'ami',
             'is_public': False,
             'created_at': uuid1_time,
             'updated_at': uuid1_time,
             'deleted_at': None,
             'deleted': False,
             'checksum': None,
             'min_disk': 0,
             'min_ram': 0,
             'size': 13,
             'locations': [{'url': "file:///%s/%s" % (self.test_dir, UUID1),
                            'metadata': {}, 'status': 'active'}],
             'properties': {'type': 'kernel'}},
            {'id': UUID2,
             'name': 'fake image #2',
             'status': 'active',
             'disk_format': 'vhd',
             'container_format': 'ovf',
             'is_public': True,
             'created_at': uuid2_time,
             'updated_at': uuid2_time,
             'deleted_at': None,
             'deleted': False,
             'checksum': None,
             'min_disk': 5,
             'min_ram': 256,
             'size': 19,
             'locations': [{'url': "file:///%s/%s" % (self.test_dir, UUID2),
                            'metadata': {}, 'status': 'active'}],
             'properties': {}}]

        self.context = glance.context.RequestContext(is_admin=True)
        #db_api.get_engine()
        #self.destroy_fixtures()
        #self.create_fixtures()

    def test_create_images(self):
        for fixture in self.FIXTURES:
            db_api.image_create(self.context, fixture)
            # We write a fake image file to the filesystem
            with open("%s/%s" % (self.test_dir, fixture['id']), 'wb') as image:
                image.write("chunk00000remainder")
                image.flush()