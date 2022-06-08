from urllib.parse import ParseResult, urlparse
import requests
import json
import os


def get_short_link(headers: json, long_url: str) -> dict:
    """Convert long link to short link"""

    url: str = 'https://api-ssl.bitly.com/v4/shorten'
    payload: json = {
        "long_url": long_url,
    }
    response: requests.Response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()['link']


def total_clicks(headers: json, bitlink: str) -> dict:
    """Counts number of Bitlink clicks"""

    bitlink: str = cut_protochol_from_url(url=bitlink)

    url: str = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response: requests.Response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def is_bitlink(headers: json, bitlink: str,) -> bool:
    """Check for Bitlink"""

    bitlink: str = cut_protochol_from_url(url=bitlink)

    url: str = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response: requests.Response = requests.get(url, headers=headers)

    return response.ok


def cut_protochol_from_url(url: str) -> str:
    """Cut protochol from URL"""
    parsed_url: ParseResult = urlparse(url)
    link: str = ''.join([parsed_url.hostname, parsed_url.path])

    return link


if __name__=='__main__':

    headers: json = {
        "Authorization": f"Bearer {os.environ.get('API_TOKEN')}"
    }

    link: str = str(input('Введите ссылку или Битлинк: '))

    try:
        is_bitlink: bool = is_bitlink(bitlink=link, headers=headers)
        print('is_bitlink', is_bitlink)
        response = (
            total_clicks(headers=headers, bitlink=link) 
            if is_bitlink 
            else get_short_link(headers=headers, long_url=link)
        )
    except:
        print('Не корректный запрос')
    else:
        print(response)



