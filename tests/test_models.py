#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json

from freezegun import freeze_time

from pyactionnetwork.models import Tag, Donation


@freeze_time('2017-08-14')
def test_create_donation():
    with open('test_data/donations.json') as f:
        data = json.loads(f.read())
    donations = [Donation(data=data['_embedded']['osdi:donations'][num]) for num in range(len((data['_embedded']['osdi:donations'])))]  # noqa
    assert donations[0].id == '3039205h-5c40-4e44-bc9b-ed3985713cc8', donations[0].id
    assert donations[0].next_donation == datetime.datetime(2017, 10, 29, 14, 54, 26), donations[0].next_donation  # noqa
    assert donations[0].recurring is True, donations[0].recurring


def test_create_tag():
    with open('test_data/tags.json') as f:
        data = json.loads(f.read())
    tags = [Tag(data=data['_embedded']['osdi:tags'][num]) for num in range(len((data['_embedded']['osdi:tags'])))]  # noqa
    assert tags[0].id == 'ccc91387-2a79-4ec4-91e6-8104e931bd03', tags[0].id
    assert tags[0].name == '2017_04_general_meeting', tags[0].name
