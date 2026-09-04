from __future__ import annotations

import json
from typing import Dict, List, Optional


class ChannelsResource:
    def __init__(self, client):
        self._client = client

    def create(self, name: str, custom_fields: Optional[Dict[str, str]] = None) -> str:
        """Create a channel. Returns the channel UUID."""
        parts = [('name', (None, name))]
        if custom_fields:
            parts.append(('custom_fields', (None, json.dumps(custom_fields))))
        resp = self._client.request('POST', '/channels/', files=parts)
        return resp.json()['id']

    def list(self, owner_email: Optional[str] = None) -> list:
        """List channels. Optionally filter by owner email."""
        params = {}
        if owner_email:
            params['owner_email'] = owner_email
        resp = self._client.request('GET', '/channels/', params=params)
        return resp.json().get('data', [])

    def search(self, query: str, owner_email: Optional[str] = None) -> list:
        """Search channels by name."""
        params = {'query': query}
        if owner_email:
            params['owner_email'] = owner_email
        resp = self._client.request('GET', '/subscription/channels/search/', params=params)
        return resp.json().get('data', [])

    def add_contact(self, channel_id: str, email: str, role: str = 'manager') -> dict:
        """Add a contact to a channel."""
        resp = self._client.request(
            'POST',
            '/channel_contacts/',
            files=[
                ('channel', (None, channel_id)),
                ('email', (None, email)),
                ('add_to_panel', (None, 'true')),
                ('sharing_permissions', (None, role)),
            ],
        )
        return resp.json()
