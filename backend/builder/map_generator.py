from fastapi import APIRouter
import numpy as np
import random
from scipy.spatial import Voronoi
from fastapi.responses import JSONResponse
from noise import pnoise2
from loguru import logger

# Define API router
router = APIRouter()

MAP_WIDTH = 20
MAP_HEIGHT = 20
COUNTRIES = 6
SCALE = 10.0  # Scale for Perlin noise
OCTAVES = 6  # Increased for more detail
PERSISTENCE = 0.6  # Adjusted for smoother transitions
LACUNARITY = 2.5  # Increased for more terrain variety
SEA_LEVEL = -0.05  # Define sea level threshold
MOUNTAIN_THRESHOLD = 0.6  # Define mountain threshold
BUILDING_DENSITY = 0.02  # Probability of a building on a land tile

logger.info("Initializing map generation parameters")

def generate_voronoi_map():
    try:
        logger.info("Generating country centers")
        country_centers = np.array([[random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT)] for _ in range(COUNTRIES)])
        vor = Voronoi(country_centers)
        
        country_map = np.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=int)
        elevation_map = np.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=float)
        terrain_map = np.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=object)
        country_names = [f"Country {i+1}" for i in range(COUNTRIES)]
        country_assignment = np.full((MAP_WIDTH, MAP_HEIGHT), "", dtype=object)
        buildings = []
        grid_coordinates = []

        logger.info("Generating terrain, assigning countries, and adding additional map data")
        for i in range(MAP_WIDTH):
            for j in range(MAP_HEIGHT):
                grid_coordinates.append((i, j))
                # Generate elevation using Perlin noise
                elevation = pnoise2(i / SCALE, j / SCALE, octaves=OCTAVES, persistence=PERSISTENCE, lacunarity=LACUNARITY)
                elevation_map[i, j] = elevation
                
                # Assign country based on Voronoi distance
                point = np.array([i, j])
                distances = [np.linalg.norm(point - center) for center in country_centers]
                country_index = np.argmin(distances)
                country_map[i, j] = country_index
                country_assignment[i, j] = country_names[country_index]
                
                # Determine terrain type based on elevation
                if elevation < SEA_LEVEL:
                    terrain_map[i, j] = "water" 
                elif elevation > MOUNTAIN_THRESHOLD:
                    terrain_map[i, j] = "mountain"
                else:
                    terrain_map[i, j] = "land"
                    # Randomly place buildings on land tiles
                    if random.random() < BUILDING_DENSITY:
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
    logger.info("Processing API request for /generate-map")
    return JSONResponse(content=generate_voronoi_map())
