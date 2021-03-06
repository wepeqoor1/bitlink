from urllib.parse import ParseResult, urlparse
from dotenv import load_dotenv
import requests

import argparse
import json
import os


def get_short_link(headers: json, long_url: str) -> str:
    """Convert long link to short link"""

    url: str = 'https://api-ssl.bitly.com/v4/shorten'
    payload: json = {
        "long_url": long_url,
    }
    response: requests.Response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()['link']


def total_clicks(headers: json, bitlink: str) -> str:
    """Counts number of Bitlink clicks"""

    bitlink: str = cut_protocol_from_url(url=bitlink)

    url: str = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response: requests.Response = requests.get(url, headers=headers)
    response.raise_for_status()

    return f"Количество переходов по ссылке битли: {response.json()['total_clicks']}"


def is_bitlink(headers: json, bitlink: str) -> bool:
    """Check for Bitlink"""

    bitlink: str = cut_protocol_from_url(url=bitlink)

    url: str = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response: requests.Response = requests.get(url, headers=headers)

    return response.ok


def cut_protocol_from_url(url: str) -> str:
    """Cut protocol from URL"""

    parsed_url: ParseResult = urlparse(url)
    
    return ''.join([parsed_url.hostname, parsed_url.path])


if __name__=='__main__':

    parser = argparse.ArgumentParser(
        description=(
            """
            Программа принимает на вход ссылки и генерирует коротки (Битлинк) ссылки.
            Так же считает количество переходов по коротким ссылкам.
            """)
        )
    parser.add_argument('link', help='Введите ссылку или битлинк')
    args = parser.parse_args()
    link: str = args.link

    """Load environment variables"""
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    headers: json = {
        "Authorization": f"Bearer {os.environ.get('BITLINK_API_TOKEN')}"
    }

    try:
        is_bitlink: bool = is_bitlink(bitlink=link, headers=headers)
        response = (
            total_clicks(headers=headers, bitlink=link) 
            if is_bitlink 
            else get_short_link(headers=headers, long_url=link)
        )
    except requests.exceptions.HTTPError:
        print('Не корректный запрос')
    except TypeError:
        print('Введите ссылку или Битлик')
    else:
        print(response)
