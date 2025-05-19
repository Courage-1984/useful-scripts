import os
import sys
from imagededup.methods import PHash
from imagededup.utils import plot_duplicates
from multiprocessing import freeze_support
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib

matplotlib.use('TkAgg')

def get_image_info(image_path):
    file_size = os.path.getsize(image_path) / 1024  # Size in KB
    with Image.open(image_path) as img:
        width, height = img.size
    return f"{os.path.basename(image_path)}\n{file_size:.2f} KB\n{width}x{height}"

def plot_duplicates_custom(image_dir, duplicate_map, filename):
    duplicates = duplicate_map[filename]
    num_images = len(duplicates) + 1
    
    # Close any existing figures
    plt.close('all')
    
    # Create a figure that uses the full screen
    # fig, axs = plt.subplots(2, num_images, figsize=(16, 9), 
    #                         gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.1})
    fig, axs = plt.subplots(2, num_images, figsize=(14, 6), 
                            gridspec_kw={'height_ratios': [5, 0.5]})
    
        # Maximize the figure window
    fig_manager = plt.get_current_fig_manager()
    try:
        fig_manager.window.state('zoomed')  # For Windows
    except AttributeError:
        fig_manager.window.showMaximized()  # Fallback for other systems

    # Plot original image
    original_img = Image.open(os.path.join(image_dir, filename))
    axs[0, 0].imshow(original_img)
    axs[0, 0].axis('off')
    axs[0, 0].set_title("Original", fontsize=18, pad=1)
    
    # Display image info below the original
    axs[1, 0].text(0.5, 0.5, get_image_info(os.path.join(image_dir, filename)),
                   ha='center', va='center', wrap=True, fontsize=11)
    axs[1, 0].axis('off')
    
    # Plot duplicates
    for idx, dup in enumerate(duplicates, 1):
        dup_img = Image.open(os.path.join(image_dir, dup))
        axs[0, idx].imshow(dup_img)
        axs[0, idx].axis('off')
        axs[0, idx].set_title(f"Duplicate {idx}", fontsize=18, pad=1)
        
        # Display image info below each duplicate
        axs[1, idx].text(0.5, 0.5, get_image_info(os.path.join(image_dir, dup)),
                         ha='center', va='center', wrap=True, fontsize=11)
        axs[1, idx].axis('off')
    
    # Reduce spacing between subplots
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    plt.tight_layout()
    plt.show(block=True)
    plt.close(fig)

def main():
    image_dir = sys.argv[1]
    if not os.path.isdir(image_dir):
        print(f"Error: The directory '{image_dir}' does not exist.")
        sys.exit(1)

    # Display all image information before processing
    print("\nAll images in the directory:")
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(image_dir, filename)
            print(get_image_info(file_path).replace('\n', ', '))
    
    input("\nPress Enter to continue with duplicate detection...")

    phasher = PHash()
    print("\nGenerating encodings...")
    phash_encodings = phasher.encode_images(image_dir=image_dir)
    print("Encodings generated.")
    print("Finding duplicates...")
    phash_duplicates = phasher.find_duplicates(encoding_map=phash_encodings)
    print("Duplicates found.")
    print(f"Number of images processed: {len(phash_encodings)}")
    print(f"Number of duplicate sets found: {len([v for v in phash_duplicates.values() if v])}")
    
    print("\nPlotting duplicates and displaying file info...")
    images_with_duplicates = [k for k, v in phash_duplicates.items() if v]
    if images_with_duplicates:
        for image in images_with_duplicates:
            try:
                print(f"\nDuplicates for {image}:")
                print(f"0. {get_image_info(os.path.join(image_dir, image)).replace(chr(10), ', ')}")
                for i, dup in enumerate(phash_duplicates[image], 1):
                    print(f"{i}. {get_image_info(os.path.join(image_dir, dup)).replace(chr(10), ', ')}")
                
                plot_duplicates_custom(image_dir, phash_duplicates, image)
                
                choice = input("Enter the number of the image to delete (or press Enter to skip): ")
                if choice.isdigit():
                    choice = int(choice)
                    if 0 <= choice <= len(phash_duplicates[image]):
                        file_to_delete = image if choice == 0 else phash_duplicates[image][choice-1]
                        os.remove(os.path.join(image_dir, file_to_delete))
                        print(f"Deleted: {file_to_delete}")
                    else:
                        print("Invalid choice. Skipping.")
                else:
                    print("Skipping deletion.")
            except Exception as e:
                print(f"Error processing duplicates for {image}: {str(e)}")
    else:
        print("No duplicates found to plot.")

if __name__ == '__main__':
    freeze_support()
    main()
