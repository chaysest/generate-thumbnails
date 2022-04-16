import os 
import sys
from moviepy.editor import * 
from PIL import Image
from pathlib import Path
import time

# Inspired by: https://hardweb.dev/blogs/posts/2020/steps-to-create-thumbnails-from-video-in-python-using-moviepy.html

## TODO ##
# Add commmand line functionality to choose which second to grab thumbnail from
# Check vid path extention before converting

SUPPORTED_FILE_EXT = [
                        ".webm",
                        ".mpg", 
                        ".mp2", 
                        ".mpeg", 
                        ".mpe", 
                        ".mpv", 
                        ".ogg", 
                        ".mp4", 
                        ".m4v", 
                        ".m4p", 
                        ".avi", 
                        ".wmv", 
                        ".mov", 
                        ".qt", 
                        ".flv", 
                        ".swf"]

SKIPPED_VIDEO_FILES = []

def main():
    if len(sys.argv) < 3:
        usage("general")
    if len(sys.argv)  >= 3:
        if sys.argv[1] == "-r":
            # If -r flag is used
            if len(sys.argv) >= 4:
                INPUT_DIR = sys.argv[2]
                OUTPUT_DIR = sys.argv[3]

                try:
                    FRAME = int(sys.argv[4])
                except:
                    FRAME = 1

                makeAllThumbs(INPUT_DIR, OUTPUT_DIR, FRAME)
            else: 
                usage("-r")
         
        INPUT_FILE = sys.argv[1]
        OUTPUT_DIR = sys.argv[2]
        try:
            FRAME = int(sys.argv[3])
        except:
            FRAME = 1
        start = time.time()
        makeThumb(INPUT_FILE, OUTPUT_DIR, FRAME)
        print(f"Done in {round(time.time() - start, 2)}s")
        sys.exit(0)
    else: 
        usage("single")
    

def makeThumb(vidPath, output, frame_choice=1):
    p = Path(vidPath)
    name = p.stem # Just the naming scheme of the video
    ext = p.suffix

    # Check file extension and skip if not a video
    if ext.lower() not in SUPPORTED_FILE_EXT:
        print(f"Skipping {name}{ext}")
        return False
    clip = VideoFileClip(vidPath)

    # Check that the frame at the desired time is within the duration of the video
    if not frame_choice <= clip.duration:
        print(f"Skipping {name}{ext}")
        SKIPPED_VIDEO_FILES.append([f"{name}{ext}", "Video is too short for chosen thumbnail timestamp"])
        return False

    print(f'Making thumbnail for {name}{ext}')
    FRAME_AT_SECOND = frame_choice # Change this to change the desired frame
    frame = clip.get_frame(FRAME_AT_SECOND)
    new_thumb_path = f'{output}/{name}.png'
    new_image = Image.fromarray(frame)
    new_image.save(new_thumb_path)
    clip.reader.close()
    return True


def makeAllThumbs(input, output, frame_choice):
    start = time.time()
    filesList = os.listdir(input)
    c = 0
    # Loop through all files in directory
    for file in filesList:
        if makeThumb(input+file, output, frame_choice):
            c += 1
    
    print(f"Done in {round(time.time() - start, 2)}s\nCount: {c} files created in {output}\n")

    # Print any skipped video files
    if len(SKIPPED_VIDEO_FILES) > 0:
        print("The Following Files were skipped")
        for skipped in SKIPPED_VIDEO_FILES:
            print(f"{skipped[0]} : {skipped[1]}")
    sys.exit()


def usage(choice="general"):
    msg = {
        "general": "Error: Missing arguments. \nTo make one thumbnail: python make_thumbs.py FILE DIR [n]\nTo make multiple thumbnails: python make_thumbs.py -r DIR DIR [n]",
        "single": "To make one thumbnail: python make_thumbs.py FILE DIR [n]",
        "-r": "To make multiple thumbnails: python make_thumbs.py -r DIR0 DIR1 [n]",
    }
    if choice in msg:
        print(msg[choice])
    else:
        print(msg["general"])
    sys.exit(1)
    
    

if __name__ == "__main__":
   main()