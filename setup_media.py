import os
import shutil
from pathlib import Path

def setup_media_directory():
    """
    Set up the media directory structure and create necessary default files.
    Run this script after running migrations to ensure media files are in place.
    """
    BASE_DIR = Path(__file__).resolve().parent
    
    # Create media directories if they don't exist
    media_dir = BASE_DIR / 'media'
    profile_pics_dir = media_dir / 'profile_pics'
    receipts_dir = media_dir / 'receipts'
    vehicle_pics_dir = media_dir / 'vehicle_pics'
    
    os.makedirs(profile_pics_dir, exist_ok=True)
    os.makedirs(receipts_dir, exist_ok=True)
    os.makedirs(vehicle_pics_dir, exist_ok=True)
    
    # Create default profile image if it doesn't exist
    default_image_path = media_dir / 'default.png'
    if not default_image_path.exists():
        # Copy from static directory if available
        static_default = BASE_DIR / 'static' / 'images' / 'default-profile.png'
        if static_default.exists():
            print("Copying default profile image from static to media...")
            shutil.copy(static_default, default_image_path)
        else:
            print("Default profile image not found in static directory.")
            print("Please add a default.png file to the media directory manually.")
    
    print("Media directory structure set up successfully!")

if __name__ == "__main__":
    setup_media_directory() 