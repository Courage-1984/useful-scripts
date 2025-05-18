import os
from PIL import Image
import shutil  # Import the shutil module for copying files


def resize_image_pair(
    hq_image_path,
    lq_image_path,
    output_hq_dir,
    output_lq_dir,
    max_width=1920,
    max_height=1080,
):
    """
    Resizes a pair of HQ and LQ images if the HQ image exceeds the maximum dimensions,
    maintaining the aspect ratio and the 4x scale relationship. Copies the pair
    to the output directory if no resizing is needed.
    """
    try:
        hq_img = Image.open(hq_image_path)
        lq_img = Image.open(lq_image_path)

        hq_width, hq_height = hq_img.size

        # The primary condition for resizing is the HQ image exceeding the target resolution
        if hq_width > max_width or hq_height > max_height:
            print(f"Resizing image pair: {os.path.basename(hq_image_path)}")

            # Calculate the scaling factor based on the HQ image relative to the max dimensions
            width_scale = max_width / hq_width
            height_scale = max_height / hq_height
            scale = min(width_scale, height_scale)

            # Calculate new dimensions for HQ, ensuring divisibility by 4
            new_hq_width = int(hq_width * scale)
            new_hq_height = int(hq_height * scale)

            # Ensure new dimensions are divisible by 4 for LQ scale
            new_hq_width = (new_hq_width // 4) * 4
            new_hq_height = (new_hq_height // 4) * 4

            # Calculate new dimensions for LQ (must be 1/4 of new HQ dimensions)
            new_lq_width = new_hq_width // 4
            new_lq_height = new_hq_height // 4

            # Resize images
            hq_img_resized = hq_img.resize(
                (new_hq_width, new_hq_height), Image.Resampling.LANCZOS
            )
            lq_img_resized = lq_img.resize(
                (new_lq_width, new_lq_height), Image.Resampling.LANCZOS
            )  # Resize LQ based on the *new* HQ size

            # Save resized images
            hq_output_path = os.path.join(
                output_hq_dir, os.path.basename(hq_image_path)
            )
            lq_output_path = os.path.join(
                output_lq_dir, os.path.basename(lq_image_path)
            )

            try:
                hq_img_resized.save(
                    hq_output_path, quality=95
                )  # Added quality for JPEGs
                lq_img_resized.save(
                    lq_output_path, quality=95
                )  # Added quality for JPEGs
            except IOError:
                # If saving with original format fails, try PNG
                print(
                    f"Could not save {os.path.basename(hq_image_path)} in original format. Saving as PNG."
                )
                hq_output_path = os.path.join(
                    output_hq_dir,
                    os.path.splitext(os.path.basename(hq_image_path))[0] + ".png",
                )
                lq_output_path = os.path.join(
                    output_lq_dir,
                    os.path.splitext(os.path.basename(lq_image_path))[0] + ".png",
                )
                hq_img_resized.save(hq_output_path, format="PNG")
                lq_img_resized.save(lq_output_path, format="PNG")

            print(
                f"Saved resized images: {os.path.basename(hq_output_path)}, {os.path.basename(lq_output_path)}"
            )
        else:
            print(
                f"Image pair does not require resizing based on HQ dimensions: {os.path.basename(hq_image_path)}. Copying originals."
            )
            # Copy the original files if no resizing is needed
            try:
                hq_output_path = os.path.join(
                    output_hq_dir, os.path.basename(hq_image_path)
                )
                lq_output_path = os.path.join(
                    output_lq_dir, os.path.basename(lq_image_path)
                )
                shutil.copy(hq_image_path, hq_output_path)
                shutil.copy(lq_image_path, lq_output_path)
                print(
                    f"Copied original images: {os.path.basename(hq_image_path)}, {os.path.basename(lq_image_path)}"
                )
            except Exception as copy_e:
                print(
                    f"Error copying files {os.path.basename(hq_image_path)} and {os.path.basename(lq_image_path)}: {copy_e}"
                )

    except FileNotFoundError:
        print(
            f"Error: One or both image files not found for pair: {os.path.basename(hq_image_path)} and {os.path.basename(lq_image_path)}"
        )
    except Exception as e:
        print(
            f"Error processing image pair {os.path.basename(hq_image_path)} and {os.path.basename(lq_image_path)}: {e}"
        )


# --- Configuration ---
# *** IMPORTANT: Replace these paths with your actual directory paths ***
hq_input_dir = "./og/hq"
lq_input_dir = "./og/lq"
output_hq_dir = "./new/hq"
output_lq_dir = "./new/lq"

# Create output directories if they don't exist
os.makedirs(output_hq_dir, exist_ok=True)
os.makedirs(output_lq_dir, exist_ok=True)

# --- Main processing loop ---
if __name__ == "__main__":
    # Get list of image files, assuming common image extensions
    image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")
    hq_images = sorted(
        [
            f
            for f in os.listdir(hq_input_dir)
            if f.lower().endswith(image_extensions)
            and os.path.isfile(os.path.join(hq_input_dir, f))
        ]
    )

    # Assuming image file names correspond between HQ and LQ (e.g., 'image1.png' in HQ and 'image1.png' in LQ)
    # We will iterate through HQ images and find the corresponding LQ
    print(f"Found {len(hq_images)} potential HQ images to process.")

    for hq_img_name in hq_images:
        lq_img_name = hq_img_name  # Assuming LQ image has the same name as HQ
        lq_image_path = os.path.join(lq_input_dir, lq_img_name)
        hq_image_path = os.path.join(hq_input_dir, hq_img_name)

        # Check if the corresponding LQ file exists before processing the pair
        if os.path.exists(lq_image_path):
            resize_image_pair(
                hq_image_path, lq_image_path, output_hq_dir, output_lq_dir
            )
        else:
            print(
                f"Skipping HQ image {hq_img_name}: Corresponding LQ image not found at {lq_image_path}"
            )
