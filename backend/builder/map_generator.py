import os
import numpy as np
import random
import json
from fastapi import APIRouter, HTTPException
from scipy.spatial import Voronoi
from fastapi.responses import JSONResponse
from noise import pnoise2
from loguru import logger
from builder.schemas import MapConfig


# Define API router
router = APIRouter()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "map_config.json")

# Load configuration from JSON file
def load_config():
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)

config = load_config()

logger.info("Initializing map generation parameters")

def generate_voronoi_map():
    """
    Generates a procedural map using Voronoi segmentation and Perlin noise.
    Assigns countries, terrain, and elevation data.
    """
    try:
        logger.info("Generating country centers")
        country_centers = np.array([[random.randint(0, config["MAP_WIDTH"]), random.randint(0, config["MAP_HEIGHT"]) ] for _ in range(config["COUNTRIES"])])
        vor = Voronoi(country_centers)
        
        country_map = np.zeros((config["MAP_WIDTH"], config["MAP_HEIGHT"]), dtype=int)
        elevation_map = np.zeros((config["MAP_WIDTH"], config["MAP_HEIGHT"]), dtype=float)
        terrain_map = np.zeros((config["MAP_WIDTH"], config["MAP_HEIGHT"]), dtype=object)
        country_names = [f"Country {i+1}" for i in range(config["COUNTRIES"])]
        country_assignment = np.full((config["MAP_WIDTH"], config["MAP_HEIGHT"]), "", dtype=object)
        buildings = []
        grid_coordinates = []

        logger.info("Generating terrain, assigning countries, and adding additional map data")
        for i in range(config["MAP_WIDTH"]):
            for j in range(config["MAP_HEIGHT"]):
                grid_coordinates.append((i, j))
                elevation = pnoise2(i / config["SCALE"], j / config["SCALE"], octaves=config["OCTAVES"], persistence=config["PERSISTENCE"], lacunarity=config["LACUNARITY"])
                elevation_map[i, j] = elevation
                
                point = np.array([i, j])
                distances = [np.linalg.norm(point - center) for center in country_centers]
                country_index = np.argmin(distances)
                country_map[i, j] = country_index
                country_assignment[i, j] = country_names[country_index]
                
                if elevation < config["SEA_LEVEL"]:
                    terrain_map[i, j] = "water"
                elif elevation > config["MOUNTAIN_THRESHOLD"]:
                    terrain_map[i, j] = "mountain"
                else:
                    terrain_map[i, j] = "land"
                    if random.random() < config["BUILDING_DENSITY"]:
                        buildings.append({"x": i, "y": j, "type": "building"})
        
        logger.info("Map generation complete")
        return {
            "map": country_map.tolist(),
            "countries": country_assignment.tolist(),
            "voronoi_vertices": vor.vertices.tolist(),
            "elevation": elevation_map.tolist(),
            "terrain": terrain_map.tolist(),
            "grid_coordinates": grid_coordinates,
            "buildings": buildings
        }
    except Exception as e:
        logger.error(f"Error during map generation: {e}")
        return {"error": "Failed to generate map"}

@router.get("/generate-map")
def get_map():
    """
    API route to generate and return a procedural map.
    """
    logger.info("Processing API request for /generate-map")
    map_data = generate_voronoi_map()
    return JSONResponse(content=map_data)

@router.post("/update-config")
def update_config(new_config: MapConfig):
    """
    API route to update the map configuration.
    """
    try:
        with open(CONFIG_PATH, "w") as file:
            json.dump(new_config, file, indent=4)
        global config
        config = load_config()
        logger.info("Map configuration updated successfully")
        return {"message": "Configuration updated successfully"}
    except Exception as e:
        logger.error(f"Failed to update configuration: {e}")
        raise HTTPException(status_code=500, detail="Failed to update configuration")
