from pydantic import BaseModel, Field
from typing import Dict

class MapConfig(BaseModel):
    MAP_WIDTH: int = Field(..., gt=0, description="Width of the map")
    MAP_HEIGHT: int = Field(..., gt=0, description="Height of the map")
    COUNTRIES: int = Field(..., gt=0, description="Number of countries")
    SCALE: float = Field(..., gt=0, description="Scaling factor for noise generation")
    OCTAVES: int = Field(..., gt=0, description="Number of noise octaves")
    PERSISTENCE: float = Field(..., gt=0, description="Persistence factor for terrain generation")
    LACUNARITY: float = Field(..., gt=0, description="Lacunarity factor for noise variation")
    SEA_LEVEL: float = Field(..., description="Sea level threshold")
    MOUNTAIN_THRESHOLD: float = Field(..., description="Mountain threshold for elevation")
    BUILDING_DENSITY: float = Field(..., ge=0, le=1, description="Probability of buildings on land")

class GameConfig(BaseModel):
    MAX_PLAYERS: int = Field(..., ge=1, le=12, description="Maximum number of players")
    AUTO_PLAY: bool = Field(..., description="Whether all players are controlled by AI")
    TURN_LIMIT: int = Field(..., gt=0, description="Number of turns before the game ends")
    STARTING_RESOURCES: Dict[str, int] = Field(..., description="Starting resources for each player")
    DIFFICULTY: str = Field(..., description="Game difficulty level")
