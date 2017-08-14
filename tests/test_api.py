#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import re
import responses
import json

import pyactionnetwork
from responses import GET, POST, PUT


DEFAULT_URL = re.compile(r'https://actionnetwork\.org/.*')


@responses.activate
def get_api():
    with open('test_data/self.json', 'r') as f:
        responses.add(GET, DEFAULT_URL, f.read())
    return pyactionnetwork.ActionNetworkApi(api_key="test")


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

    with responses.RequestsMock() as resps:
        with open('test_data/people.json', 'r') as f:
            resps.add(GET, DEFAULT_URL, f.read())
        resp = api.get_resource('people')['_embedded']
        assert len(resp['osdi:people']) == 1
        assert resp['osdi:people'][0]['given_name'] == 'Test'
        assert resp['osdi:people'][0]['family_name'] == 'User'


def test_create_person():
    api = get_api()

    person = {
        'family_name': 'Doe',
        'given_name': 'John',
        'address': ['800 Nowhere St.', 'Apt. 1'],
        'city': 'Philadelphia',
        'state': 'PA',
        'country': 'US',
        'postal_code': 19125,
        'email': 'john.doe@example.com'
    }

    def callback(request):
        payload = json.loads(request.body)
        headers = {'content_type': 'application/json'}

        assert payload['person']['family_name'] == person['family_name']
        assert payload['person']['given_name'] == person['given_name']

        assert 'postal_addresses' in payload['person']
        assert 'email_addresses' in payload['person']
        address = payload['person']['postal_addresses'][0]
        email = payload['person']['email_addresses'][0]

        assert address['address_lines'] == person['address']
        assert address['locality'] == person['city']
        assert address['region'] == person['state']
        assert address['country'] == person['country']
        assert address['postal_code'] == person['postal_code']

        assert email['address'] == person['email']

        return (200, headers, json.dumps(payload))

    with responses.RequestsMock() as resps:
        resps.add_callback(
            POST,
            'https://actionnetwork.org/api/v2/people/',
            callback=callback)
        api.create_person(**person)


def test_update_person():
    api = get_api()

    person = {
        'family_name': 'Doe',
        'given_name': 'John',
        'address': ['800 Nowhere St.', 'Apt. 1'],
        'city': 'Philadelphia',
        'state': 'PA',
        'country': 'US',
        'postal_code': 19147,
        'email': 'john.doe@example.com'
    }

    def callback(request):
        payload = json.loads(request.body)
        headers = {'content_type': 'application/json'}

        assert payload['family_name'] == person['family_name']
        assert payload['given_name'] == person['given_name']

        assert 'postal_addresses' in payload
        assert 'email_addresses' in payload
        address = payload['postal_addresses'][0]
        email = payload['email_addresses'][0]

        assert address['address_lines'] == person['address']
        assert address['locality'] == person['city']
        assert address['region'] == person['state']
        assert address['country'] == person['country']
        assert address['postal_code'] == person['postal_code']

        assert email['address'] == person['email']

        return (200, headers, json.dumps(payload))

    with responses.RequestsMock() as resps:
        resps.add_callback(
            PUT,
            'https://actionnetwork.org/api/v2/people/0',
            callback=callback)
        api.update_person(person_id=0, **person)


def test_get_person():
    api = get_api()

    @responses.activate
    def test():
        with open('test_data/get_person.json', 'r') as f:
            responses.add(GET, DEFAULT_URL, f.read())
        resp = api.get_person(search_string='jane@example.com')
        assert len(resp['_embedded']['osdi:people']) == 1
        assert resp['_embedded']['osdi:people'][0]['given_name'] == 'jane'
        assert resp['_embedded']['osdi:people'][0]['family_name'] == 'doe'
        assert responses.calls[0].request.url == "https://actionnetwork.org/api/v2/people/?filter=email%20eq%20'jane%40example.com'"  # noqa
    test()
