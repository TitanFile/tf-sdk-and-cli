from __future__ import annotations

import os
from pathlib import Path
from typing import Union

CHUNK_SIZE = 1024 * 1024 * 200       # 200 MB per chunk
LARGE_FILE_THRESHOLD = 1024 * 1024 * 500  # 500 MB


class FilesResource:
    def __init__(self, client):
        self._client = client

    def upload(self, file_path: Union[str, Path], file_name: str = None) -> str:
        """
        Upload a file to TitanFile. Returns the file UUID.
        Automatically uses chunked upload for files larger than 500 MB.
        """
        file_path = Path(file_path)
        file_name = file_name or file_path.name
        size = os.path.getsize(file_path)

        if size >= LARGE_FILE_THRESHOLD:
            return self._chunked_upload(file_path, file_name, size)
        return self._direct_upload(file_path, file_name)

    def _direct_upload(self, file_path: Path, file_name: str) -> str:
        with open(file_path, 'rb') as f:
            resp = self._client.request(
                'POST',
                '/files/upload/',
                files=[('file', (file_name, f, 'application/octet-stream'))],
            )
        return resp.json()['id']

    def _chunked_upload(self, file_path: Path, file_name: str, size: int = None) -> str:
        # Start session
        resp = self._client.request('POST', '/files/upload_session/start/')
        session_id = resp.json()['session_id']

        # Upload parts
        size = size or os.path.getsize(file_path)
        total_parts = -(-size // CHUNK_SIZE)  # ceiling division
        with open(file_path, 'rb') as f:
            part_num = 1
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                self._client.request(
                    'POST',
                    '/files/upload_session/add_part/',
                    data={'session_id': session_id, 'part_number': part_num},
                    files=[('chunk', chunk)],
                )
                print(f'Uploaded part {part_num}/{total_parts} ({len(chunk) / 1024 / 1024:.1f} MB)', flush=True)
                part_num += 1

        # Complete session
        resp = self._client.request(
            'POST',
            '/files/upload_session/complete/',
            data={'session_id': session_id, 'file_name': file_name},
        )
        return resp.json()['id']
