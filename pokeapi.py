import csv
import json
import logging
import sys
from types import new_class
from typing import Any, AnyStr, Dict, List, Optional, Sequence, Type, Union
from enum import StrEnum
import requests
from urllib.parse import urljoin
import os
from logger import init_logger

IntOrStr = Union[int, str, None]

class PokemonEndPoints(StrEnum):
  Ability = "ability"
  Berry = "berry"
  BerryFirmness = "berry-firmness"
  BerryFlavor = "berry-flavor"
  Characteristic = "characteristic"
  ContestEffect = "contest-effect"
  ContestType = "contest-type"
  EggGroup = "egg-group"
  Encounter = "encounters"
  EncounterCondition = "encounter-condition"
  EncounterConditionValue = "encounter-condition-value"
  EncounterMethod = "encounter-method"
  EvolutionChain = "evolution-chain"
  EvolutionTrigger = "evolution-trigger"
  Gender = "gender"
  Generation = "generation"
  GrowthRate = "growth-rate"
  Item = "item"
  ItemAttribute = "item-attribute"
  ItemCategory = "item-category"
  ItemFlingEffect = "item-fling-effect"
  ItemPocket = "item-pocket"
  Language = "language"
  Location = "location"
  LocationArea = "location-area"
  Machine = "machine"
  Move = "move"
  MoveAilment = "move-ailment"
  MoveBattleStyle = "move-battle-style"
  MoveCategory = "move-category"
  MoveDamageClass = "move-damage-class"
  MoveLearnMethod = "move-learn-method"
  MoveTarget = "move-target"
  Nature = "nature"
  PalParkArea = "pal-park-area"
  PokeathlonStat = "pokeathlon-stat"
  Pokedex = "pokedex"
  Pokemon = "pokemon"
  PokemonColor = "pokemon-color"
  PokemonForm = "pokemon-form"
  PokemonHabitat = "pokemon-habitat"
  PokemonShape = "pokemon-shape"
  PokemonSpecies = "pokemon-species"
  Region = "region"
  Stat = "stat"
  SuperContestEffect = "super-contest-effect"
  Type = "type"
  Version = "version"
  VersionGroup = "version-group"


class PokeAPIError(Exception):
    """Custom exception for API errors"""
    pass


class PokeAPI:
    def __init__(self,
                 version:int = 2,
                 api_key:str = "",
                 logger_level= logging.ERROR

                 ) -> None:
        self.url = "https://pokeapi.co/api/v{}/".format(str(version))
        self._api_key = api_key or os.getenv("API")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
            })
        self.logger = init_logger("PokemonAPI", level=logger_level)

    def _request(self, method:str, endpoint:Optional[str|None]=None, params=None) -> dict:
        url = urljoin(self.url, endpoint)
        try:
            response = self.session.request(method, url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise PokeAPIError(f"API request failed: {str(e)}")

    def _fetch_data(self, endpoint:Optional[str|None]=None, limit=20):
        all_data = []
        offset = 0
        self.logger.info(f"Fetching data from {endpoint}")
        while True:
            params = {"offset": offset, "limit": limit}
            response = self._request("GET", endpoint=endpoint,  params=params)
            self.logger.info(f"Fetched data offset {offset}")
            if "results" in response.keys():
                all_data.extend(response["results"])
                if not response["next"]:
                    break
                else:
                    offset += limit
            else:
                return response
        return all_data


    # ENDPOINTS
    def list_endpoints(self) -> dict:
        return self._request("GET")

    # GAMES
    def get_endpoint(self, endpoint:Optional[PokemonEndPoints]=None, id_or_name:Optional[int|str] = None):
        if endpoint == PokemonEndPoints.Encounter:
            parsed_endpoint = f"pokemon/{id_or_name}/encounters"
        else:
            parsed_endpoint = "{}/{}".format(endpoint or "", id_or_name or "")
        return self._fetch_data(parsed_endpoint)

    @staticmethod
    def to_csv(data, filename, endpoint):
        with open(f"./data/{endpoint}/{filename}.csv", mode="a", newline="") as csvfile:
            fieldnames = data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data)
