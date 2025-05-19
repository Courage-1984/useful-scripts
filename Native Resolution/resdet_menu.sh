#!/bin/bash

# Function to convert Windows path to WSL path
convert_path() {
    # Print the exact conversion steps
    echo "Original path: $1" >&2
    
    # Step 1: Replace backslashes with forward slashes
    local step1=$(echo "$1" | sed -E 's/\\/\//g')
    echo "After replacing backslashes: $step1" >&2
    
    # Step 2: Get drive letter in lowercase
    local drive=$(echo "${step1:0:1}" | tr '[:upper:]' '[:lower:]')
    echo "Drive letter: $drive" >&2
    
    # Step 3: Get the rest of the path (after C:)
    local rest="${step1#*:}"
    echo "Rest of path: $rest" >&2
    
    # Step 4: Combine with /mnt/
    local final="/mnt/$drive$rest"
    echo "Final path: $final" >&2
    
    echo "$final"
}

# Function to handle path input
get_path() {
    # Read the path with quotes to preserve backslashes
    read -r -p "Enter image path (Windows or WSL path): " img_path
    # Check if path contains ':' (Windows path)
    if [[ $img_path == *":"* ]]; then
        img_path=$(convert_path "$img_path")
        echo "Debug - Final path: \"$img_path\"" >&2
    fi
    echo "\"$img_path\""
}

while true; do
    clear
    echo "===== ResDet Menu ====="
    echo "1. Basic ResDet Analysis"
    echo "2. Linear RGB Colorspace Analysis"
    echo "3. Deblocked JPEG Analysis"
    echo "4. Quick Upscale Check"
    echo "5. Exit"
    echo "===================="
    
    read -p "Choose an option (1-5): " choice

    case $choice in
        1)
            echo "Performing Basic ResDet Analysis..."
            echo "This option analyzes the image to detect if it has been upscaled, providing the most likely original resolution."
            img_path=$(get_path)
            img_path_unquoted="${img_path//\"}"
            echo "Debug - Path being passed to resdet: $img_path" >&2
            if [ -f "$img_path_unquoted" ]; then
                echo "Debug - File exists" >&2
            else
                echo "Debug - File does not exist" >&2
            fi
            resdet "$img_path_unquoted"
            ;;
        2)
            echo "Performing Linear RGB Colorspace Analysis..."
            echo "This option converts the image to a linear RGB colorspace before analysis, which can improve accuracy if the image was resized in a linear light colorspace."
            img_path=$(get_path)
            img_path_unquoted="${img_path//\"}"
            echo "Debug - Path being passed to convert: $img_path_unquoted" >&2
            if [ -f "$img_path_unquoted" ]; then
                echo "Debug - File exists" >&2
                convert "$img_path_unquoted" -colorspace RGB pfm:- | resdet -t image/x-portable-floatmap -
            else
                echo "Debug - File does not exist" >&2
                echo "Invalid image"
            fi
            ;;
        3)
            echo "Performing Deblocked JPEG Analysis..."
            echo "This option applies a deblocking filter to JPEG images to reduce compression artifacts before analysis, which can help improve detection accuracy."
            img_path=$(get_path)
            img_path_unquoted="${img_path//\"}"
            echo "Debug - Path being passed to ffmpeg: $img_path_unquoted" >&2
            
            if [ -f "$img_path_unquoted" ]; then
                echo "Debug - File exists" >&2
                # Create temporary PNG with a more unique name
                temp_file="/tmp/deblocked_$(date +%s%N).png"
                if ffmpeg -i "$img_path_unquoted" -vf pp=ha/va "$temp_file"; then
                    echo "Debug - FFmpeg conversion successful" >&2
                    resdet "$temp_file"
                    rm -f "$temp_file"
                else
                    echo "Debug - FFmpeg conversion failed" >&2
                    echo "Error: Failed to process image"
                fi
            else
                echo "Debug - File does not exist" >&2
                echo "Invalid image"
            fi
            ;;
        4)
            echo "Performing Quick Upscale Check..."
            echo "This option quickly checks if the image is upscaled, providing a simple yes or no answer."
            img_path=$(get_path)
            img_path_unquoted="${img_path//\"}"
            echo "Debug - Path being passed to resdet: $img_path" >&2
            if [ -f "$img_path_unquoted" ]; then
                echo "Debug - File exists" >&2
                if resdet -v0 "$img_path_unquoted"; then
                    echo "Image is upscaled"
                else
                    echo "Image is not upscaled"
                fi
            else
                echo "Debug - File does not exist" >&2
                echo "Invalid image"
            fi
            ;;
        5)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option"
            ;;
    esac

    echo
    read -p "Press Enter to continue..."
done