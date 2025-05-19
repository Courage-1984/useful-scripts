import os
from PIL import Image

# --- User Configuration ---
# Set this to the path of the directory containing your input images.
input_directory = "C:/Users/anon/ai/training/train/first_icons_redone/_png"
# Set this to the path where you want to save the processed images.
# The script will attempt to create this directory if it doesn't exist.
output_directory = "C:/Users/anon/ai/training/train/first_icons_redone/_png_noA"
# ------------------------


def remove_alpha_channel(input_dir, output_dir):
    """
    Removes the alpha channel from all images in a directory and saves them
    as PNG files in a different directory.

    Args:
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory to save results.
    """
    if not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        # Skip if it's a directory
        if os.path.isdir(input_path):
            continue

        try:
            with Image.open(input_path) as img:
                print(f"Processing {filename}...")
                # Check if image has an alpha channel (e.g., RGBA, LA)
                if img.mode in ("RGBA", "LA"):
                    # Convert to RGB
                    # Create a white background
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    # Paste the image onto the background
                    background.paste(
                        img, mask=img.split()[-1]
                    )  # Use alpha channel as mask
                    img = background
                    print(f"Removed alpha channel from {filename}.")
                elif img.mode != "RGB":
                    # Convert other modes like 'L' (grayscale) or 'P' (palette) to RGB
                    img = img.convert("RGB")
                    print(f"Converted {filename} to RGB.")
                else:
                    print(f"{filename} already in RGB format.")

                # Define output path (save as PNG)
                base, _ = os.path.splitext(filename)
                output_filename = f"{base}.png"
                output_path = os.path.join(output_dir, output_filename)

                # Save the processed image
                img.save(output_path, "PNG")
                print(f"Saved processed image to {output_path}")

        except FileNotFoundError:
            print(f"Error: File not found at {input_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    remove_alpha_channel(input_directory, output_directory)
    print("Processing complete.")
