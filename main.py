import requests as req
import time

API_KEY = 'RGAPI-1248e2cc-18c4-4b2d-ae38-6a7793eb77e8'
SERVERLIST = ['NA', 'JP', 'PBE', 'EUW', 'RU', 'KR', 'BR', 'OC', 'EUNE']


def handle_response_code(response_raw, request_url):
    if response_raw.status_code is 429:
        '''rate limit exceeded, slowing down'''
        time.sleep(1)
        response_raw = req.get(request_url)

    if response_raw.status_code is not 200:
        if response_raw.status_code is 401:
            print('API Key is outdated\nShutting down...')
        elif response_raw.status_code is 404:
            print('Summoner Name not found!\nShutting down...')
        else:
            print('something went wrong: Error Code ' + str(response_raw.status_code) + '\nShutting down...')
        exit(1)


def wizard() -> (str, str):
    print('Welcome to LoL Stats\n')

    summoner_name = input("enter your Summoner Name ")

    server = input("enter your Server ")

    return summoner_name, server


def setup_url(server):
    server = server.upper()
    if server not in set(SERVERLIST):
        print('Unsupported Server\nShutting down...')
        exit(1)

    server = server + '1'
    if server == 'EUNE1':
        server = 'EUN1'
    if server == 'KR1':
        server = 'KR'
    if server == 'RU1':
        server = 'RU'

    base_url = 'https://' + server + '.api.riotgames.com'
    key_param = '?api_key=' + API_KEY

    return base_url, key_param


def getthis(url: str) -> str:
    request_url = BASE_URL + url + KEY_PARAM
    print('GET | ' + request_url)
    response_raw = req.get(request_url)
    handle_response_code(response_raw, request_url)
    return response_raw.json()


def get_account_id(summoner_name: str) -> str:
    return getthis('/lol/summoner/v4/summoners/by-name/' + summoner_name)['accountId']


def get_summoner_id(summoner_name: str) -> str:
    return getthis('/lol/summoner/v4/summoners/by-name/' + summoner_name)['id']


def get_mastery_score(summoner_name: str) -> str:
    return str(getthis('/lol/champion-mastery/v4/scores/by-summoner/' + get_summoner_id(summoner_name)))


SERVER = 'EUW'
NAME = 'SMALLYELLOWONE'

BASE_URL, KEY_PARAM = setup_url(SERVER)

print(get_account_id(NAME))
