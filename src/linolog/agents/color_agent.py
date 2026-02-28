import os
import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from typing import Dict, Any, List
from .base_agent import BaseAgent

class ColorAgent(BaseAgent):
    """Agent that analyzes print images to detect colors using color clustering."""
    
    def __init__(self):
        super().__init__()
        self.color_names = {
            'red': ['red', 'crimson', 'scarlet', 'maroon'],
            'blue': ['blue', 'navy', 'cobalt', 'azure'],
            'green': ['green', 'emerald', 'forest', 'olive'],
            'yellow': ['yellow', 'gold', 'amber', 'ochre'],
            'purple': ['purple', 'violet', 'lavender', 'plum'],
            'orange': ['orange', 'rust', 'copper', 'amber'],
            'brown': ['brown', 'sienna', 'umber', 'tan'],
            'black': ['black', 'charcoal', 'ebony'],
            'white': ['white', 'ivory', 'cream'],
            'gray': ['gray', 'grey', 'silver', 'charcoal']
        }
    
    def process(self, metadata: Dict[str, Any], folder_path: str) -> Dict[str, Any]:
        """Analyze print image and suggest colors."""
        updated_metadata = metadata.copy()
        
        # Find print image
        image_path = self._find_print_image(folder_path)
        if not image_path:
            print(f"      🖼️  No print image found")
            self.logger.warning(f"No print image found in {folder_path}")
            return updated_metadata
        
        print(f"      🖼️  Analyzing image: {os.path.basename(image_path)}")
        # Analyze colors
        colors = self._analyze_colors(image_path)
        if colors:
            updated_metadata['colors_used'] = colors
            print(f"      🎨 Detected colors: {colors}")
            self.logger.info(f"Detected colors: {colors}")
        
        return updated_metadata
    
    def _find_print_image(self, folder_path: str) -> str:
        """Find the main print image in the folder."""
        image_extensions = ['.jpg', '.jpeg', '.png']
        
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                # Prefer files with 'final' or 'print' in the name
                if 'final' in file.lower() or 'print' in file.lower():
                    return os.path.join(folder_path, file)
        
        # If no preferred file found, return first image
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                return os.path.join(folder_path, file)
        
        return None
    
    def _analyze_colors(self, image_path: str) -> List[str]:
        """Analyze image and return detected colors."""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                self.logger.error(f"Failed to load image: {image_path}")
                return []
            
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Reshape image for clustering
            pixels = image_rgb.reshape(-1, 3)
            
            # Use K-means to find dominant colors
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Get cluster centers (dominant colors)
            colors = kmeans.cluster_centers_.astype(int)
            
            # Convert to color names
            color_names = []
            for color in colors:
                color_name = self._rgb_to_color_name(color)
                if color_name and color_name not in color_names:
                    color_names.append(color_name)
            
            return color_names[:3]  # Return top 3 colors
            
        except Exception as e:
            self.logger.error(f"Error analyzing colors: {e}")
            return []
    
    def _rgb_to_color_name(self, rgb: np.ndarray) -> str:
        """Convert RGB values to color name."""
        r, g, b = rgb
        
        # Simple color classification
        if r > 200 and g < 100 and b < 100:
            return 'red'
        elif r < 100 and g < 100 and b > 200:
            return 'blue'
        elif r < 100 and g > 200 and b < 100:
            return 'green'
        elif r > 200 and g > 200 and b < 100:
            return 'yellow'
        elif r > 200 and g < 100 and b > 200:
            return 'purple'
        elif r > 200 and g > 100 and g < 200 and b < 100:
            return 'orange'
        elif r > 100 and r < 200 and g > 50 and g < 150 and b < 100:
            return 'brown'
        elif r < 50 and g < 50 and b < 50:
            return 'black'
        elif r > 200 and g > 200 and b > 200:
            return 'white'
        elif abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
            return 'gray'
        
        return None 