def show_info(option):
    info = {
        1: {
            "title": "List available metrics",
            "use_case": "When you want to see all the image quality metrics available in pyiqa.",
            "description": "This option provides a comprehensive list of all the metrics that can be used to evaluate image quality.",
            "note": "It is useful for users who are unfamiliar with the available metrics and want to explore their options."
        },
        2: {
            "title": "Run a single metric on a single image",
            "use_case": "When you want to evaluate the quality of a single image using one specific metric.",
            "description": "This option allows you to focus on a particular aspect of image quality by selecting a specific metric.",
            "note": "Ideal for quick assessments or when you have a specific quality concern in mind."
        },
        3: {
            "title": "Run multiple metrics on a single image",
            "use_case": "When you want to evaluate a single image using multiple quality metrics at once.",
            "description": "This option provides a broader analysis of an image's quality by applying several metrics simultaneously.",
            "note": "Useful for comprehensive quality assessments or when comparing different quality aspects."
        },
        4: {
            "title": "Run a single metric on a directory",
            "use_case": "When you want to evaluate multiple images in a directory using one specific metric.",
            "description": "This option automates the process of applying a single metric to a batch of images, saving time and effort.",
            "note": "Ideal for consistent quality checks across a dataset or collection of images."
        },
        5: {
            "title": "Run multiple metrics on a directory",
            "use_case": "When you want to evaluate multiple images in a directory using multiple quality metrics.",
            "description": "This option allows for a thorough quality analysis of a batch of images, applying several metrics to each.",
            "note": "Perfect for detailed quality reports or when assessing a large dataset."
        },
        6: {
            "title": "Compare two images using FR metrics",
            "use_case": "When you want to compare a test image against a reference image using Full-Reference metrics.",
            "description": "This option is useful for scenarios where you have a high-quality reference image and want to measure deviations.",
            "note": "Commonly used in image processing tasks where fidelity to the original is crucial."
        },
        7: {
            "title": "Compare two directories using FR metrics",
            "use_case": "When you want to compare multiple test images against their corresponding reference images.",
            "description": "This option is ideal for batch processing, allowing you to compare entire datasets of images.",
            "note": "Useful in quality assurance processes where consistency across a set of images is required."
        },
        8: {
            "title": "Compare upscaled image with original using NR metrics",
            "use_case": "When you want to evaluate if upscaling improved image quality without a high-quality reference.",
            "description": "This option is beneficial when you lack a reference image and need to assess quality improvements post-upscaling.",
            "note": "Suitable for evaluating the effectiveness of upscaling algorithms."
        },
        9: {
            "title": "Batch compare upscaled images",
            "use_case": "When you want to evaluate the quality improvement of multiple upscaled images at once.",
            "description": "This option streamlines the process of assessing a batch of upscaled images, providing a comparative analysis.",
            "note": "Ideal for projects involving large-scale image enhancement."
        },
        10: {
            "title": "Compare upscaling methods",
            "use_case": "When you want to compare the effectiveness of different upscaling methods on a single image.",
            "description": "This option allows you to directly compare the results of various upscaling techniques on the same image.",
            "note": "Useful for selecting the best upscaling method for a specific application."
        },
        11: {
            "title": "Compare multiple upscaling models",
            "use_case": "When you want to compare multiple upscaled versions of the same image produced by different models or settings.",
            "description": "This option provides insights into how different models or settings affect image quality.",
            "note": "Ideal for research and development in image processing technologies."
        },
        12: {
            "title": "Run FID metric",
            "use_case": "When you want to evaluate the quality and diversity of generated images compared to real images.",
            "description": "This option is particularly useful in generative modeling, where the goal is to produce realistic images.",
            "note": "FID (Fréchet Inception Distance) is a popular metric for assessing the performance of generative models."
        },
        13: {
            "title": "Generate quality map",
            "use_case": "When you want to visualize the quality distribution across an image.",
            "description": "This option helps in identifying areas of an image that may have quality issues.",
            "note": "Useful for detailed quality analysis and visualization."
        },
        14: {
            "title": "Run metrics on video",
            "use_case": "When you want to evaluate the quality of a video file.",
            "description": "This option extends image quality assessment to video, allowing for frame-by-frame analysis.",
            "note": "Ideal for video processing tasks where quality consistency is important."
        },
        15: {
            "title": "Save results to a file",
            "use_case": "When you want to save the quality assessment results to a file for later analysis.",
            "description": "This option is useful for documentation and reporting purposes, enabling you to keep a record of assessments.",
            "note": "Ideal for projects that require detailed quality tracking over time."
        },
        16: {
            "title": "Exit the program",
            "use_case": "When you want to terminate the program and return to the command prompt.",
            "description": "This option provides a clean exit from the program, ensuring all processes are properly closed."
        }
    }
    
    try:
        option = int(option)
        if option < 1 or option > 16:
            print("Please enter a number between 1 and 16.")
            return
            
        info_data = info.get(option)
        if info_data:
            print(f"\n{info_data['title']}")
            print("-" * len(info_data['title']))
            print(f"Use case: {info_data['use_case']}")
            print(f"Description: {info_data['description']}")
            if "note" in info_data:
                print(f"Note: {info_data['note']}")
        else:
            print("Invalid option number.")
            
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        show_info(sys.argv[1])
    else:
        print("Please provide an option number.")
