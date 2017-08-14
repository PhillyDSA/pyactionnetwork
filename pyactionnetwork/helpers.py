#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

from .models import Donation


def get_all_donations(api=None, donations=None, url="https://actionnetwork.org/api/v2/donations"):
    """Get a list of all donations for an organization.

    Args:
        api (pyactionnetwork.ActionNetworkApi):
            Authorized ActionNetwork API instance.
        donations (list):
            List of Donation instances.
        url (str):
            URL of the donations endpoint to use. Defaults to all
            donations made to a group.

    Returns:
        (list) List of Donations processed by AN.
    """
    if not donations:
        donations = []

    data = requests.get(url=url, headers=api.headers)
    donations += [Donation(data=d) for d in data.json()['_embedded']['osdi:donations']]

    if data.json().get('_links', {}).get('next', None):
        next_url = data.json().get('_links').get('next').get('href')
        return get_all_donations(api=api, donations=donations, url=next_url)
    return donations
