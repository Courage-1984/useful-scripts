import os
import argparse
import cairosvg


def convert_svg_to_png(input_dir, output_dir, width=1920):
    """Converts all SVG files in input_dir to PNG format in output_dir with a specified height."""
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: '{output_dir}'")

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".svg"):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".png"
            output_path = os.path.join(output_dir, output_filename)

            try:
                print(f"Converting '{input_path}' to '{output_path}'...")
                cairosvg.svg2png(
                    url=input_path, write_to=output_path, output_width=width
                )
                print("Conversion successful.")
            except Exception as e:
                print(f"Error converting '{input_path}': {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Bulk convert SVG files to PNG with a specified height."
    )
    parser.add_argument("input_dir", help="Directory containing SVG files.")
    parser.add_argument("output_dir", help="Directory to save converted PNG files.")
    # parser.add_argument(
    #     "--height",
    #     type=int,
    #     default=1920,
    #     help="Height of the output PNG files (default: 1080).",
    # )
    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="Width of the output PNG files (default: 1920).",
    )

    args = parser.parse_args()

    convert_svg_to_png(args.input_dir, args.output_dir, args.width)


if __name__ == "__main__":
    main()
