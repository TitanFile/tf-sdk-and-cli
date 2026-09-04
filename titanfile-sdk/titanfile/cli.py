from __future__ import annotations

import argparse
import json
import os
import sys

from titanfile import TitanFileClient


def _client_from_env_or_args(args) -> TitanFileClient:
    api_id = args.api_id or os.environ.get('TITANFILE_API_ID')
    api_key = args.api_key or os.environ.get('TITANFILE_API_KEY')
    subdomain = args.subdomain or os.environ.get('TITANFILE_SUBDOMAIN')

    if not all([api_id, api_key, subdomain]):
        print('Error: --api-id, --api-key and --subdomain are required (or set via env vars).', file=sys.stderr)
        sys.exit(1)

    return TitanFileClient(api_id=api_id, api_key=api_key, subdomain=subdomain)


def cmd_upload(args):
    client = _client_from_env_or_args(args)
    file_id = client.files.upload(args.file, args.name)
    print(json.dumps({'file_id': file_id}))


def cmd_send(args):
    client = _client_from_env_or_args(args)
    result = client.messages.send(
        channel_id=args.channel,
        owner_email=args.owner_email,
        message=args.message,
        file_id=args.file_id,
    )
    print(json.dumps(result))


def cmd_channel_create(args):
    client = _client_from_env_or_args(args)
    custom_fields = json.loads(args.custom_fields) if args.custom_fields else None
    channel_id = client.channels.create(args.name, custom_fields=custom_fields)
    print(json.dumps({'channel_id': channel_id}))


def cmd_channel_search(args):
    client = _client_from_env_or_args(args)
    results = client.channels.search(args.query, owner_email=args.owner_email)
    print(json.dumps(results))


def main():
    parser = argparse.ArgumentParser(prog='titanfile', description='TitanFile CLI')

    # Global auth args
    parser.add_argument('--api-id', default=None)
    parser.add_argument('--api-key', default=None)
    parser.add_argument('--subdomain', default=None)

    sub = parser.add_subparsers(dest='command', required=True)

    # upload
    p_upload = sub.add_parser('upload', help='Upload a file. Returns file_id JSON.')
    p_upload.add_argument('--file', required=True, help='Path to file')
    p_upload.add_argument('--name', default=None, help='File name override')
    p_upload.set_defaults(func=cmd_upload)

    # send
    p_send = sub.add_parser('send', help='Send a message to a channel.')
    p_send.add_argument('--channel', required=True, help='Channel UUID')
    p_send.add_argument('--owner-email', default=None)
    p_send.add_argument('--message', default=None)
    p_send.add_argument('--file-id', default=None, help='File UUID from upload command')
    p_send.set_defaults(func=cmd_send)

    # channel create
    p_cc = sub.add_parser('channel-create', help='Create a channel. Returns channel_id JSON.')
    p_cc.add_argument('--name', required=True)
    p_cc.add_argument('--custom-fields', default=None, help='JSON string of required custom fields, e.g. \'{"field": "value"}\'')
    p_cc.set_defaults(func=cmd_channel_create)

    # channel search
    p_cs = sub.add_parser('channel-search', help='Search channels.')
    p_cs.add_argument('--query', required=True)
    p_cs.add_argument('--owner-email', default=None)
    p_cs.set_defaults(func=cmd_channel_search)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
