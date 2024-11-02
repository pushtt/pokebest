import csv
from types import new_class
from typing import Any, Dict, List, Optional, Sequence, Type, Union
from enum import StrEnum
from polars import when
import requests
from urllib.parse import urljoin
import os
from logger import logger

IntOrStr = Union[int, str, None]


class GameEndpoint(StrEnum):
    GENERATION = "generation"
    POKEDEX = "pokedex"
    VERSION = "version"
    VERSION_GROUP = "version-group"

class PokemonEndPoint(StrEnum):
    ABILITY = "ability"
    CHARACTERISTIC = "characteristic"
    TYPE = "type"
    STAT = "stat"
    EGG_GROUP = "egg-group"
    POKEMON = "pokemon"
    POKEMON_COLOUR = "pokemon-color"
    POKEMON_FORM = "pokemon-form"
    POKEMON_HABITAT = "pokemon-habitat"
    POKEMON_SPECIES = "pokemon-species"
    POKEMON_SHAPE = "pokemon-shape"
    ENCOUNTER = "encounters"

class PokeAPIError(Exception):
    """Custom exception for API errors"""
    pass


class PokeAPI:
    def __init__(self,
                 version:int = 2,
                 api_key:str = ""
                 ,
                 ) -> None:
        self.url = "https://pokeapi.co/api/v{}/".format(str(version))
        self._api_key = api_key or os.getenv("API")

        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
            })

    def _request(self, method:str, endpoint:Optional[str], params=None) -> dict:
        url = urljoin(self.url, endpoint)
        try:
            response = self.session.request(method, url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise PokeAPIError(f"API request failed: {str(e)}")

    def _fetch_data(self, endpoint, limit=20):
        all_data = []
        offset = 0
        logger.info(f"Fetching data from {endpoint}")
        while True:
            params = {"offset": offset, "limit": limit}
            response = self._request("GET", endpoint=endpoint,  params=params)
            logger.info(f"Fetched data offset {offset}")
            all_data.extend(response["results"])
            if not response["next"]:
                break
            else:
                offset += limit
        return all_data


    # GAMES
    def get_games(self, endpoint:GameEndpoint) -> List:
        return self._fetch_data(endpoint)

    def get_game(self, endpoint:GameEndpoint, id_or_name:IntOrStr = None) -> dict:
        return self._request("GET", f"{endpoint}/{id_or_name}")

    # POKEMON
    def get_pokemons(self, endpoint:PokemonEndPoint) -> List:
        return self._fetch_data(endpoint)

    def get_pokemon(self, endpoint:PokemonEndPoint, id_or_name:IntOrStr = None) -> dict:
        if endpoint != PokemonEndPoint.ENCOUNTER:
            return self._request("GET", f"{endpoint}/{id_or_name}")
        return self._request("GET", f"pokemon/{id_or_name}/{endpoint}")

    @staticmethod
    def to_csv(data:dict, filename):
        with open(filename, mode="w", newline="") as csvfile:
            fieldnames = data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data)


