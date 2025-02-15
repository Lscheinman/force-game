import json
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from builder.world_generator import create_world_map
from builder.schemas import GameConfig
from database.client import save_game_to_db, load_game_from_db, delete_game_from_db

# Define API router
router = APIRouter()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "game_config.json")

# Load configuration from JSON file
def load_game_config():
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)

def validate_game_config(new_config):
    """
    Validates incoming game configuration updates to ensure only known keys are modified.
    """
    allowed_keys = {"MAX_PLAYERS", "AUTO_PLAY", "TURN_LIMIT", "STARTING_RESOURCES", "DIFFICULTY"}
    if not all(key in allowed_keys for key in new_config.keys()):
        raise ValueError("Invalid game configuration keys provided.")

def setup_game(game_name=None):
    """
    Sets up a new game session.
    - Generates a world map
    - Assigns players (human or AI)
    - Applies game settings from configuration
    """
    
    game_config = load_game_config()
    logger.info(f"Creating new game: {game_name}")
    game = create_world_map(world=game_name)
    
    players = []
    for i in range(game_config["MAX_PLAYERS"]):
        players.append({
            "id": i + 1,
            "name": f"Player {i+1}",
            "human": not game_config["AUTO_PLAY"],
            "resources": game_config["STARTING_RESOURCES"]
        })
    
    game["players"] = players
    game["turn_limit"] = game_config["TURN_LIMIT"]
    game["difficulty"] = game_config["DIFFICULTY"]
    game["current_round"] = game_config["CURRENT_ROUND"]
    game["moves"] = []
    return game

@router.get("/start")
def start_game():
    """
    API route to create and return a new game session.
    """
    logger.info("Processing API request for /start-game")
    game_data = setup_game()
    return JSONResponse(content=game_data)

@router.post("/update-game-config")
def update_game_config(new_config: GameConfig):
    """
    API route to update the game configuration.
    """
    try:
        validate_game_config(new_config)
        with open(CONFIG_PATH, "w") as file:
            json.dump(new_config, file, indent=4)
        global game_config
        game_config = load_game_config()
        logger.info("Game configuration updated successfully")
        return {"message": "Game configuration updated successfully"}
    except ValueError as ve:
        logger.error(f"Invalid game configuration update: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Failed to update game configuration: {e}")
        raise HTTPException(status_code=500, detail="Failed to update game configuration")

@router.post("/save")
def save_game(game_data: dict):
    """
    API route to save or update a game session in ArangoDB.
    """
    save_game_to_db(game_data=game_data)
    return {"message": "Game saved successfully"}


@router.post("/load")
def load_game(game_name: str):
    """
    API route to save or update a game session in ArangoDB.
    """
    game_data = load_game_from_db(game_name=game_name)
    if game_data:
        logger.info(f"{game_name} loaded")
    else:
        logger.info(f"{game_name} not found")
    return JSONResponse(content=game_data)


@router.post("/delete")
def delete_game(game_name: str):
    """
    API route to save or update a game session in ArangoDB.
    """
    game_data = delete_game_from_db(game_name=game_name)
    if game_data:
        logger.info(f"{game_name} deleted")
    else:
        logger.info(f"{game_name} not found")
    return JSONResponse(content=game_data)
