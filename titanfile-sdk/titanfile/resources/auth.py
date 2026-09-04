from __future__ import annotations

import requests

from titanfile.exceptions import TitanFileAuthError


class AuthResource:
    def __init__(self, client):
        self._client = client

    def get_token(self, api_id: str, api_key: str) -> str:
        resp = requests.post(
            self._client.base_url + '/token/',
            headers={'Accept': 'application/json; version=1.0'},
            json={'username': api_id, 'password': api_key},
            timeout=30,
        )
        if not resp.ok:
            raise TitanFileAuthError(f'Authentication failed: {resp.text}')
        token = resp.json().get('access')
        if not token:
            raise TitanFileAuthError('No access token in response.')
        return token
