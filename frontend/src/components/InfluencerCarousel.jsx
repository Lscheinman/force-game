import { useState, useEffect } from "react";
import { Card, CardContent, Typography, Button } from "@mui/material";

function InfluencerCarousel({ entityData, setZoomTarget }) {
  const [influencers, setInfluencers] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (entityData && entityData.entity_locations) {
      setInfluencers(entityData.entity_locations);
    }
  }, [entityData]);

  if (!influencers || influencers.length === 0) return null;

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % influencers.length);
  };

  const handlePrev = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + influencers.length) % influencers.length);
  };

  const handleCardClick = () => {
    const location = influencers[currentIndex]?.location;
    if (location) {
      console.log(`Zooming to: X=${location[0]}, Y=${location[1]}`);
      setZoomTarget(location); // Set zoom target in GameMap
    }
  };

  return (
    <Card 
      style={{ position: "absolute", top: 10, right: 10, background: "white", padding: "10px", zIndex: 10, width: "300px", cursor: "pointer" }} 
      onClick={handleCardClick}
    >
      <CardContent>
        <Typography variant="h6" style={{ textAlign: "center", marginBottom: "10px" }}>
          {influencers[currentIndex]?.name || "Unknown"}
        </Typography>

        {/* Influencer Image */}
        {influencers[currentIndex]?.path && (
          <img 
            src={influencers[currentIndex]?.path} 
            alt={influencers[currentIndex]?.name || "Influencer"} 
            style={{ width: "100%", height: "150px", objectFit: "cover", borderRadius: "5px", marginBottom: "10px" }}
          />
        )}

        {/* Condensed Info Section */}
        <div style={{ display: "grid", gridTemplateColumns: "auto auto", gap: "5px", fontSize: "14px" }}>
          <strong>Nation:</strong> <span>{influencers[currentIndex]?.nation || "Unknown"}</span>
          <strong>Role:</strong> <span>{influencers[currentIndex]?.role || "Unknown"}</span>
          <strong>Power:</strong> <span>{influencers[currentIndex]?.power || 0}</span>
          <strong>Experience:</strong> <span>{influencers[currentIndex]?.experience || 0}</span>
          <strong>Level:</strong> <span>{influencers[currentIndex]?.level || 0}</span>
          <strong>Evolution:</strong> 
          <span>{(influencers[currentIndex]?.evolution_steps || []).join(" → ")}</span>
        </div>
      </CardContent>

      {/* Navigation Buttons */}
      <div style={{ display: "flex", justifyContent: "space-between", padding: "10px" }}>
        <Button variant="contained" onClick={handlePrev}>Previous</Button>
        <Button variant="contained" onClick={handleNext}>Next</Button>
      </div>
    </Card>


  );
}

export default InfluencerCarousel;
