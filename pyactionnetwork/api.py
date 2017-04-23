#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class ActionNetworkApi:
    """Python wrapper for Action Network API."""

    def __init__(self, api_key, **kwargs):
        """Instantiate the API client and get config."""
        self.headers = {"OSDI-API-Token": api_key}
        self.refresh_config()
        self.base_url = self.config.get('links', {}).get('self', 'https://actionnetwork.org/api/v2/')
        print(self.config['motd'])

    def refresh_config(self):
        """Get a new version of the base_url config."""
        self.config = requests.get(url="https://actionnetwork.org/api/v2/",
                                   headers=self.headers).json()

    def resource_to_url(self, resource):
        """Convert a named endpoint into a URL.

        Args:
            resource (str):
                resource name (e.g. 'links', 'people', etc.)
        Returns:
            (str) Full resource endpoint URL.
        """
        if resource in self.config.get('_links', {}).keys():
            return self.config['_links'][resource]['href']
        try:
            return self.config['_links']["osdi:{0}".format(resource)]['href']
        except KeyError:
            raise KeyError("Unknown Resource %s", resource)

    def get_resource(self, resource):
        """Get a resource endpoint by name.

        Args:
            resource (str):
                Resource endpoint of the format 'people', 'events', 'lists', etc.
        Returns:
            (dict) API response from endpoint or `None` if not found/valid.
        """
        url = self.resource_to_url(resource)
        return requests.get(url, headers=self.headers).json()

    def get_person(self, person_id=None, search_by='email', search_string=None):
        """Search for a user.

        Args:
            search_by (str):
                Field by which to search for a user. 'email' is the default.
            search_string (str):
                String to search for within the field given by `search_by`

        Returns:
            (dict) person json if found, otherwise `None`
        """
        if person_id:
            url = "{0}people/{1}".format(self.base_url, person_id)
        else:
            url = "{0}people/?filter={1} eq '{2}'".format(self.base_url, search_by, search_string)

        resp = requests.get(url, headers=self.headers)
        return resp.json()

    def create_person(self, person):
        """Create a user.

        Args:
            person (dict):
                Dict-like object that has keys for 'given_name', 'family_name',
                'address_lines', 'locality', 'region', 'country', 'postal_code', and
                'email'.
        Returns:
            (dict) A fully fleshed out dictionary representing a person, containing the above
            attributes and additional attributes set by Action Network.
        """
        url = "{0}people/".format(self.base_url)
        payload = {
            'person': {
                'family_name': person['family_name'],
                'given_name': person['given_name'],
                'postal_addresses': [{
                    'address_lines': person['address_lines'],
                    'locality': person['locality'],
                    'region': person['region'],
                    'country': person['country'],
                    'postal_code': person['postal_code']
                }],
                'email_addresses': [{
                    'address': person['email']
                }]
            }
        }

        print(payload)

        resp = requests.post(url, json=payload, headers=self.headers)
        return resp.json()

    def update_person(self, person_id, person):
        """Update a user.

        Args:
            person (dict):
                Dict-like object that has keys for 'given_name', 'family_name',
                'address_lines', 'locality', 'region', 'country', 'postal_code', and
                'email'.
        Returns:
            (dict) A fully fleshed out dictionary representing a person, containing the above
            attributes and additional attributes set by Action Network.
        """
        url = "{0}people/{1}".format(self.base_url, person_id)
        payload = {
            'family_name': person['family_name'],
            'given_name': person['given_name'],
            'postal_addresses': [{
                'address_lines': person['address_lines'],
                'locality': person['locality'],
                'region': person['region'],
                'country': person['country'],
                'postal_code': person['postal_code']
            }],
            'email_addresses': [{
                'address': person['email']
            }]
        }

        resp = requests.put(url, json=payload, headers=self.headers)
        return resp.json()

    def search(self, resource, operator, term):
        """Search for a given `term` within a `resource`.

        Args:
            resource (str):
                Resource family within which to search. Should be one of
                'people', 'events', etc.
            operator (str):
                Operator by which to search. Should be something like
                'eq', 'gt', 'lt', etc.
            term (str):
                Term for which to search. Can be an email, name, etc.

        Returns:
            (dict) Object if found, otherwise `None`.
        """
        pass
