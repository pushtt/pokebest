#!/Users/thinh/.pyenv/versions/3.12.7/bin/python
import logging
from pokeapi import PokeAPI, PokemonEndPoints
import json
import polars as pl

if __name__ == "__main__":
    poke_api = PokeAPI(logger_level=logging.INFO)
    generation = poke_api.get_endpoint(PokemonEndPoints.Generation)
    data = []
    for g in generation:
        data.append(poke_api.get_endpoint(PokemonEndPoints.Generation, g["name"]))

    poke_api.to_csv(data, "generation", PokemonEndPoints.Generation)
    # df = pl.from_dicts(results)
    # # df.write_csv("./data/pokemon.csv")
    # df = pl.read_csv("./data/pokemon.csv")
    # pokemon = []
    # for name in df["name"]:
    #     df1 = poke_api.get_pokemon(PokemonEndPoint.POKEMON, name)
    #     pokemon.append(df1)
    #
    # for poke in pokemon:
    #     poke_api.to_csv(poke, "./data/pokemon_details.csv")
