import os
import sys
import argparse
from PIL import Image

def compile_images_to_pdf(folder_path, output_pdf=None, title=None):
    folder = os.path.abspath(folder_path)
    if not os.path.exists(folder):
        print(f"Error: Folder does not exist: {folder}")
        sys.exit(1)
        
    valid_exts = ('.jpg', '.jpeg', '.png')
    all_files = sorted([f for f in os.listdir(folder) if f.lower().endswith(valid_exts) and not f.startswith(('test_', 'crop_', 'debug_'))])
    
    # Priority sorting: 00_封面 first, numbered 01..15, then 99_封底 last
    def sort_key(name):
        lower = name.lower()
        if "cover_front" in lower or lower.startswith("00_"):
            return (0, 0)
        elif "cover_back" in lower or lower.startswith("99_"):
            return (2, 999)
        else:
            try:
                prefix = int(name.split("_")[0])
                return (1, prefix)
            except ValueError:
                return (1, 500)
                
    sorted_files = sorted(all_files, key=sort_key)
    if not sorted_files:
        print("Error: No images found in folder to compile.")
        sys.exit(1)
        
    print(f"Compiling {len(sorted_files)} images into PDF:")
    for sf in sorted_files:
        print(f"  - {sf}")
        
    images = []
    for sf in sorted_files:
        p = os.path.join(folder, sf)
        img = Image.open(p).convert('RGB')
        images.append(img)
        
    if not output_pdf:
        folder_name = os.path.basename(folder)
        pdf_name = f"{folder_name}_漫畫電子書.pdf"
        if title:
            pdf_name = f"{folder_name}_{title}_漫畫電子書.pdf"
        output_pdf = os.path.join(folder, pdf_name)
        
    # Save as high-quality PDF
    images[0].save(
        output_pdf,
        save_all=True,
        append_images=images[1:],
        resolution=150.0,
        quality=95
    )
    size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
    print(f"\n[Success] Tablet-ready manga PDF generated: {output_pdf} ({size_mb:.2f} MB)")
    return output_pdf

def main():
    parser = argparse.ArgumentParser(description="Compile sorted manga pages into a tablet-ready PDF.")
    parser.add_argument("--folder", required=True, help="Directory containing the manga images.")
    parser.add_argument("--output", default=None, help="Output PDF file path (optional).")
    parser.add_argument("--title", default=None, help="Chapter title to include in PDF filename.")
    args = parser.parse_args()
    
    compile_images_to_pdf(args.folder, args.output, args.title)

if __name__ == "__main__":
    main()
