import os
import cv2
import numpy as np
import base64
from PIL import Image
from sklearn.cluster import KMeans
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent


class LLMColorAgent(BaseAgent):
    """Enhanced color agent that uses LLM for better color analysis."""

    def __init__(self, llm_client=None):
        super().__init__()
        self.llm_client = llm_client
        self.color_names = {
            "red": ["red", "crimson", "scarlet", "maroon"],
            "blue": ["blue", "navy", "cobalt", "azure"],
            "green": ["green", "emerald", "forest", "olive"],
            "yellow": ["yellow", "gold", "amber", "ochre"],
            "purple": ["purple", "violet", "lavender", "plum"],
            "orange": ["orange", "rust", "copper", "amber"],
            "brown": ["brown", "sienna", "umber", "tan"],
            "black": ["black", "charcoal", "ebony"],
            "white": ["white", "ivory", "cream"],
            "gray": ["gray", "grey", "silver", "charcoal"],
        }

    def process(self, metadata: Dict[str, Any], folder_path: str) -> Dict[str, Any]:
        """Analyze print image and suggest colors using LLM if available."""
        updated_metadata = metadata.copy()

        # Find print image
        image_path = self._find_print_image(folder_path)
        if not image_path:
            print(f"      🖼️  No print image found")
            self.logger.warning(f"No print image found in {folder_path}")
            return updated_metadata

        print(f"      🖼️  Analyzing image: {os.path.basename(image_path)}")

        # Try LLM analysis first, fallback to traditional method
        colors = self._analyze_colors_with_llm(image_path)
        if not colors:
            print(f"      🔄 LLM analysis failed, using traditional method")
            colors = self._analyze_colors_traditional(image_path)
        else:
            print(f"      🧠 LLM analysis successful")

        if colors:
            updated_metadata["colors_used"] = colors
            print(f"      🎨 Detected colors: {colors}")
            self.logger.info(f"Detected colors: {colors}")

        return updated_metadata

    def _analyze_colors_with_llm(self, image_path: str) -> Optional[List[str]]:
        """Analyze colors using LLM if available."""
        if not self.llm_client:
            return None

        try:
            # Encode image to base64
            image_base64 = self._encode_image_to_base64(image_path)
            if not image_base64:
                return None

            # Create prompt for LLM
            prompt = """Analyze this linocut print image and identify the specific art colors used. 
            
            Focus on:
            - Primary colors visible in the print
            - Use proper art color names (e.g., 'burnt sienna', 'forest green', 'ochre', 'ultramarine blue')
            - Consider the medium (linocut prints often use earthy, natural colors)
            - Identify 3-5 most prominent colors
            
            Return only the color names separated by commas, no explanations.
            Example: burnt sienna, forest green, ochre"""

            # Call LLM
            response = self.llm_client.analyze_image(prompt, image_base64)

            if response:
                # Parse response into color list
                colors = [color.strip() for color in response.split(",")]
                return colors[:5]  # Limit to 5 colors

        except Exception as e:
            self.logger.error(f"LLM color analysis failed: {e}")

        return None

    def _analyze_colors_traditional(self, image_path: str) -> List[str]:
        """Traditional color analysis using clustering (fallback method)."""
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

    def _encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """Encode image to base64 for LLM API with compression if needed."""
        try:
            # Check file size first
            file_size = os.path.getsize(image_path)
            max_size = 5 * 1024 * 1024  # 5MB

            if file_size > max_size:
                # Compress the image
                return self._compress_and_encode_image(image_path)
            else:
                # Use original image
                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                    return encoded_string

        except Exception as e:
            self.logger.error(f"Failed to encode image: {e}")
            return None

    def _compress_and_encode_image(self, image_path: str) -> Optional[str]:
        """Compress image to fit within API limits."""
        try:
            from PIL import Image
            import io

            # Open image
            with Image.open(image_path) as img:
                # Convert to RGB if needed
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Get original dimensions
                original_width, original_height = img.size
                print(
                    f"      📏 Original image size: {original_width}x{original_height}"
                )

                # Start with original size and high quality
                current_width, current_height = original_width, original_height
                quality = 85
                max_size = 5 * 1024 * 1024  # 5MB

                while True:
                    # Resize image if needed
                    if current_width > 1920 or current_height > 1920:
                        # Calculate new dimensions maintaining aspect ratio
                        if current_width > current_height:
                            new_width = 1920
                            new_height = int(current_height * 1920 / current_width)
                        else:
                            new_height = 1920
                            new_width = int(current_width * 1920 / current_height)

                        resized_img = img.resize(
                            (new_width, new_height), Image.Resampling.LANCZOS
                        )
                        print(f"      📐 Resized to: {new_width}x{new_height}")
                    else:
                        resized_img = img

                    # Save to bytes with current quality
                    img_bytes = io.BytesIO()
                    resized_img.save(
                        img_bytes, format="JPEG", quality=quality, optimize=True
                    )
                    compressed_size = img_bytes.tell()

                    print(f"      🗜️  Quality {quality}%: {compressed_size} bytes")

                    if compressed_size <= max_size or quality <= 10:
                        # Encode to base64
                        img_bytes.seek(0)
                        encoded_string = base64.b64encode(img_bytes.read()).decode(
                            "utf-8"
                        )
                        print(
                            f"      ✅ Final size: {compressed_size} bytes (under 5MB limit)"
                        )
                        return encoded_string

                    # Reduce quality first, then size if needed
                    if quality > 10:
                        quality -= 15
                    else:
                        # If quality is already low, reduce size
                        current_width = int(current_width * 0.8)
                        current_height = int(current_height * 0.8)
                        quality = 85  # Reset quality
                        print(
                            f"      📐 Reducing size to: {current_width}x{current_height}"
                        )

        except Exception as e:
            self.logger.error(f"Failed to compress image: {e}")
            return None

    def _find_print_image(self, folder_path: str) -> str:
        """Find the main print image in the folder."""
        image_extensions = [".jpg", ".jpeg", ".png"]

        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                # Prefer files with 'final' or 'print' in the name
                if "final" in file.lower() or "print" in file.lower():
                    return os.path.join(folder_path, file)

        # If no preferred file found, return first image
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                return os.path.join(folder_path, file)

        return None

    def _rgb_to_color_name(self, rgb: np.ndarray) -> str:
        """Convert RGB values to color name (fallback method)."""
        r, g, b = rgb

        # Simple color classification
        if r > 200 and g < 100 and b < 100:
            return "red"
        elif r < 100 and g < 100 and b > 200:
            return "blue"
        elif r < 100 and g > 200 and b < 100:
            return "green"
        elif r > 200 and g > 200 and b < 100:
            return "yellow"
        elif r > 200 and g < 100 and b > 200:
            return "purple"
        elif r > 200 and g > 100 and g < 200 and b < 100:
            return "orange"
        elif r > 100 and r < 200 and g > 50 and g < 150 and b < 100:
            return "brown"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        elif r > 200 and g > 200 and b > 200:
            return "white"
        elif abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
            return "gray"

        return None
