from fastapi import APIRouter
from fastapi.responses import JSONResponse
import json
import string
import os
import random
from loguru import logger
from builder.map_generator import generate_voronoi_map

# Define API router
router = APIRouter()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config",  "world_config.json")

def load_entities():
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Failed to load entity config: {e}")
        return {}

def create_world_map(world=None):
    """
    Creates a map with a random name and then
    - creates a map from the map_generator
    - assigns entities to the map
    - returns the map of countries with assigned entities for additional game layers
    """
    if not world:
        world = f"World {random.randint(1, 1000)}-{random.choice(string.ascii_uppercase)}"
    
    logger.info(f"Creating map for world {world}")
    world_map = assign_entities_to_map(generate_voronoi_map())
    world_map["name"] = world
    return world_map

def assign_entities_to_map(map_data):
    """
    Assigns entities to the map based on the nation index. Each entity is placed on a random
    tile corresponding to its designated country in the map matrix.
    
    Args:
        map_data (dict): The generated map data containing country assignments.
    
    Returns:
        dict: Updated map data with assigned entities.
    """
    entities = load_entities()
    entity_locations = []
    logger.info(f"Loaded {len(entities.get('entities', []))} entities")
    logger.info(entities)
    rows, cols = len(map_data["map"]), len(map_data["map"][0])
    
    # Initialize a matrix with None values to store entity placements
    assigned_entities = [[None for _ in range(cols)] for _ in range(rows)]
    
    # Group tiles by country index
    country_tiles = {}
    for i, row in enumerate(map_data["map"]):
        for j, country_index in enumerate(row):
            if country_index not in country_tiles:
                country_tiles[country_index] = []
            country_tiles[country_index].append((i, j))
    
    # Iterate through entities and place them randomly within their assigned nation
    for entity in entities.get("entities", []):
        nation_index = entity.get("map")
        logger.info(f"Placing entity {entity['path']} on country {nation_index}")
        if nation_index in country_tiles and country_tiles[nation_index]:
            tile = random.choice(country_tiles[nation_index])  # Select a random tile
            assigned_entities[tile[0]][tile[1]] = entity["path"]  # Assign entity path to tile
            country_tiles[nation_index].remove(tile)
            entity['location'] = tile
            entity_locations.append(entity) # Remove assigned tile from available slots
    
    # Store the assigned entity matrix in map data
    map_data["entities"] = assigned_entities
    map_data["entity_locations"] = entity_locations  # Store entity locations for game logic
    return map_data

@router.get("/generate-entity-map")
def get_map():
    logger.info("Processing API request for /generate-entity-map")
    map = create_world_map()
    return JSONResponse(content=map)