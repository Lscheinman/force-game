from pyArango.connection import Connection
import os
from loguru import logger

# Database configuration
DB_NAME = "force_game"
ARANGO_URL = os.getenv("ARANGO_URL", "http://localhost:8529")
USERNAME = os.getenv("ARANGO_USER", "root")
PASSWORD = os.getenv("ARANGO_PASSWORD", "9neSH4PtBnt1qrxy")

# Initialize the ArangoDB connection
logger.info("Connecting to ArangoDB at {}", ARANGO_URL)
conn = Connection(arangoURL=ARANGO_URL, username=USERNAME, password=PASSWORD)

# Ensure the database exists
def setup_database():
    logger.info("Setting up database: {}", DB_NAME)
    if DB_NAME not in conn.databases:
        conn.createDatabase(DB_NAME)
        logger.info("Database {} created", DB_NAME)
    else:
        logger.info("Database {} already exists", DB_NAME)

    db = conn[DB_NAME]
    collections = ["games", "entities", "map_tiles"]
    for col in collections:
        if col not in db.collections:
            db.createCollection(name=col)
            logger.info("Collection {} created", col)
        else:
            logger.info("Collection {} already exists", col)

def get_db():
    logger.info("Returning database instance")
    return conn[DB_NAME]

def get_game(name: str):
    """
    Returns the 'games' collection from the ArangoDB database.
    """
    db = get_db()
    games_collection = db["games"]
    query = f'FOR game IN games FILTER game.name == "{name}" RETURN game'
    results = list(db.AQLQuery(query, rawResults=True))
    if results:
        game_doc = games_collection[results[0]["_key"]] 
        return game_doc
    else:
        logger.info(f"Game not found: {name}")
        return None

def save_game_to_db(game_data: dict):
    """
    Saves or updates a game session in the ArangoDB 'games' collection.
    """
    game_name = game_data.get("name")
    try:
        db = get_db()
        games_collection = db["games"]

        game_doc = get_game(game_name)
        if game_doc: 
            game_doc.set(game_data)
            game_doc.save()
            logger.info(f"Updated existing game: {game_name}")
        else:
            new_game = games_collection.createDocument()
            new_game.set(game_data)
            new_game.save()
            logger.info(f"Saved new game: {game_name}")
    except Exception as e:
        logger.error(f"Failed to save game: {e}")
        raise

def load_game_from_db(game_name: str):
    """
    Loads a game session from the ArangoDB 'games' collection.
    """
    try:
        game_doc = get_game(game_name)
        if not game_doc:
            return None
        return game_doc.getStore()
    except Exception as e:
        logger.error(f"Failed to load game: {e}")
        raise

def delete_game_from_db(game_name: str):
    """
    Deletes a game session from the ArangoDB 'games' collection.
    """
    try:
        game_doc = get_game(game_name)
        if not game_doc:
            return None
        game_doc.delete()
        logger.info(f"Deleted game: {game_name}")
    except Exception as e:
        logger.error(f"Failed to delete game: {e}")
        raise

setup_database()