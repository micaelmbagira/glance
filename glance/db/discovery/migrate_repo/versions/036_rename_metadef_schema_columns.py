# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from discovery.schema import MetaData
from discovery.schema import Table


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    metadef_objects = Table('metadef_objects', meta, autoload=True)
    metadef_objects.c.schema.alter(name='json_schema')

    metadef_properties = Table('metadef_properties', meta, autoload=True)
    metadef_properties.c.schema.alter(name='json_schema')


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    metadef_objects = Table('metadef_objects', meta, autoload=True)
    metadef_objects.c.json_schema.alter(name='schema')

    metadef_properties = Table('metadef_properties', meta, autoload=True)
    metadef_properties.c.json_schema.alter(name='schema')
