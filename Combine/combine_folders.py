import os
import shutil

# Define source and destination directories
sources = ["1", "2"]
subfolders = ["hq", "lq"]
dest_root = "combined"

# Create destination directories
for sub in subfolders:
    os.makedirs(os.path.join(dest_root, sub), exist_ok=True)


# Helper to avoid filename collisions
def get_unique_filename(dest_dir, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(dest_dir, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename


# Copy files, maintaining pairs
for src in sources:
    for sub in subfolders:
        src_dir = os.path.join(src, sub)
        dest_dir = os.path.join(dest_root, sub)
        for fname in os.listdir(src_dir):
            src_path = os.path.join(src_dir, fname)
            if os.path.isfile(src_path):
                # Ensure no filename collision
                unique_fname = get_unique_filename(dest_dir, fname)
                dest_path = os.path.join(dest_dir, unique_fname)
                shutil.copy2(src_path, dest_path)

print("Folders combined successfully. Check the 'combined' directory.")
