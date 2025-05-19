import os
import subprocess
import sys

def check_dependencies():
    try:
        import vapoursynth
        return True
    except ImportError:
        print("\nERROR: VapourSynth is not installed or not in Python path.")
        print("Please run setup.bat first and follow the instructions.")
        return False

def show_menu():
    print("\nGetnative CLI Menu")
    print("1. Explain Getnative")
    print("2. Explain Arguments")
    print("3. Run Getnative with default settings")
    print("4. Run Getnative with custom arguments")
    print("5. Check Dependencies")
    print("6. Run with Lanczos (4 taps)")
    print("7. Run with high precision range (1-pixel steps)")
    print("8. Run with extended height range (300-1200)")
    print("9. Run with detail mask output")
    print("10. Run with interactive plot GUI")
    print("11. Run quick analysis (limited range)")
    print("12. Run with bilinear mode (ffms2)")
    print("13. Run with bicubic mode (lsmash)")
    print("14. Run with bl-bc mode (imwri)")
    print("15. Run all modes comparison (ffms2)")
    print("16. Run with custom source filter")
    print("17. Run quick bilinear analysis (imwri)")
    print("18. Run with custom aspect ratio")
    print("19. Run with linear plot scaling")
    print("20. Run with no file saving")
    print("21. Run with specific frame")
    print("22. Run with multiple output formats")
    print("23. Exit")

def explain_getnative():
    print("\nGetnative is a tool to find the native resolution(s) of upscaled material, mostly anime.")
    print("It analyzes video frames to determine the original resolution before upscaling.")
    print("\nRequired dependencies:")
    print("- VapourSynth R55+")
    print("- descale plugin")
    print("- ffms2 or lsmash or imwri plugin")
    print("- ImageMagick (if using imwri)\n")

def explain_arguments():
    print("\nArguments you can pass to Getnative:")
    print("--frame (-f): Specify a frame for analysis.")
    print("--kernel (-k): Resize kernel to be used (e.g., bicubic, bilinear, lanczos).")
    print("--bicubic-b (-b): B parameter of bicubic resize (default: 1/3).")
    print("--bicubic-c (-c): C parameter of bicubic resize (default: 1/3).")
    print("--lanczos-taps (-t): Taps parameter of lanczos resize (default: 3).")
    print("--aspect-ratio (-ar): Force aspect ratio.")
    print("--min-height (-min): Minimum height to consider (default: 500).")
    print("--max-height (-max): Maximum height to consider (default: 1000).")
    print("--output-mask (-mask): Save detail mask as png.")
    print("--plot-scaling (-ps): Scaling of the y axis (linear or log).")
    print("--plot-format (-pf): Format of the output image (e.g., svg, png).")
    print("--show-plot-gui (-pg): Show an interactive plot GUI window.")
    print("--no-save (-ns): Do not save files to disk.")
    print("--is-image (-img): Force image input.")
    print("--stepping (-steps): Change the way resolutions are handled.")
    print("--output-dir (-dir): Path of the output directory.\n")

def run_getnative_default():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file])
    else:
        print(f"\nError: File not found: {input_file}")

def run_getnative_custom():
    input_file = input("Enter the path to the input file: ")
    if not os.path.exists(input_file):
        print(f"\nError: File not found: {input_file}")
        return
        
    print("\nCommon argument combinations:")
    print("1. Basic analysis: --kernel bicubic")
    print("2. Force image input: --is-image")
    print("3. Custom height range: --min-height 500 --max-height 1000")
    print("4. Save mask: --output-mask")
    print("5. Custom bicubic parameters: --kernel bicubic --bicubic-b 0.33 --bicubic-c 0.33")
    print("6. Enter custom arguments")
    
    choice = input("\nSelect an option (1-6) or press Enter for custom arguments: ")
    
    if choice == "1":
        custom_args = "--kernel bicubic"
    elif choice == "2":
        custom_args = "--is-image"
    elif choice == "3":
        min_h = input("Enter minimum height: ")
        max_h = input("Enter maximum height: ")
        custom_args = f"--min-height {min_h} --max-height {max_h}"
    elif choice == "4":
        custom_args = "--output-mask"
    elif choice == "5":
        custom_args = "--kernel bicubic --bicubic-b 0.33 --bicubic-c 0.33"
    else:
        custom_args = input("Enter custom arguments: ")

    subprocess.run([sys.executable, "-m", "getnative", input_file] + custom_args.split())

def check_deps():
    try:
        import vapoursynth
        print("\nVapourSynth is installed correctly!")
        
        vs = vapoursynth.core
        
        plugins = []
        if hasattr(vs, 'descale'):
            plugins.append('descale')
        if hasattr(vs, 'ffms2'):
            plugins.append('ffms2')
        if hasattr(vs, 'lsmas'):
            plugins.append('lsmash')
        if hasattr(vs, 'imwri'):
            plugins.append('imwri')
            
        print(f"Installed plugins: {', '.join(plugins)}")
        
        if not plugins:
            print("\nWarning: No required plugins detected!")
            print("Please install at least one of: descale, ffms2, lsmash, imwri")
            
    except ImportError:
        print("\nVapourSynth is not installed!")
        print("Please install VapourSynth from: http://www.vapoursynth.com/")

def run_lanczos_4taps():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--kernel", "lanczos", "--lanczos-taps", "4"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_high_precision():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--stepping", "1", "--kernel", "bicubic"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_extended_range():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--min-height", "300", "--max-height", "1200"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_with_mask():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--output-mask", "--kernel", "bicubic"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_interactive():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--show-plot-gui", "--plot-scaling", "linear"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_quick_analysis():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--min-height", "700", "--max-height", "900", "--stepping", "2"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_bilinear_ffms2():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, 
                       "--mode", "bilinear", 
                       "--use", "ffms2.Source",
                       "--is-image"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_bicubic_lsmash():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, 
                       "--mode", "bicubic", 
                       "--use", "lsmas.LWLibavSource",
                       "--is-image"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_blbc_imwri():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, 
                       "--mode", "bl-bc", 
                       "--use", "imwri.Read",
                       "--is-image"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_all_modes_ffms2():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, 
                       "--mode", "all", 
                       "--use", "ffms2.Source",
                       "--is-image",
                       "--plot-format", "png,svg"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_custom_source():
    input_file = input("Enter the path to the input file: ")
    if not os.path.exists(input_file):
        print(f"\nError: File not found: {input_file}")
        return
    
    print("\nAvailable source filters:")
    print("1. ffms2.Source")
    print("2. lsmas.LWLibavSource")
    print("3. imwri.Read")
    choice = input("Select source filter (1-3): ")
    
    source_filter = {
        "1": "ffms2.Source",
        "2": "lsmas.LWLibavSource",
        "3": "imwri.Read"
    }.get(choice, "ffms2.Source")
    
    subprocess.run([sys.executable, "-m", "getnative", input_file, 
                   "--use", source_filter,
                   "--is-image"])

def run_quick_bilinear_imwri():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, 
                       "--mode", "bilinear", 
                       "--use", "imwri.Read",
                       "--is-image",
                       "--min-height", "700",
                       "--max-height", "900",
                       "--stepping", "2"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_custom_aspect_ratio():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        aspect_ratio = input("Enter the aspect ratio (e.g., 16:9): ")
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--aspect-ratio", aspect_ratio, "--is-image"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_linear_plot_scaling():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--plot-scaling", "linear", "--is-image"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_no_file_saving():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--no-save", "--is-image"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_specific_frame():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        frame_number = input("Enter the frame number to analyze: ")
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--frame", frame_number, "--is-image"])
    else:
        print(f"\nError: File not found: {input_file}")

def run_multiple_output_formats():
    input_file = input("Enter the path to the input file: ")
    if os.path.exists(input_file):
        subprocess.run([sys.executable, "-m", "getnative", input_file, "--plot-format", "png,svg", "--is-image"])
    else:
        print(f"\nError: File not found: {input_file}")

def main():
    if not check_dependencies():
        return

    while True:
        show_menu()
        choice = input("Select an option: ")
        if choice == '1':
            explain_getnative()
        elif choice == '2':
            explain_arguments()
        elif choice == '3':
            run_getnative_default()
        elif choice == '4':
            run_getnative_custom()
        elif choice == '5':
            check_deps()
        elif choice == '6':
            run_lanczos_4taps()
        elif choice == '7':
            run_high_precision()
        elif choice == '8':
            run_extended_range()
        elif choice == '9':
            run_with_mask()
        elif choice == '10':
            run_interactive()
        elif choice == '11':
            run_quick_analysis()
        elif choice == '12':
            run_bilinear_ffms2()
        elif choice == '13':
            run_bicubic_lsmash()
        elif choice == '14':
            run_blbc_imwri()
        elif choice == '15':
            run_all_modes_ffms2()
        elif choice == '16':
            run_custom_source()
        elif choice == '17':
            run_quick_bilinear_imwri()
        elif choice == '18':
            run_custom_aspect_ratio()
        elif choice == '19':
            run_linear_plot_scaling()
        elif choice == '20':
            run_no_file_saving()
        elif choice == '21':
            run_specific_frame()
        elif choice == '22':
            run_multiple_output_formats()
        elif choice == '23':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()