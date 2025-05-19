import os
import shutil
import subprocess
import time
from datetime import datetime
import sys

# Configuration
SEVEN_ZIP_PATH = r"C:/Program Files/7-Zip/7z.exe"
SOURCE_DIR = r"F:/FMHY Base64 Libraries/Hellenistic Theism/test"  # Replace with your directory path


def get_directory_size(path):
    """Calculate total size of a directory in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def get_free_space(directory):
    """Get free space of the drive containing the directory."""
    if sys.platform.startswith("win"):
        free_bytes = shutil.disk_usage(directory).free
        return free_bytes
    return 0


def verify_zip(zip_path, original_folder):
    """Verify the ZIP file integrity and contents."""
    print(f"\nVerifying ZIP file: {zip_path}")

    # Check existence
    if not os.path.exists(zip_path):
        raise Exception("ZIP file was not created")

    # Wait a few seconds before verification
    time.sleep(3)

    # Test ZIP integrity using 7-Zip
    test_command = [SEVEN_ZIP_PATH, "t", zip_path]
    result = subprocess.run(test_command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"ZIP integrity test failed: {result.stderr}")

    # # Compare file counts
    # original_count = sum([len(files) for _, _, files in os.walk(original_folder)])
    # list_command = [SEVEN_ZIP_PATH, 'l', zip_path]
    # result = subprocess.run(list_command, capture_output=True, text=True)
    # # Basic file count from 7z listing (might need adjustment based on output format)
    # zip_count = result.stdout.count('\n') - 20  # Approximate adjustment for header/footer lines

    # if original_count != zip_count:
    #     raise Exception(f"File count mismatch: Original={original_count}, ZIP={zip_count}")

    print("Verification completed successfully")
    return True


def process_folder(source_dir, folder_path):
    """Process a single folder: zip, verify, and delete."""
    folder_name = os.path.basename(folder_path)
    zip_path = os.path.join(source_dir, f"{folder_name}.zip")

    # Check available space
    required_space = get_directory_size(folder_path) * 1.2  # 20% buffer
    if get_free_space(source_dir) < required_space:
        raise Exception("Insufficient disk space for zip operation")

    print(f"\nProcessing folder: {folder_name}")
    print(f"Folder size: {get_directory_size(folder_path) / (1024*1024):.2f} MB")

    # Create ZIP file
    start_time = time.time()
    zip_command = [SEVEN_ZIP_PATH, "a", "-tzip", zip_path, folder_path]
    process = subprocess.Popen(
        zip_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())

    if process.returncode != 0:
        raise Exception("ZIP creation failed")

    # Verify the ZIP file
    if verify_zip(zip_path, folder_path):
        # Delete original folder
        shutil.rmtree(folder_path)
        print(f"Deleted original folder: {folder_name}")

    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")


def main(source_dir):
    print(f"Starting folder processing at {datetime.now()}")
    print(f"Source directory: {source_dir}")

    # Verify 7-Zip exists
    if not os.path.exists(SEVEN_ZIP_PATH):
        print(f"Error: 7-Zip not found at {SEVEN_ZIP_PATH}")
        input("Press Enter to exit...")
        return

    # Verify source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory not found at {source_dir}")
        input("Press Enter to exit...")
        return

    # Get list of folders
    folders = [
        f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))
    ]

    if not folders:
        print("No folders found to process")
        input("Press Enter to exit...")
        return

    print(f"Found {len(folders)} folders to process")

    try:
        for folder in folders:
            folder_path = os.path.join(source_dir, folder)
            try:
                process_folder(source_dir, folder_path)
            except Exception as e:
                print(f"\nError processing folder {folder}: {str(e)}")
                choice = input(
                    "\nOptions:\n1. Skip and continue\n2. Retry\n3. Exit\nEnter choice (1-3): "
                )
                if choice == "1":
                    continue
                elif choice == "2":
                    process_folder(source_dir, folder_path)
                else:
                    raise Exception("User chose to exit")

        print("\nAll folders processed successfully!")
    except Exception as e:
        print(f"\nScript terminated: {str(e)}")
    finally:
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python zipAllandDelete.py <directory>")
        sys.exit(1)
    else:
        source_directory = sys.argv[1]
        main(source_directory)
