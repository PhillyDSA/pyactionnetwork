#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from dateutil import relativedelta
import re


class ANBaseModel:
    """Class representing a default model for AN / OSDI data structures."""

    def __init__(self, **kwargs):
        """Parse data into new instance."""
        data = kwargs.pop('data', {})
        for (key, val) in data.items():
            setattr(self, key.replace('action_network:', ''), data.get(key, None))
        self._json = data

        if len(self.identifiers) == 1:
            self.id = self.identifiers[0].replace('action_network:', '')
        else:
            self.id = [identifier.replace('action_network:', '') for identifier in self.identifiers]


class Donation(ANBaseModel):
    """Class representing a single donation in the AN API."""

    @property
    def recurring(self):
        """Return bool describing if donation is recurring or not."""
        return getattr(self, 'recurrence', None).get('recurring')

    @property
    def period(self):
        """Return the recurring period."""
        return getattr(self, 'recurrence', None).get('period')

    @property
    def next_donation(self):
        """Return the date of the next donation."""
        if not self.recurring:
            return None

        # Splitting the recurring period to be machine parseable.
        # Hopefully this is obviated by a bug report sent to AN, bc
        # their response should be ['weekly', 'monthly', quarterly', 'yearly']
        # however, as of 12 Aug 2017, nothing heard back from them.
        data = re.split(r'\s', self.period)
        period = data[2].lower()
        num_periods = int(data[1])

        # We'll use this to pass kwargs to relativedelta
        rd_kwargs = {period: num_periods}

        created = datetime.datetime.strptime(self.created_date, "%Y-%m-%dT%H:%M:%SZ")
        now = datetime.datetime.now()

        def get_next(start, end, rd_kwargs):
            if start + relativedelta.relativedelta(**rd_kwargs) > now:
                return start + relativedelta.relativedelta(**rd_kwargs)
            else:
                return get_next(start + relativedelta.relativedelta(**rd_kwargs), now, rd_kwargs)

        return get_next(created, now, rd_kwargs)

    def __repr__(self):
        return 'Donation(id={0}, recurring={1}, period={2}, created={3}, amount={4})'.format(
            self.id,
            self.recurring,
            self.period,
            self.created_date,
            self.amount)


class Tag(ANBaseModel):
    """Class representing a single tag in the AN API."""

    def __repr__(self):
        return 'Tag(id={0}, name={1})'.format(self.id, self.name)


class Tagging(ANBaseModel):
    """Class representing a tagging in AN.

    Generally consists of OSDI:Person embeddings.
    """

    def __repr__(self):
        return 'Tagging(id={0}, name={1})'.format(self.id, self.name)


class Person(ANBaseModel):
    """Class representing a specific person instance in AN."""

    def __repr__(self):
        return 'Person(id={0}, name={1})'.format(self.id, self.name)
