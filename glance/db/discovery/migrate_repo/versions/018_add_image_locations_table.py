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


def upgrade(migrate_engine):
    meta = discovery.schema.MetaData(migrate_engine)

    # NOTE(bcwaldon): load the images table for the ForeignKey below
    discovery.Table('images', meta, autoload=True)

    image_locations_table = discovery.Table(
        'image_locations', meta,
        discovery.Column('id',
                          schema.Integer(),
                          primary_key=True,
                          nullable=False),
        discovery.Column('image_id',
                          schema.String(36),
                          discovery.ForeignKey('images.id'),
                          nullable=False,
                          index=True),
        discovery.Column('value',
                          schema.Text(),
                          nullable=False),
        discovery.Column('created_at',
                          schema.DateTime(),
                          nullable=False),
        discovery.Column('updated_at',
                          schema.DateTime()),
        discovery.Column('deleted_at',
                          schema.DateTime()),
        discovery.Column('deleted',
                          schema.Boolean(),
                          nullable=False,
                          default=False,
                          index=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8',
    )

    schema.create_tables([image_locations_table])


def downgrade(migrate_engine):
    meta = discovery.schema.MetaData(migrate_engine)
    image_locations_table = discovery.Table('image_locations', meta,
                                             autoload=True)
    schema.drop_tables([image_locations_table])
