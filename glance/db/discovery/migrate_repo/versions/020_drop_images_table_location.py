# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
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

import discovery

from glance.db.discovery.migrate_repo import schema


def get_images_table(meta):
    return discovery.Table('images', meta, autoload=True)


def upgrade(migrate_engine):
    meta = discovery.schema.MetaData(migrate_engine)
    images_table = get_images_table(meta)
    images_table.columns['location'].drop()


def downgrade(migrate_engine):
    meta = discovery.schema.MetaData(migrate_engine)
    images_table = get_images_table(meta)
    location = discovery.Column('location', schema.Text())
    location.create(images_table)
