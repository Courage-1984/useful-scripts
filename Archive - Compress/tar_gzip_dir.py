import os
import subprocess
import sys

def create_tar_gz(directory):
    # Check if the provided directory exists
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return

    # Iterate through top-level directories first
    for top_dir in os.listdir(directory):
        top_dir_path = os.path.join(directory, top_dir)
        
        # Only process if it's a directory
        if os.path.isdir(top_dir_path):
            # Now iterate through the subdirectories we actually want to archive
            for dir_name in os.listdir(top_dir_path):
                folder_path = os.path.join(top_dir_path, dir_name)
                if os.path.isdir(folder_path):  # Ensure it's a directory
                    # Create tar and gz file paths in the same directory as the folder
                    tar_file = os.path.join(top_dir_path, f"{dir_name}.tar")
                    gz_file = f"{tar_file}.gz"

                    # Create a .tar archive using 7zip
                    tar_command = ["7z", "a", tar_file, folder_path]
                    tar_result = subprocess.run(tar_command)

                    # Check if the .tar creation was successful
                    if tar_result.returncode == 0:
                        print(f"Successfully created {tar_file}")

                        # Delete the original folder after successful .tar creation
                        subprocess.run(f"rmdir /S /Q \"{folder_path}\"", shell=True)

                        # Create a .gz archive using 7zip
                        gz_command = ["7z", "a", gz_file, tar_file]
                        gz_result = subprocess.run(gz_command)

                        # Check if the .gz creation was successful
                        if gz_result.returncode == 0:
                            print(f"Successfully created {gz_file}")

                            # Delete the .tar file after successful .gz creation
                            subprocess.run(f"del \"{tar_file}\"", shell=True)
                        else:
                            print(f"Failed to create {gz_file}")
                    else:
                        print(f"Failed to create {tar_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tar_gzip_dir.py <directory>")
    else:
        create_tar_gz(sys.argv[1])
