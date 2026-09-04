from __future__ import annotations

import requests

from titanfile.resources.auth import AuthResource
from titanfile.resources.files import FilesResource
from titanfile.resources.messages import MessagesResource
from titanfile.resources.channels import ChannelsResource

ACCEPT = 'application/json; version=1.0'
USER_AGENT = 'TitanFile-SDK-Python/1.0.0'


class TitanFileClient:
    """
    TitanFile API client.

    Usage:
        tf = TitanFileClient(api_id='...', api_key='...', subdomain='yourcompany')
        channel_id = tf.channels.create('My Channel')
        file_id = tf.files.upload('/path/to/file.pdf', 'file.pdf')
        tf.messages.send(channel_id=channel_id, file_id=file_id)
    """

    def __init__(self, api_id: str, api_key: str, subdomain: str):
        self.base_url = f'https://{subdomain}.titanfile.com/api/v1'
        self._session = requests.Session()
        self._session.headers.update({'Accept': ACCEPT, 'User-Agent': USER_AGENT})

        token = AuthResource(self).get_token(api_id, api_key)
        self._session.headers['Authorization'] = f'Bearer {token}'

        self.files = FilesResource(self)
        self.messages = MessagesResource(self)
        self.channels = ChannelsResource(self)

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        resp = self._session.request(method, self.base_url + path, timeout=600, **kwargs)
        if not resp.ok:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            raise requests.exceptions.HTTPError(
                f'{resp.status_code} {resp.reason} — {detail}',
                response=resp,
            )
        return resp
