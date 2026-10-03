import os
import sys
import shutil
import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def process_cover(img_path, is_front=True):
    """
    Clean cover/back cover mockup backgrounds (fabric, desk textures, drop shadows)
    and center the clean A4 book page on an 896x1200 pure white canvas.
    """
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape
    
    if is_front:
        # Front cover book bounds: approx (57..63, 40..44, 843..848, 1155..1159)
        # Inset slightly by 3-5px to guarantee no drop shadow residue in corners
        crop = img.crop((63, 44, 843, 1155))
    else:
        # Back cover book bounds: approx (52, 36, 850, 1162)
        crop = img.crop((52, 36, 850, 1162))
        
    cw, ch = crop.size
    out = Image.new('RGB', (w, h), color=(255, 255, 255))
    tx = (w - cw) // 2
    ty = (h - ch) // 2
    out.paste(crop, (tx, ty))
    out.save(img_path, quality=95)
    print(f"  [Cover Cleaned] {os.path.basename(img_path)}: crop={cw}x{ch} placed on {w}x{h} pure white canvas.")

def process_interior_page(img_path, page_num_str, font_path=r'C:\Windows\Fonts\arial.ttf'):
    """
    Clean stray AI artifacts (A4, A5, rogue numbers) outside the frame
    and draw a centered page number in the bottom margin.
    """
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    gray = np.array(img.convert('L'))
    h, w, _ = arr.shape
    draw = ImageDraw.Draw(img)
    
    # 1. Detect bottom panel border line
    horiz_borders = []
    for y in range(1050, 1180):
        if np.mean(gray[y, 250:650]) < 60:
            horiz_borders.append(y)
    bot_y = max(horiz_borders) if horiz_borders else 1140
    
    # 2. Erase stray corner marks outside the frame (below bot_y)
    # Bottom-left stray (like '21'): x in [60, 150], y > bot_y + 3
    # Check if there is isolated dark text in BL margin
    bl_crop = gray[bot_y + 3:h, 40:160]
    if np.sum(bl_crop < 180) > 0 and np.sum(bl_crop < 180) < 500:
        draw.rectangle([40, bot_y + 2, 160, h], fill=(255, 255, 255))
        print(f"  [Stray Erased] BL margin cleaned for {os.path.basename(img_path)}")
        
    # Bottom-right stray (like 'A4', 'A5'): x in [760, 860], y > bot_y + 3
    br_crop = gray[bot_y + 3:h, 750:870]
    if np.sum(br_crop < 180) > 0 and np.sum(br_crop < 180) < 500:
        draw.rectangle([750, bot_y + 2, 870, h], fill=(255, 255, 255))
        print(f"  [Stray Erased] BR margin cleaned for {os.path.basename(img_path)}")
        
    # 3. Draw standard centered page number
    try:
        font = ImageFont.truetype(font_path, 24)
    except Exception:
        font = ImageFont.load_default()
        
    bbox = draw.textbbox((0, 0), str(page_num_str), font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = 1172  # optimal vertical center in the white bottom margin
    draw.text((tx, ty), str(page_num_str), fill=(60, 60, 60), font=font)
    
    img.save(img_path, quality=95)
    print(f"  [Page Number Added] Page {page_num_str} saved to {os.path.basename(img_path)}")

def main():
    parser = argparse.ArgumentParser(description="Post-process manga pages and covers.")
    parser.add_argument("--folder", required=True, help="Directory containing the manga images.")
    args = parser.parse_args()
    
    folder = os.path.abspath(args.folder)
    if not os.path.exists(folder):
        print(f"Error: Folder does not exist: {folder}")
        sys.exit(1)
        
    backup_folder = os.path.join(folder, "原始備份")
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('test_')])
    
    print(f"Starting post-processing on {len(files)} images in {folder}...")
    for f in files:
        src = os.path.join(folder, f)
        bak = os.path.join(backup_folder, f)
        if not os.path.exists(bak):
            shutil.copy2(src, bak)
            
        base_lower = f.lower()
        if "cover_front" in base_lower or f.startswith("00_"):
            process_cover(src, is_front=True)
        elif "cover_back" in base_lower or f.startswith("99_"):
            process_cover(src, is_front=False)
        else:
            # Interior page: extract page number from prefix e.g. "01_..." -> "1"
            prefix = f.split("_")[0]
            try:
                p_num = int(prefix)
                process_interior_page(src, str(p_num))
            except ValueError:
                print(f"  [Skipping page number] Could not parse number from filename: {f}")

    print("Post-processing complete! All images refined with white backgrounds and clean page numbers.")

if __name__ == "__main__":
    main()
