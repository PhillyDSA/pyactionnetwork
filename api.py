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
            resource (string):
                resource name (e.g. 'links', 'people', etc.)
        Returns:
            (string) Full resource endpoint URL.

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
            resource (string):
                Resource endpoint of the format 'people', 'events', 'lists', etc.
        Returns:
            (dict) API response from endpoint or `None` if not found/valid.
        """
        url = self.resource_to_url(resource)
        return requests.get(url, headers=self.headers).json()

    def get_person(self, search_by='email', search_string=None):
        """Search for a user.

        Args:
            search_by (string):
                Field by which to search for a user. 'email' is the default.
            search_string (string):
                String to search for within the field given by `search_by`

        Returns:
            person json if found, otherwise `None`
        """
        url = "{base_url}people/?filter={search_by} eq '{search_string}'".format(
            base_url=self.base_url,
            search_by=search_by,
            search_string=search_string)

        resp = requests.get(url, headers=self.headers)
        return resp.json()
