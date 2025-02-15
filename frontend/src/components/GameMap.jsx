import { useEffect, useState, useMemo, useRef } from "react";
import { Canvas, useLoader, useThree } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import { Card, CardContent, Typography } from "@mui/material";
import CameraControls from "./CameraControls";
import InfluencerCarousel from "./InfluencerCarousel";

// Preload textures once and cache them
const preloadTextures = () => {
  const textures = {};
  ["water", "land", "mountain"].forEach((type) => {
    for (let i = 1; i <= 6; i++) {
      textures[`${type}_${i}`] = new THREE.TextureLoader().load(`/textures/${type}_${i}.jpg`);
    }
    textures[type] = new THREE.TextureLoader().load(`/textures/${type}.jpg`); // Default fallback
  });
  return textures;
};

function Tile({ position, height, texture, onClick }) {
  return (
    <mesh position={[position[0], position[1], height / 2]} onClick={onClick} castShadow receiveShadow>
      <boxGeometry args={[1, 1, Math.max(height, 0.75)]} />
      <meshStandardMaterial attach="material" map={texture} />
    </mesh>
  );
}

function Building({ position }) {
  return (
    <mesh position={[position[0], position[1], 0.75]} castShadow receiveShadow>
      <boxGeometry args={[0.5, 0.5, 1.5]} />
      <meshStandardMaterial attach="material" color="gray" />
    </mesh>
  );
}

function TileDetails({ selectedTile }) {
  if (!selectedTile) return null;

  return (
    <Card style={{ position: "absolute", top: 10, left: 10, background: "white", padding: "10px", zIndex: 10, width: "250px" }}>
      <CardContent>
        <Typography variant="h6">Selected Tile</Typography>
        <Typography variant="body1">Position: {selectedTile.x}, {selectedTile.y}</Typography>
        <Typography variant="body1">Elevation: {selectedTile.elevation.toFixed(2)}</Typography>
        <Typography variant="body1">Terrain: {selectedTile.terrain}</Typography>
        <Typography variant="body1">Country: {selectedTile.country}</Typography>
        {selectedTile.influencer && <Typography variant="body1">Influencer: {selectedTile.influencer}</Typography>}
      </CardContent>
    </Card>
  );
}

function GameMap() {
  const [mapData, setMapData] = useState(null);
  const [selectedTile, setSelectedTile] = useState(null);
  const [zoomTarget, setZoomTarget] = useState(null);
  const textures = useMemo(preloadTextures, []);

  const resetZoom = () => {
    setZoomTarget([0, 0]);
  };

  useEffect(() => {
    fetch("http://localhost:8000/builder/game/start")
      .then(response => response.json())
      .then(data => setMapData(data));
  }, []);

  if (!mapData) return <div>Loading map...</div>;

  const { map, elevation, terrain, buildings, countries, entity_names, entities, entity_locations } = mapData;

  return (
    <div style={{ width: "100vw", height: "100vh", position: "relative" }}>
      <TileDetails selectedTile={selectedTile} />
      <InfluencerCarousel entityData={{ entity_locations }} setZoomTarget={setZoomTarget} />
      <Canvas camera={{ position: [0, 0, 20], fov: 50 }} style={{ width: "100%", height: "100%" }} shadows>
        <ambientLight intensity={0.8} />
        <directionalLight position={[10, 10, 10]} intensity={1} castShadow />
        <CameraControls zoomTarget={zoomTarget} resetZoom={resetZoom} />
        {map.map((row, x) =>
          row.map((_, y) => {
            const height = elevation[x][y] * 5;
            const countryIndex = countries[x][y].split(" ")[1]; // Extract country number
            const terrainKey = `${terrain[x][y]}_${countryIndex}`;
            const texture = textures[terrainKey] || textures[terrain[x][y]] || textures.land;
            const influencer = entity_names && entity_names[x][y] ? entity_names[x][y] : null;
            return (
              <Tile
                key={`${x}-${y}`}
                position={[x - 10, y - 10]}
                height={height}
                texture={texture}
                onClick={() => setSelectedTile({ 
                  x, 
                  y, 
                  elevation: elevation[x][y], 
                  terrain: terrain[x][y], 
                  country: countries[x][y],
                  influencer
                })}
              />
            );
          })
        )}
        {buildings.map((building, index) => (
          <Building key={index} position={[building.x - 10, building.y - 10]} />
        ))}
      </Canvas>
    </div>
  );
}

export default GameMap;
