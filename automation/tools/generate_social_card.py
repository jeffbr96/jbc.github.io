# generate_social_card.py
#
# This script automates the creation of social media preview cards for a Jekyll blog.
# It is written to be compatible with older versions of Python (3.9-) and Pillow (<10.0).
#
# It performs the following steps:
# 1. Finds the most recent post in the `_posts` directory.
# 2. Reads the post's front matter to get the main image path and the excerpt.
# 3. Resizes the main image to a standard social media size (1200x630).
# 4. Adds a semi-transparent "glassy" background behind the text.
# 5. Dynamically adjusts font size to fit the text, then wraps and writes it.
# 6. Saves the new image in the same directory as the original, appending ".social.media" to the filename.
# 7. Updates the original post's front matter with a new `social_image` field pointing to the generated card.
#
# Dependencies:
# - Pillow: `pip install Pillow`
# - PyYAML: `pip install PyYAML`

import os
import glob
import yaml
import re
import textwrap
from typing import Union
from PIL import Image, ImageDraw, ImageFont

# --- OS-Aware Configuration ---
if os.name == 'nt': # Native Windows
    PROJECT_ROOT = "C:/Users/jeffb/OneDrive/Desktop/Blog/jbc.github.io"
    # Note: Calibri is a common Windows font. If not found, you might need to
    # provide a path to another font like "C:/Windows/Fonts/seguib.ttf" (Segoe UI Bold)
    FONT_PATH = "C:/Windows/Fonts/ELEPHNT.ttf" # Calibri Regular
else: # Linux, macOS, or Windows Subsystem for Linux (WSL)
    PROJECT_ROOT = "/mnt/c/Users/jeffb/OneDrive/Desktop/Blog/jbc.github.io"
    FONT_PATH = "/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf" # Common path for Roboto Regular

# --- General Configuration ---
POSTS_DIR = os.path.join(PROJECT_ROOT, "_posts")
RESIZE_DIMS = (1200, 630)
TEXT_COLOR = (66, 62, 0) # Almost black yellow
GLASS_COLOR = (255, 255, 255, 180) # White, ~47% transparent

def find_latest_post() -> Union[str, None]:
    """Finds the most recent post file based on filename."""
    list_of_posts = glob.glob(os.path.join(POSTS_DIR, "*.md"))
    if not list_of_posts:
        return None
    latest_post = max(list_of_posts, key=os.path.getctime)
    return latest_post

def parse_post(post_path: str) -> Union[dict, None]:
    """Parses the front matter and content of a post."""
    try:
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except IOError:
        return None

    match = re.search(r'---\s*(.*?)\s*---', content, re.DOTALL)
    if not match:
        return None

    front_matter_str = match.group(1)
    try:
        front_matter = yaml.safe_load(front_matter_str)
        front_matter['full_content'] = content[match.end():].strip()
        return front_matter
    except yaml.YAMLError:
        return None

def get_excerpt(front_matter: dict) -> str:
    """Gets the excerpt from front matter or generates it from content."""
    if front_matter.get('excerpt'):
        return front_matter['excerpt']
    
    paragraphs = front_matter.get('full_content', '').split('\n\n')
    for p in paragraphs:
        if p.strip():
            return p.strip()
    return "Read more on the blog"

def generate_social_card(image_path: str, output_path: str, text: str):
    """Resizes an image and adds a glassy background and dynamically sized text."""
    try:
        with Image.open(image_path) as img:
            img = img.resize(RESIZE_DIMS).convert("RGBA")
            draw_temp = ImageDraw.Draw(img)

            # --- Dynamic Font Sizing ---
            font_sizes = [60, 54, 48, 42, 36, 30]
            max_text_height = RESIZE_DIMS[1] * 0.7  # Allow text to take up to 70% of card height
            
            font = None
            wrapped_text = ""
            text_width = 0
            text_height = 0

            for size in font_sizes:
                try:
                    font = ImageFont.truetype(FONT_PATH, size)
                except IOError:
                    print(f"Warning: Font not found at {FONT_PATH}. Using default PIL font.")
                    font = ImageFont.load_default()

                # Calculate wrap width based on current font size
                try:
                    avg_char_width = sum(font.getsize(c)[0] for c in 'abcdefghijklmnopqrstuvwxyz') / 26
                except AttributeError:
                    avg_char_width = font.getsize('a')[0]
                
                wrap_width = int((RESIZE_DIMS[0] * 0.9) / avg_char_width)
                wrapped_text = textwrap.fill(text, width=wrap_width)

                # Measure the height of the wrapped text
                try:
                    text_width, text_height = draw_temp.multiline_textsize(wrapped_text, font=font)
                except AttributeError:
                    text_width, text_height = (RESIZE_DIMS[0] * 0.8, RESIZE_DIMS[1] * 0.5)

                if text_height <= max_text_height:
                    print(f"✅ Text fits. Selected font size: {size}px")
                    break # Found a suitable font size
            else: # This 'else' belongs to the 'for' loop
                print(f"⚠️ Text may be too long. Using smallest font size: {font_sizes[-1]}px")
            # --- End Dynamic Font Sizing ---

            x = (RESIZE_DIMS[0] - text_width) / 2
            y = (RESIZE_DIMS[1] - text_height) / 2

            # --- Glassy Background ---
            overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
            draw_overlay = ImageDraw.Draw(overlay)

            padding = 40
            rect_x0 = x - padding
            rect_y0 = y - padding
            rect_x1 = x + text_width + padding
            rect_y1 = y + text_height + padding
            
            try:
                draw_overlay.rounded_rectangle(
                    (rect_x0, rect_y0, rect_x1, rect_y1), 
                    radius=17, # Reduced radius for less roundness
                    fill=GLASS_COLOR
                )
            except AttributeError:
                draw_overlay.rectangle(
                    (rect_x0, rect_y0, rect_x1, rect_y1), 
                    fill=GLASS_COLOR
                )
            # --- End Glassy Background ---

            img = Image.alpha_composite(img, overlay)
            draw = ImageDraw.Draw(img)
            
            # Removed shadow drawing loop
            
            draw.multiline_text((x, y), wrapped_text, font=font, fill=TEXT_COLOR, align="center")

            if output_path.lower().endswith(('.jpg', '.jpeg')):
                img = img.convert("RGB")

            img.save(output_path)
            print(f"✅ Social card saved to: {output_path}")

    except FileNotFoundError:
        print(f"❌ Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"❌ An error occurred during image generation: {e}")

def update_post_file(post_path: str, social_image_url: str):
    """Updates or adds the image field in the post's front matter."""
    with open(post_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        
        new_image_line = f"image: {social_image_url}"

        # Check if the correct social_image field already exists
        if new_image_line in content:
            print("✅ Post already contains the correct social_image field.")
            return

        # Try to replace an existing 'image:' field
        image_pattern = re.compile(r"^image:.*$", re.MULTILINE)
        new_content, num_replacements = image_pattern.subn(new_image_line, content, count=1)

        if num_replacements > 0:
            print(f"✅ Updated social image to: {social_image_url}")
        else:
            # If 'image:' field doesn't exist, add it to the front matter
            end_fm_match = re.search(r'^---\s*$', content, re.MULTILINE)
            if not end_fm_match:
                print("❌ Could not find the end of the front matter.")
                return
            
            insertion_point = end_fm_match.start()
            prefix = content[:insertion_point]
            field_to_add = f"{new_image_line}\n"
            
            if not prefix.endswith('\n'):
                field_to_add = '\n' + field_to_add

            new_content = prefix + field_to_add + content[insertion_point:]
            print(f"✅ Added social image: {social_image_url}")

        f.seek(0)
        f.write(new_content)
        f.truncate()

def main():
    """Main function to run the script."""
    print("--- Starting Social Card Generator ---")
    
    latest_post_path = find_latest_post()
    if not latest_post_path:
        print("❌ No posts found in `_posts` directory.")
        return

    print(f"📄 Found latest post: {os.path.basename(latest_post_path)}")
    
    post_data = parse_post(latest_post_path)
    if not post_data:
        print("❌ Failed to parse post front matter.")
        return

    original_image_rel_path = post_data.get('image')
    if not original_image_rel_path:
        print("❌ 'image' field not found in post front matter.")
        return
        
    excerpt = get_excerpt(post_data)
    print(f"💬 Excerpt: \"{excerpt[:80]}...\"")

    original_image_abs_path = os.path.join(PROJECT_ROOT, original_image_rel_path.lstrip('/'))

    path_parts = os.path.splitext(original_image_rel_path)
    social_image_rel_path = f"{path_parts[0]}.social.media{path_parts[1]}"
    social_image_abs_path = os.path.join(PROJECT_ROOT, social_image_rel_path.lstrip('/'))

    generate_social_card(original_image_abs_path, social_image_abs_path, excerpt)
    update_post_file(latest_post_path, social_image_rel_path)
    
    print("--- Script finished ---")

if __name__ == "__main__":
    main()