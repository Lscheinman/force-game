import { useEffect, useRef } from "react";
import { useThree } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";

function CameraControls({ zoomTarget, resetZoom }) {
  const { camera } = useThree();
  const controls = useRef();
  const isAnimating = useRef(false);

  useEffect(() => {
    if (zoomTarget && controls.current) {
      isAnimating.current = true;
      const targetPosition = new THREE.Vector3(zoomTarget[0], zoomTarget[1], 10);
      const currentPosition = new THREE.Vector3().copy(camera.position);
      const tiltAngle = Math.PI / 6; // 30-degree tilt angle
      
      const animateZoom = () => {
        if (currentPosition.distanceTo(targetPosition) > 0.1) {
          currentPosition.lerp(targetPosition, 0.05); // Gradual slow-down effect
          camera.position.copy(currentPosition);
          camera.lookAt(targetPosition.x, targetPosition.y, 0);
          controls.current.target.set(targetPosition.x, targetPosition.y, 0);
          camera.rotation.x = -tiltAngle; // Tilt to 30 degrees downward
          requestAnimationFrame(animateZoom);
        } else {
          isAnimating.current = false;
        }
      };
      animateZoom();
    }
  }, [zoomTarget, camera]);

  // Handle double-click to reset the camera
  useEffect(() => {
    const handleDoubleClick = () => {
      if (!isAnimating.current) {
        camera.position.set(0, 0, 20);
        camera.lookAt(0, 0, 0);
        controls.current.target.set(0, 0, 0);
        resetZoom(); 
      }
    };
    window.addEventListener("dblclick", handleDoubleClick);
    return () => window.removeEventListener("dblclick", handleDoubleClick);
  }, [resetZoom, camera]);

  return <OrbitControls ref={controls} enablePan enableZoom enableRotate />;
}

export default CameraControls;
