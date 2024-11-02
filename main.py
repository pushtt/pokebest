#!/Users/thinh/.pyenv/versions/3.12.7/bin/python
from pokeapi import GameEndpoint, PokeAPI, PokemonEndPoint
import json
import polars as pl

if __name__ == "__main__":
    poke_api = PokeAPI()
    results = poke_api.get_games(GameEndpoint.GENERATION)
    # with open(f"./data/pokemons.csv", "w") as f:
    for r in results:
        print(json.dumps(r))
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
