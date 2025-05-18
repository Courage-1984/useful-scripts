import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import time
import atexit


def has_sound(audio_path):
    try:
        audio = AudioSegment.from_file(audio_path)
        return (
            audio.rms > 0
        )  # Check if the root mean square (RMS) of the audio is greater than 0
    except Exception as e:
        print(f"Error checking sound for {audio_path}: {str(e)}")
        return False


def move_videos_with_sound(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    def cleanup(clip):
        try:
            if clip.audio:
                clip.audio.close()
            if clip:
                clip.close()
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    atexit.register(cleanup, clip=None)

    for root, _, files in os.walk(source_folder):
        for filename in files:
            if filename.endswith((".mp4", ".avi", ".mkv", ".mov")):
                video_path = os.path.join(root, filename)
                audio_path = f"{video_path[:-4]}.mp3"  # Convert video to audio (assuming mp3 format)

                try:
                    clip = VideoFileClip(video_path)

                    # Check if the video has audio
                    if clip.audio is not None:
                        clip.audio.write_audiofile(audio_path, codec="mp3")

                        # Close video and audio files if they exist
                        if clip.audio:
                            clip.audio.close()
                        if clip:
                            clip.close()

                        if has_sound(audio_path):
                            time.sleep(
                                0.7
                            )  # Increase the sleep duration to 2 seconds or more
                            destination_path = os.path.join(
                                destination_folder, filename
                            )
                            os.rename(video_path, destination_path)
                            print(f"Moved {filename} to {destination_folder}")
                    else:
                        print(f"{filename} does not have an audio stream.")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

                # Delete temporary audio file
                if os.path.exists(audio_path):
                    os.remove(audio_path)


if __name__ == "__main__":
    source_folder = "C:/path/to/source/folder"
    destination_folder = "C:/path/to/destination/folder"

    move_videos_with_sound(source_folder, destination_folder)
