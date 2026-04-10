# ./animations/animations.py
# ================================================
# PokéLocker Animation Generator
# Generates animated GIFs for trainer poses + layered cosmetics
# Run this script to pre-generate animated preview files that your web app can use.
#
# Usage:
#   python ./animations/animations.py
#
# Requirements (run once):
#   pip install pillow
#
# Folder structure it expects (create these folders):
#   ./images/poses/                  ← base pose frames (e.g. stand_frame1.png, stand_frame2.png...)
#   ./images/cosmetics/hats/         ← your hat images
#   ./images/cosmetics/tops/         ← shirts, jackets, etc.
#   ./images/cosmetics/bottoms/
#   ./images/cosmetics/shoes/
#   ./images/cosmetics/accessories/
#   ./images/cosmetics/outfits/      ← full outfits if you want
#   ./animations/output/             ← generated animated GIFs go here (created automatically)

import os
from PIL import Image, ImageDraw, ImageFont
import glob

# ====================== CONFIG ======================
OUTPUT_DIR = "./animations/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# How many frames per animation (for idle bob / breathing effect)
FRAMES = 8
FPS = 12

# Slight "bob" offset for idle animation (pixels)
BOB_OFFSET = 4

# Layer order (bottom to top) - same as your web preview
LAYER_ORDER = ["pants", "shoes", "shirt", "jacket", "accessory", "hat"]

# Map web layer names → cosmetic folder names
LAYER_TO_FOLDER = {
    "hat": "hats",
    "shirt": "tops",
    "jacket": "outfits",
    "pants": "bottoms",
    "shoes": "shoes",
    "accessory": "accessories"
}

# ===================================================

def get_pose_frames(pose_name: str):
    """Return list of frame images for a pose (e.g. 'stand', 'victory', etc.)"""
    pattern = f"./images/poses/{pose_name}_frame*.png"
    frames = sorted(glob.glob(pattern))
    if not frames:
        # fallback to single static image if no frames exist
        static = f"./images/poses/{pose_name}.png"
        if os.path.exists(static):
            return [Image.open(static).convert("RGBA")] * FRAMES
        raise FileNotFoundError(f"No pose frames found for '{pose_name}'")
    return [Image.open(f).convert("RGBA") for f in frames]

def load_layer_image(layer_name: str, item_id: str):
    """Load a single cosmetic layer image"""
    folder = LAYER_TO_FOLDER.get(layer_name)
    if not folder:
        return None
    path = f"./images/cosmetics/{folder}/{item_id}.png"
    if os.path.exists(path):
        return Image.open(path).convert("RGBA")
    print(f"⚠️  Missing layer: {path}")
    return None

def composite_frame(base_frame: Image.Image, current_outfit: dict, frame_index: int):
    """Build one animated frame with all layers + bob effect"""
    width, height = base_frame.size
    composite = base_frame.copy()

    # Simple bob animation (up/down movement)
    bob_y = int(BOB_OFFSET * (frame_index % 4 < 2))  # 0 or BOB_OFFSET

    for layer_name in LAYER_ORDER:
        item_id = current_outfit.get(layer_name)
        if not item_id:
            continue

        layer_img = load_layer_image(layer_name, item_id)
        if layer_img is None:
            continue

        # Paste with bob offset
        paste_x = 0
        paste_y = bob_y
        composite.paste(layer_img, (paste_x, paste_y), layer_img)

    return composite

def generate_animated_gif(pose_name: str, current_outfit: dict, output_filename: str):
    """
    Main function: generates one animated GIF for a specific pose + outfit.
    current_outfit example:
    {
        "hat": "hat17",
        "shirt": "tops5",
        "jacket": None,
        "pants": "bottoms23",
        "shoes": "shoes9",
        "accessory": "accessory4"
    }
    """
    print(f"🎬 Generating animation → {output_filename}")

    base_frames = get_pose_frames(pose_name)

    # We will create FRAMES total (loop the base frames if needed)
    animated_frames = []

    for i in range(FRAMES):
        base = base_frames[i % len(base_frames)]
        frame = composite_frame(base, current_outfit, i)
        animated_frames.append(frame)

    # Save as GIF
    full_path = os.path.join(OUTPUT_DIR, output_filename)
    animated_frames[0].save(
        full_path,
        save_all=True,
        append_images=animated_frames[1:],
        duration=1000 // FPS,
        loop=0,
        optimize=True
    )
    print(f"✅ Saved: {full_path}\n")

# ====================== EXAMPLE USAGE ======================
if __name__ == "__main__":
    # Example 1: Default trainer with a few items (you can call this from anywhere)
    test_outfit = {
        "hat": "hat5",          # ← change to any of your real item IDs
        "shirt": "tops12",
        "jacket": None,
        "pants": "bottoms8",
        "shoes": "shoes3",
        "accessory": "accessory11"
    }

    generate_animated_gif(
        pose_name="stand",                     # must match your pose files
        current_outfit=test_outfit,
        output_filename="trainer_stand_test.gif"
    )

    # Example 2: Generate a few more variations automatically
    print("Generating extra variations...")
    poses_to_generate = ["stand", "victory", "throw"]   # add more as you create them

    for pose in poses_to_generate:
        for i in range(3):   # generate 3 random-looking variations per pose
            demo_outfit = {
                "hat": f"hat{(i*5)+3}",
                "shirt": f"tops{(i*7)+2}",
                "pants": f"bottoms{(i*4)+9}",
                "shoes": f"shoes{(i*2)+1}",
                "accessory": None
            }
            generate_animated_gif(
                pose_name=pose,
                current_outfit=demo_outfit,
                output_filename=f"trainer_{pose}_var{i+1}.gif"
            )
