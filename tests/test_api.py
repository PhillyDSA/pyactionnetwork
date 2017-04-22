#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import pytest
import responses
from responses import GET

import api

DEFAULT_URL = re.compile(r'https://actionnetwork.org/.*')


@responses.activate
def get_api():
    with open('test_data/self.json', 'r') as f:
        responses.add(GET, DEFAULT_URL, f.read())
    return api.ActionNetworkApi(api_key="test")


def test_api_creation():
    api = get_api()
    assert 'motd' in api.config
    assert api.base_url == 'https://actionnetwork.org/api/v2/'
    assert api.headers == {'OSDI-API-Token': 'test'}


def test_resource_to_url():
    api = get_api()
    assert api.resource_to_url('people') == 'https://actionnetwork.org/api/v2/people'
    assert api.resource_to_url('events') == 'https://actionnetwork.org/api/v2/events'

    with pytest.raises(KeyError):
        api.resource_to_url('asdf')


def test_get_resource():
    api = get_api()

    @responses.activate
    def test():
        with open('test_data/people.json', 'r') as f:
            responses.add(GET, DEFAULT_URL, f.read())
        resp = api.get_resource('people')
        assert len(resp['odsi:people']) == 1
        assert resp['odsi:people'][0]['given_name'] == 'Test'
        assert resp['odsi:people'][0]['given_name'] == 'User'
