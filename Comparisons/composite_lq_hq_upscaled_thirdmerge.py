import os
from PIL import Image, ImageDraw, ImageFont

# Define input and output directories
lq_dir = "./og/lq/"
hq_dir = "./og/hq/"
upscaled_dir = "./up/UP/"
output_dir = "./new/up_hq_lq_composites/"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define text labels and color
lq_label = "LQ"
hq_label = "HQ"
upscaled_label = "Up"
label_color = (255, 255, 255)  # White
stroke_color = (0, 0, 0)  # Black
stroke_width = 1

# Try to load a font, use default if not found
try:
    # Adjust font path and size as needed
    font_size = 15  # Decreased font size
    font = ImageFont.truetype("arial.ttf", font_size)
except IOError:
    font = ImageFont.load_default()
    print("Warning: arial.ttf not found. Using default PIL font.")


# Function to draw text with stroke
def draw_text_with_stroke(
    draw, position, text, font, text_color, stroke_color, stroke_width
):
    x, y = position
    # Draw stroke
    for dx, dy in [
        (sw, sh)
        for sw in range(-stroke_width, stroke_width + 1)
        for sh in range(-stroke_width, stroke_width + 1)
        if sw != 0 or sh != 0
    ]:
        draw.text((x + dx, y + dy), text, fill=stroke_color, font=font)
    # Draw main text
    draw.text(position, text, fill=text_color, font=font)


# Iterate through LQ images
for filename in os.listdir(lq_dir):
    lq_path = os.path.join(lq_dir, filename)
    hq_path = os.path.join(hq_dir, filename)  # Assume corresponding filename in HQ dir
    upscaled_path = os.path.join(
        upscaled_dir, filename
    )  # Assume corresponding filename in upscaled dir
    output_path = os.path.join(output_dir, filename)

    # Check if corresponding HQ and upscaled files exist
    if not os.path.exists(hq_path):
        print(f"Warning: Corresponding HQ file not found for {filename}. Skipping.")
        continue
    if not os.path.exists(upscaled_path):
        print(
            f"Warning: Corresponding upscaled file not found for {filename}. Skipping."
        )
        continue

    try:
        # Open images
        lq_img = Image.open(lq_path)
        hq_img = Image.open(hq_path)
        upscaled_img = Image.open(upscaled_path)

        # Get dimensions
        lq_width, lq_height = lq_img.size
        hq_width, hq_height = hq_img.size
        upscaled_width, upscaled_height = upscaled_img.size

        # Define target height (LQ height)
        target_height = lq_height

        # Resize LQ image to match target height (already is, but for consistency)
        # This step is mostly for consistency if target_height was different
        if lq_height != target_height:
            # This part might not be strictly necessary if target_height is always lq_height
            aspect_ratio = lq_width / lq_height
            new_lq_width = int(target_height * aspect_ratio)
            lq_img_resized = lq_img.resize(
                (new_lq_width, target_height), Image.Resampling.LANCZOS
            )
        else:
            lq_img_resized = lq_img

        # Resize HQ image to match target height while maintaining aspect ratio
        if hq_height != target_height:
            aspect_ratio = hq_width / hq_height
            new_hq_width = int(target_height * aspect_ratio)
            hq_img_resized = hq_img.resize(
                (new_hq_width, target_height), Image.Resampling.LANCZOS
            )
        else:
            hq_img_resized = hq_img

        # Resize upscaled image to match target height while maintaining aspect ratio
        if upscaled_height != target_height:
            aspect_ratio = upscaled_width / upscaled_height
            new_upscaled_width = int(target_height * aspect_ratio)
            upscaled_img_resized = upscaled_img.resize(
                (new_upscaled_width, target_height), Image.Resampling.LANCZOS
            )
        else:
            upscaled_img_resized = upscaled_img

        # Get dimensions of resized images
        resized_lq_width, resized_lq_height = lq_img_resized.size
        resized_hq_width, resized_hq_height = hq_img_resized.size
        resized_upscaled_width, resized_upscaled_height = upscaled_img_resized.size

        # Define strip width (one-third of resized input width)
        strip_lq_width = resized_lq_width // 3
        strip_hq_width = resized_hq_width // 3
        strip_upscaled_width = resized_upscaled_width // 3

        # Clip vertical strips
        # LQ strip from the left third
        lq_strip = lq_img_resized.crop((0, 0, strip_lq_width, target_height))
        # HQ strip from the middle third
        hq_strip = hq_img_resized.crop(
            (strip_hq_width, 0, strip_hq_width * 2, target_height)
        )
        # Upscaled strip from the right third
        upscaled_strip = upscaled_img_resized.crop(
            (
                resized_upscaled_width - strip_upscaled_width,
                0,
                resized_upscaled_width,
                target_height,
            )
        )

        # Define line width and create black and white lines
        line_width = 1
        black_line = Image.new("RGB", (line_width, target_height), (0, 0, 0))
        white_line = Image.new("RGB", (line_width, target_height), (255, 255, 255))

        # Calculate composite dimensions (sum of strip widths + line widths)
        composite_width = (
            strip_lq_width
            + line_width
            + line_width
            + strip_hq_width
            + line_width
            + line_width
            + strip_upscaled_width
        )
        composite_height = target_height  # Use target height for composite

        # Create new composite image (using white background)
        composite_img = Image.new(
            "RGB", (composite_width, composite_height), (255, 255, 255)
        )

        # Paste LQ, HQ, and upscaled strips with lines in between
        composite_img.paste(lq_strip, (0, 0))
        composite_img.paste(black_line, (strip_lq_width, 0))
        composite_img.paste(white_line, (strip_lq_width + line_width, 0))
        composite_img.paste(hq_strip, (strip_lq_width + line_width + line_width, 0))
        composite_img.paste(
            black_line, (strip_lq_width + line_width + line_width + strip_hq_width, 0)
        )
        composite_img.paste(
            white_line,
            (strip_lq_width + line_width + line_width + strip_hq_width + line_width, 0),
        )
        composite_img.paste(
            upscaled_strip,
            (
                strip_lq_width
                + line_width
                + line_width
                + strip_hq_width
                + line_width
                + line_width,
                0,
            ),
        )  # Paste upscaled strip after HQ strip

        # Add text labels with stroke
        draw = ImageDraw.Draw(composite_img)
        text_padding = 5  # Padding from the top and left edges of the strip

        # Position for LQ label
        lq_label_position = (text_padding, text_padding)
        draw_text_with_stroke(
            draw,
            lq_label_position,
            lq_label,
            font,
            label_color,
            stroke_color,
            stroke_width,
        )

        # Position for HQ label (after LQ strip and first set of lines)
        hq_label_position = (
            strip_lq_width + line_width + line_width + text_padding,
            text_padding,
        )
        draw_text_with_stroke(
            draw,
            hq_label_position,
            hq_label,
            font,
            label_color,
            stroke_color,
            stroke_width,
        )

        # Position for Upscaled label (after LQ strip, lines, and HQ strip)
        upscaled_label_position = (
            strip_lq_width
            + line_width
            + line_width
            + strip_hq_width
            + line_width
            + line_width
            + text_padding,
            text_padding,
        )
        draw_text_with_stroke(
            draw,
            upscaled_label_position,
            upscaled_label,
            font,
            label_color,
            stroke_color,
            stroke_width,
        )

        # Save the composite image
        composite_img.save(output_path)

        print(f"Created composite image with strips, lines, and labels: {filename}")

        # Close images
        lq_img.close()
        hq_img.close()
        upscaled_img.close()
        if lq_height != target_height:
            lq_img_resized.close()
        if hq_height != target_height:
            hq_img_resized.close()
        if upscaled_height != target_height:
            upscaled_img_resized.close()
        lq_strip.close()
        hq_strip.close()
        upscaled_strip.close()
        black_line.close()
        white_line.close()
        composite_img.close()  # Close composite image after drawing

    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("Script finished.")
