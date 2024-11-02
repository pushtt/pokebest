from os import getenv
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection
from psycopg2 import sql, threadsafety
from logger import logger

load_dotenv()



def connect_to_pokemon_db():
    db_params = {
            "host": getenv("DB_HOST"),
            "port": getenv("DB_PORT"),
            "database": getenv("DB_DATABASE"),
            "password": getenv("DB_PASSWORD")
            }
    logger.info(f"Connect to Pokemon DW {db_params["database"]}")
    conn = psycopg2.connect(**db_params)
    print(conn.status)
    return conn

pokemon = {"name": "VARCHAR",
           "game": "VARCHAR"}


def create_table_query(table_name, conn:connection, **kwargs):
    cur = conn.cursor()
    query = sql.SQL("CREATE TABLE {table_name} ( {columns} )").format(
        table_name=sql.Identifier(table_name),
        columns=sql.SQL(',').join(
            sql.SQL("{column_name} {data_type}").format(
                column_name=sql.Identifier(k),
                data_type=sql.SQL(v)
            )
            for k,v in kwargs.items()
        )
    )
    logger.info(f"Generate DDL {query.as_string(conn)}...")
    cur.execute(query)
    logger.info(f"Run command...")


def load_csv_to_postgres(filename, table_name, conn:connection):
    cur = conn.cursor()
    logger.info(f"COPY data from {filename} to {table_name}")
    with open(filename, 'r') as f:
        next(f) # Skip the header row
        cur.copy_from(f, table_name, sep=",")

    conn.commit()


def main():
    conn = connect_to_pokemon_db()
    create_table_query("pokemon", conn, **pokemon)
    load_csv_to_postgres("./data/pokemon.csv", "pokemon", conn)
    conn.close()


if __name__ == "__main__":
    main()



