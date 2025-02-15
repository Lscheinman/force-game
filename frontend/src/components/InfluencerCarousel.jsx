import { useState, useEffect } from "react";
import { Card, CardContent, Typography, Button } from "@mui/material";

function InfluencerCarousel({ entityData }) {
  const [influencers, setInfluencers] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (entityData && entityData.entities) {
      setInfluencers(entityData.entities);
    }
  }, [entityData]);

  if (!influencers || influencers.length === 0) return null;

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % influencers.length);
  };

  const handlePrev = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + influencers.length) % influencers.length);
  };

  return (
    <Card style={{ position: "absolute", top: 10, right: 10, background: "white", padding: "10px", zIndex: 10, width: "300px" }}>
      <CardContent>
        <Typography variant="h6">Influencer</Typography>
        <Typography variant="body1">Name: {influencers[currentIndex]?.name || "Unknown"}</Typography>
        <Typography variant="body1">Nation: {influencers[currentIndex]?.nation || "Unknown"}</Typography>
        <Typography variant="body1">Role: {influencers[currentIndex]?.role || "Unknown"}</Typography>
        <Typography variant="body1">Description: {influencers[currentIndex]?.description || "No description available"}</Typography>
        <Typography variant="body1">Power: {influencers[currentIndex]?.power || 0}</Typography>
        <Typography variant="body1">Experience: {influencers[currentIndex]?.experience || 0}</Typography>
        <Typography variant="body1">Level: {influencers[currentIndex]?.level || 0}</Typography>
        <Typography variant="body1">Evolution: {(influencers[currentIndex]?.evolution_steps || []).join(" → ")}</Typography>
      </CardContent>
      <div style={{ display: "flex", justifyContent: "space-between", padding: "10px" }}>
        <Button variant="contained" onClick={handlePrev}>Previous</Button>
        <Button variant="contained" onClick={handleNext}>Next</Button>
      </div>
    </Card>
  );
}

export default InfluencerCarousel;
