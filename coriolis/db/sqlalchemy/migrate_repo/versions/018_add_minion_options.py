# Copyright 2020 Cloudbase Solutions Srl
# All Rights Reserved.

import sqlalchemy


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    base_transfer_action = sqlalchemy.Table(
        'base_transfer_action', meta, autoload=True)

    # add 'source_minion_options' to 'base_transfer_action' table
    source_minion_options = sqlalchemy.Column(
        'source_minion_options', sqlalchemy.Text, nullable=True)
    base_transfer_action.create_column(source_minion_options)

    # add 'destination_minion_options' to 'base_transfer_action' table
    destination_minion_options = sqlalchemy.Column(
        'destination_minion_options', sqlalchemy.Text, nullable=True)
    base_transfer_action.create_column(destination_minion_options)
