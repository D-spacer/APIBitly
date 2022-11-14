import requests
import sys
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, link_to_shorten):
    header = {
        'Authorization': f'Bearer {token}'
    }
    parameters = {
        "long_url": link_to_shorten
    }
    response = requests.post('https://api-ssl.bitly.com/v4/shorten',
                             headers=header, json=parameters)
    response.raise_for_status()
    decoded_response = response.json()
    return decoded_response['link']


def count_clicks(token, bitlink):
    url_components = urlparse(bitlink)
    bitlink = f'{url_components.netloc}{url_components.path}'
    header = {
        'Authorization': f'Bearer {token}'
    }
    parameters = {
        'unit': 'month',
        'units': -1
    }
    response = requests.get(
      f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
      headers=header, params=parameters)
    response.raise_for_status()
    decoded_response = response.json()
    return decoded_response["total_clicks"]


def is_bitlink(token, bitlink):
    url_components = urlparse(bitlink)
    bitlink = f'{url_components.netloc}{url_components.path}'
    header = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(
      f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}', headers=header
    )
    return response.ok

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Videos to images')
    parser.add_argument('url', type=str, help='Input dir for videos')
    args = parser.parse_args()
    bitly_token = os.environ['BITLY_TOKEN']
    try:
        link = args.url
        if is_bitlink(bitly_token, link):
            print(f'Количество переходов по ссылке: {count_clicks(bitly_token, link)}')
        else:
            print(f'Сокращенная ссылка: {shorten_link(bitly_token, link)}')
    except requests.exceptions.HTTPError:
        sys.exit('Неверная ссылка')


if __name__ == "__main__":
    main()
