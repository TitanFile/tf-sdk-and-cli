from unittest.mock import patch, MagicMock
from titanfile import TitanFileClient


def make_client():
    with patch('titanfile.resources.auth.requests.post') as mock_post:
        mock_post.return_value = MagicMock(ok=True, json=lambda: {'access': 'test-token'})
        return TitanFileClient(api_id='test-id', api_key='test-key', subdomain='test')


def test_auth_sets_bearer_token():
    client = make_client()
    assert client._session.headers['Authorization'] == 'Bearer test-token'


def test_channels_create():
    client = make_client()
    with patch.object(client, 'request') as mock_req:
        mock_req.return_value = MagicMock(json=lambda: {'id': 'chan-uuid'})
        result = client.channels.create('Test Channel')
    assert result == 'chan-uuid'
    mock_req.assert_called_once_with('POST', '/channels/', json={'name': 'Test Channel'})


def test_files_upload_direct(tmp_path):
    client = make_client()
    f = tmp_path / 'small.txt'
    f.write_bytes(b'hello')
    with patch.object(client, 'request') as mock_req:
        mock_req.return_value = MagicMock(json=lambda: {'id': 'file-uuid'})
        result = client.files.upload(str(f))
    assert result == 'file-uuid'


def test_messages_send():
    client = make_client()
    with patch.object(client, 'request') as mock_req:
        mock_req.return_value = MagicMock(json=lambda: {'id': 'msg-uuid'})
        client.messages.send(channel_id='chan-uuid', owner_email='user@example.com', file_id='file-uuid')
    call_data = mock_req.call_args[1]['data']
    assert call_data['channel'] == 'chan-uuid'
    assert call_data['owner_email'] == 'user@example.com'
