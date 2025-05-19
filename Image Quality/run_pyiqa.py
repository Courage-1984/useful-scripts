import os
import subprocess
import sys
from typing import List, Optional
from pathlib import Path
import csv

class PyIQAToolbox:
    def __init__(self):
        self.check_pyiqa_installation()

    def check_pyiqa_installation(self):
        """Check if pyiqa is installed."""
        try:
            subprocess.run(['pyiqa', '-h'], capture_output=True)
        except FileNotFoundError:
            print("pyiqa is not installed. Please install it first.")
            print("You can install it using: pip install pyiqa")
            input("Press Enter to continue...")
            # sys.exit(1)

    def validate_path(self, path: str, must_exist: bool = True) -> bool:
        """Validate if a path exists and is accessible."""
        path_obj = Path(path)
        if must_exist and not path_obj.exists():
            print(f"Error: Path '{path}' does not exist.")
            return False
        return True

    def validate_device(self, device: str) -> bool:
        """Validate the device input."""
        if device.lower() not in ['cuda', 'cpu']:
            print("Error: Device must be either 'cuda' or 'cpu'.")
            return False
        return True

    def display_menu(self):
        """Display the main menu."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("PyIQA Toolbox")
        print("1. List available metrics")
        print("2. Run a single metric on a single image")
        print("3. Run multiple metrics on a single image")
        print("4. Run a single metric on a directory")
        print("5. Run multiple metrics on a directory")
        print("6. Compare two images using FR metrics")
        print("7. Compare two directories using FR metrics")
        print("8. Compare upscaled image with original using NR metrics")
        print("9. Batch compare upscaled images")
        print("10. Compare upscaling methods")
        print("11. Compare multiple upscaling models")
        print("12. Run FID metric")
        print("13. Generate quality map")
        print("14. Run metrics on video")
        print("15. Save results to a file")
        print("16. Exit")
        print()
        print("Enter 'info X' to see description for option X (e.g., 'info 1')")
        print()

    def run_command(self, command: List[str], capture_output: bool = False) -> Optional[str]:
        """Run a shell command and handle its output."""
        try:
            result = subprocess.run(command, capture_output=capture_output, text=True, check=True)
            return result.stdout if capture_output else None
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {' '.join(command)}")
            print(f"Error message: {e.stderr}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    def list_metrics(self):
        """List all available metrics."""
        print()
        self.run_command(['pyiqa', '-ls'])
        input("\nPress Enter to continue...")

    def run_single_metric_single_image(self):
        """Run a single metric on a single image."""
        metric = input("Enter the metric name: ")
        image_path = input("Enter the path to the image: ")
        if not self.validate_path(image_path):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print()
        self.run_command(['pyiqa', metric, '-t', image_path, '--device', device, '--verbose'])
        input("\nPress Enter to continue...")

    def run_multiple_metrics_single_image(self):
        """Run multiple metrics on a single image."""
        metrics = input("Enter metric names separated by spaces: ").split()
        image_path = input("Enter the path to the image: ")
        if not self.validate_path(image_path):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print()
        self.run_command(['pyiqa'] + metrics + ['-t', image_path, '--device', device, '--verbose'])
        input("\nPress Enter to continue...")

    def run_single_metric_directory(self):
        """Run a single metric on a directory."""
        metric = input("Enter the metric name: ")
        dir_path = input("Enter the path to the directory: ")
        if not self.validate_path(dir_path):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print()
        self.run_command(['pyiqa', metric, '-t', dir_path, '--device', device, '--verbose'])
        input("\nPress Enter to continue...")

    def run_multiple_metrics_directory(self):
        """Run multiple metrics on a directory."""
        metrics = input("Enter metric names separated by spaces: ").split()
        dir_path = input("Enter the path to the directory: ")
        if not self.validate_path(dir_path):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print()
        self.run_command(['pyiqa'] + metrics + ['-t', dir_path, '--device', device, '--verbose'])
        input("\nPress Enter to continue...")

    def compare_two_images(self):
        """Compare two images using FR metrics."""
        metric = input("Enter the FR metric name: ")
        test_image = input("Enter the path to the test image: ")
        ref_image = input("Enter the path to the reference image: ")
        
        if not all(self.validate_path(p) for p in [test_image, ref_image]):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print()
        self.run_command(['pyiqa', metric, '-t', test_image, '-r', ref_image, '--device', device, '--verbose'])
        input("\nPress Enter to continue...")

    def compare_two_directories(self):
        """Compare two directories using FR metrics."""
        metric = input("Enter the FR metric name: ")
        test_dir = input("Enter the path to the test directory: ")
        ref_dir = input("Enter the path to the reference directory: ")
        
        if not all(self.validate_path(p) for p in [test_dir, ref_dir]):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print()
        self.run_command(['pyiqa', metric, '-t', test_dir, '-r', ref_dir, '--device', device, '--verbose'])
        input("\nPress Enter to continue...")

    def compare_upscaled(self):
        """Compare upscaled image with original using NR metrics."""
        metrics = input("Enter NR metric names separated by spaces: ").split()
        original_image = input("Enter the path to the original low-quality image: ")
        upscaled_image = input("Enter the path to the upscaled image: ")
        
        if not all(self.validate_path(p) for p in [original_image, upscaled_image]):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print("\nResults for original image:")
        self.run_command(['pyiqa'] + metrics + ['-t', original_image, '--device', device, '--verbose'])
        print("\nResults for upscaled image:")
        self.run_command(['pyiqa'] + metrics + ['-t', upscaled_image, '--device', device, '--verbose'])
        input("\nPress Enter to continue...")

    def batch_compare_upscaled(self):
        """Batch compare upscaled images."""
        metrics = input("Enter NR metric names separated by spaces: ").split()
        original_dir = input("Enter the path to the directory with original images: ")
        upscaled_dir = input("Enter the path to the directory with upscaled images: ")
        output_file = input("Enter the output file name for results: ")
        
        if not all(self.validate_path(p) for p in [original_dir, upscaled_dir]):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print("\nProcessing...")
        try:
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Original Score', 'Upscaled Score'])
                
                for filename in os.listdir(original_dir):
                    original_path = os.path.join(original_dir, filename)
                    upscaled_path = os.path.join(upscaled_dir, filename)
                    
                    if os.path.exists(upscaled_path):
                        original_score = self.run_command(['pyiqa'] + metrics + ['-t', original_path, '--device', device], capture_output=True)
                        upscaled_score = self.run_command(['pyiqa'] + metrics + ['-t', upscaled_path, '--device', device], capture_output=True)
                        writer.writerow([filename, original_score.strip(), upscaled_score.strip()])
            
            print(f"Results saved to {output_file}")
        except Exception as e:
            print(f"Error processing files: {str(e)}")
        
        input("\nPress Enter to continue...")

    def compare_upscaling_methods(self):
        """Compare upscaling methods."""
        metrics = input("Enter metric names separated by spaces: ").split()
        original_image = input("Enter the path to the original image: ")
        upscaled_image1 = input("Enter the path to the first upscaled image: ")
        upscaled_image2 = input("Enter the path to the second upscaled image: ")
        
        if not all(self.validate_path(p) for p in [original_image, upscaled_image1, upscaled_image2]):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print("\nResults for original image:")
        self.run_command(['pyiqa'] + metrics + ['-t', original_image, '--device', device, '--verbose'])
        print("\nResults for first upscaled image:")
        self.run_command(['pyiqa'] + metrics + ['-t', upscaled_image1, '--device', device, '--verbose'])
        print("\nResults for second upscaled image:")
        self.run_command(['pyiqa'] + metrics + ['-t', upscaled_image2, '--device', device, '--verbose'])
        input("\nPress Enter to continue...")

    def compare_multiple_upscaling_models(self):
        """Compare multiple upscaling models."""
        metrics = input("Enter metric names separated by spaces: ").split()
        original_image = input("Enter the path to the original image: ")
        upscaled_dir = input("Enter the path to the directory containing upscaled images: ")
        output_file = input("Enter the output file name for results (e.g., results.csv): ")
        
        if not all(self.validate_path(p) for p in [original_image, upscaled_dir]):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print("\nProcessing...")
        try:
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Model', 'Score'])
                
                # Original image score
                original_score = self.run_command(['pyiqa'] + metrics + ['-t', original_image, '--device', device], capture_output=True)
                writer.writerow(['Original', original_score.strip()])
                
                # Upscaled images scores
                for filename in os.listdir(upscaled_dir):
                    upscaled_path = os.path.join(upscaled_dir, filename)
                    score = self.run_command(['pyiqa'] + metrics + ['-t', upscaled_path, '--device', device], capture_output=True)
                    writer.writerow([filename, score.strip()])
            
            print(f"Results saved to {output_file}")
            with open(output_file, 'r') as f:
                print(f.read())
        except Exception as e:
            print(f"Error processing files: {str(e)}")
        
        input("\nPress Enter to continue...")

    def run_fid_metric(self):
        """Run FID metric."""
        test_dir = input("Enter the path to the test directory: ")
        ref_dir = input("Enter the path to the reference directory (or dataset name): ")
        dataset_res = input("Enter dataset resolution (e.g., 1024, optional): ")
        dataset_split = input("Enter dataset split (e.g., trainval70k, optional): ")
        
        if not self.validate_path(test_dir):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        command = ['pyiqa', 'fid', '-t', test_dir, '-r', ref_dir, '--device', device, '--verbose']
        if dataset_res:
            command.extend(['--dataset_res', dataset_res])
        if dataset_split:
            command.extend(['--dataset_split', dataset_split])
        
        print()
        self.run_command(command)
        input("\nPress Enter to continue...")

    def generate_quality_map(self):
        """Generate quality map."""
        metric = input("Enter the metric name for quality map generation: ")
        image_path = input("Enter the path to the image: ")
        output_path = input("Enter the path for the output quality map: ")
        
        if not self.validate_path(image_path):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print()
        self.run_command(['pyiqa', metric, '-t', image_path, '--device', device, '--save_map', '--save_dir', output_path, '--verbose'])
        input("\nPress Enter to continue...")

    def run_metrics_on_video(self):
        """Run metrics on video."""
        metric = input("Enter the metric name: ")
        video_path = input("Enter the path to the video file: ")
        output_file = input("Enter the output file name for results: ")
        
        if not self.validate_path(video_path):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print("\nProcessing video...")
        try:
            result = self.run_command(['pyiqa', metric, '-t', video_path, '--device', device, '--verbose'], capture_output=True)
            if result:
                with open(output_file, 'w') as f:
                    f.write(result)
                print(f"Results saved to {output_file}")
        except Exception as e:
            print(f"Error processing video: {str(e)}")
        
        input("\nPress Enter to continue...")

    def save_results(self):
        """Save results to a file."""
        metrics = input("Enter metric names separated by spaces: ").split()
        dir_path = input("Enter the path to the directory: ")
        output_file = input("Enter the output file name: ")
        
        if not self.validate_path(dir_path):
            input("\nPress Enter to continue...")
            return
            
        device = input("Enter device (cuda or cpu, default is cuda): ") or "cuda"
        if not self.validate_device(device):
            input("\nPress Enter to continue...")
            return
        
        print()
        try:
            result = self.run_command(['pyiqa'] + metrics + ['-t', dir_path, '--device', device, '--verbose'], capture_output=True)
            if result:
                with open(output_file, 'w') as f:
                    f.write(result)
                print(f"Results saved to {output_file}")
        except Exception as e:
            print(f"Error saving results: {str(e)}")
        
        input("\nPress Enter to continue...")

    def handle_info_command(self, option: str):
        """Handle the info command by calling show_info.py."""
        self.run_command(['python', 'show_info.py', option])
        input("\nPress Enter to continue...")

    def main_loop(self):
        """Main program loop."""
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-16) or info command: ").strip()

            if choice.lower().startswith('info '):
                self.handle_info_command(choice.split()[1])
                continue

            if choice == '16':
                break

            # Map choices to methods
            actions = {
                '1': self.list_metrics,
                '2': self.run_single_metric_single_image,
                '3': self.run_multiple_metrics_single_image,
                '4': self.run_single_metric_directory,
                '5': self.run_multiple_metrics_directory,
                '6': self.compare_two_images,
                '7': self.compare_two_directories,
                '8': self.compare_upscaled,
                '9': self.batch_compare_upscaled,
                '10': self.compare_upscaling_methods,
                '11': self.compare_multiple_upscaling_models,
                '12': self.run_fid_metric,
                '13': self.generate_quality_map,
                '14': self.run_metrics_on_video,
                '15': self.save_results
            }

            if choice in actions:
                actions[choice]()
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    toolbox = PyIQAToolbox()
    toolbox.main_loop()
