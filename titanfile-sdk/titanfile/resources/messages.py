from __future__ import annotations

from typing import List, Optional, Union


class MessagesResource:
    def __init__(self, client):
        self._client = client

    def send(
        self,
        channel_id: str,
        owner_email: Optional[str] = None,
        message: Optional[str] = None,
        file_id: Optional[str] = None,
        file_ids: Optional[List[str]] = None,
        folder_path: Optional[str] = None,
        notify_contacts: bool = True,
    ) -> dict:
        """
        Send a message to a channel, optionally with files.

        Args:
            channel_id:     Channel UUID.
            owner_email:    Email of the channel owner (required when using a service account).
            message:        HTML message body.
            file_id:        Single file UUID (from files.upload()).
            file_ids:       Multiple file UUIDs.
            folder_path:    Panel folder path (e.g. '/reports/').
            notify_contacts: Whether to notify channel members (default True).
        """
        data = {
            'channel': channel_id,
            'notify_contacts': 'true' if notify_contacts else 'false',
        }
        if owner_email:
            data['owner_email'] = owner_email
        if message:
            data['message_html'] = message
        if folder_path:
            data['folder_path'] = folder_path

        # Build multipart fields as list of (name, (None, value)) tuples so
        # repeated keys (uploaded_files) are sent correctly.
        parts = [(k, (None, str(v))) for k, v in data.items()]
        for fid in (file_ids or ([file_id] if file_id else [])):
            parts.append(('uploaded_files', (None, fid)))

        resp = self._client.request('POST', '/messages/', files=parts)
        return resp.json()
