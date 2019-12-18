# -*- coding: utf-8 -*-
import requests as req
import time
import os

print('Welcome to LoL Stats\n')

API_KEY = None
while API_KEY is None:
    try:
        f = open("APIKEY.txt", "r")
        API_KEY = f.read()
        f.close()

        # check if API KEY is valid and not timed out.

        response = req.get('https://euw1.api.riotgames.com/lol/status/v3/shard-data?api_key=' + API_KEY)
        if response.status_code in {400, 404, 405, 415, 500, 502, 503, 504}:
            print('ERROR ' + str(response.status_code) + '/nShutting down.\n')
            input('Press enter to continue...')
            exit(1)

        if response.status_code == 401:
            print('API KEY is outdated\nDeleting outdated key')
            os.remove("APIKEY.txt")
            API_KEY = None

        if response.status_code == 403:
            print('API Key is invalid\nDeleting invalid key')
            os.remove("APIKEY.txt")
            API_KEY = None

    except IOError:
        print("API KEY not found")
        API_KEY = input(
            "An API KEY is required to access Riots Database.\n"
            "You can find your API KEY on\nhttps://developer.riotgames.com/\n"
            "Enter your API KEY: ")
        f = open("APIKEY.txt", "w")
        f.write(API_KEY)
        f.close()
        API_KEY = None

SERVERLIST = ['NA', 'JP', 'PBE', 'EUW', 'RU', 'KR', 'BR', 'OC', 'EUNE']


def handle_response_code(response_raw, request_url):
    time.sleep(0.5)
    resp = response_raw
    while resp.status_code == 429 or resp.status_code == 503:
        print('rate limit exceeded, slowing down')
        time.sleep(30)
        resp = req.get(request_url)

    if resp.status_code != 200:
        if resp.status_code == 401:
            print('API Key is outdated\nShutting down...')
        elif resp.status_code == 403:
            print('API Key is invalid\nShutting down...')
        elif resp.status_code == 404:
            print('Summoner Name not found!\nShutting down...')
        else:
            print('something went wrong: Error Code ' + str(resp.status_code) + '\nShutting down...')
        input("Press enter to exit...")
        exit(1)
    return resp


def wizard() -> (str, str):
    summoner_name = input("enter your Summoner Name ")
    server = input("enter your Server ")
    return summoner_name, server


def setup_url(server):
    server = server.upper()
    if server not in set(SERVERLIST):
        print('Unsupported Server\nShutting down...')
        input("Press enter to exit...")
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
    response_raw = handle_response_code(response_raw, request_url)
    return response_raw.json()


def get_account_id(summoner_name: str) -> str:
    return getthis('/lol/summoner/v4/summoners/by-name/' + summoner_name)['accountId']


def get_summoner_id(summoner_name: str) -> str:
    return getthis('/lol/summoner/v4/summoners/by-name/' + summoner_name)['id']


def get_mastery_score(summoner_name: str) -> str:
    return str(getthis('/lol/champion-mastery/v4/scores/by-summoner/' + get_summoner_id(summoner_name)))


def get_number_of_games(summoner_name: str) -> str:
    request_url = BASE_URL + '/lol/match/v4/matchlists/by-account/' + get_account_id(
        summoner_name) + KEY_PARAM + '&endIndex=99999&beginIndex=99999'
    print('GET | ' + request_url)
    response_raw = req.get(request_url)
    response_raw = handle_response_code(response_raw, request_url)
    return response_raw.json()['totalGames']


def get_match_id(index: int, summoner_name=None, account_id=None) -> str:
    if account_id is None:
        if summoner_name is None or summoner_name == NAME:
            account_id = ACCOUNT_ID
        else:
            account_id = get_account_id(summoner_name)
    request_url = BASE_URL + '/lol/match/v4/matchlists/by-account/' + account_id + KEY_PARAM + '&endIndex=' + str(
        index + 1) + '&beginIndex=' + str(index)
    print('GET | ' + request_url)
    response_raw = req.get(request_url)
    response_raw = handle_response_code(response_raw, request_url)
    return response_raw.json()['matches'][0]['gameId']


def get_players(match_id: str):
    response = getthis('/lol/match/v4/matches/' + str(match_id))['participantIdentities']
    players = [a['player']['summonerName'] for a in response]
    return players


SERVER = None
NAME = None
if SERVER is None or NAME is None:
    NAME, SERVER = wizard()
BASE_URL, KEY_PARAM = setup_url(SERVER)
ACCOUNT_ID = get_account_id(NAME)
