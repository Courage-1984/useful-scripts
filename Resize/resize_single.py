import os
from PIL import Image
import shutil  # Import the shutil module for copying files


def resize_single_image(
    image_path,
    output_dir,
    max_width=1920,
    max_height=1080,
):
    """
    Resizes a single image if it exceeds the maximum dimensions, maintaining the aspect ratio.
    Copies the image to the output directory if no resizing is needed.
    """
    try:
        img = Image.open(image_path)
        width, height = img.size

        # Condition for resizing: image exceeds the target resolution
        if width > max_width or height > max_height:
            print(f"Resizing image: {os.path.basename(image_path)}")

            # Calculate the scaling factor
            width_scale = max_width / width
            height_scale = max_height / height
            scale = min(width_scale, height_scale)

            # Calculate new dimensions
            new_width = int(width * scale)
            new_height = int(height * scale)

            # Resize image
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save resized image
            output_path = os.path.join(output_dir, os.path.basename(image_path))

            try:
                img_resized.save(output_path, quality=95)  # Added quality for JPEGs
            except IOError:
                # If saving with original format fails, try PNG
                print(
                    f"Could not save {os.path.basename(image_path)} in original format. Saving as PNG."
                )
                output_path = os.path.join(
                    output_dir,
                    os.path.splitext(os.path.basename(image_path))[0] + ".png",
                )
                img_resized.save(output_path, format="PNG")

            print(f"Saved resized image: {os.path.basename(output_path)}")
        else:
            print(
                f"Image does not require resizing: {os.path.basename(image_path)}. Copying original."
            )
            # Copy the original file if no resizing is needed
            try:
                output_path = os.path.join(output_dir, os.path.basename(image_path))
                shutil.copy(image_path, output_path)
                print(f"Copied original image: {os.path.basename(image_path)}")
            except Exception as copy_e:
                print(f"Error copying file {os.path.basename(image_path)}: {copy_e}")

    except FileNotFoundError:
        print(f"Error: Image file not found: {os.path.basename(image_path)}")
    except Exception as e:
        print(f"Error processing image {os.path.basename(image_path)}: {e}")


# --- Configuration ---
# *** IMPORTANT: Replace these paths with your actual directory paths ***
input_dir = "./og/single"  # Assuming you want to process images from the 'og/hq' directory
output_dir = "./new/resized_single"  # New output directory

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# --- Main processing loop ---
if __name__ == "__main__":
    # Get list of image files, assuming common image extensions
    image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")
    images = sorted(
        [
            f
            for f in os.listdir(input_dir)
            if f.lower().endswith(image_extensions)
            and os.path.isfile(os.path.join(input_dir, f))
        ]
    )

    print(f"Found {len(images)} potential images to process.")

    for img_name in images:
        image_path = os.path.join(input_dir, img_name)
        resize_single_image(image_path, output_dir)
