"""platerecognizer.py

Process images created by SecuritySpy(https://bensoftware.com/securityspy/)
and upload them to platerecognizer.com API

Attributes:
    USER: OS User running SecuritySpy
    DIRECTORIES: Paths to check for images.
    SECRET_KEY: API key
    URL: API Url
    DELETE: [description]
    if __name__: [description]
"""
import datetime
import os
import json
import sys
import signal
import logging as log
import time
import requests

# Define a list of directories to process... (i did not do
# all incase you did not want to do all cameras only some...)
USER = "MacUser"
DIRECTORIES = [
    "/Users/{USER}/SecuritySpy/Captured Files/Camera1",
    "/Users/{USER}/SecuritySpy/Captured Files/Camera2",
    "/Users/{USER}/SecuritySpy/Captured Files/Camera3",
    "/Users/{USER}/SecuritySpy/Captured Files/Camera4",
    "/Users/{USER}/SecuritySpy/Captured Files/Camera5"
    ]

# Details to login to platerecognizer api
SECRET_KEY = 'DEMOKEYDEMOKEYDEMOKEYDEMOKEYDEMOKEYDEMOKEY'
URL = 'https://api.platerecognizer.com/v1/plate-reader/'

# Set if we want to delete the image/thumb files or not.
# Keep in mind, we do not keep track of files already sent
# So if you do not delete them, it will re-process those
# images. In the future may relocate to a "done" directory
# But for now this is how it is handled.
# True/False
DELETE=False

def signal_handler(_sig, _frame):
    """
    Function: signal_handler
    Summary: Handles the SIGINT signal (Ctrl-C) by logging a message.
    Attributes: 
        @param (sig):the signal number 
        @param (frame):the interrupted stack frame
    Returns: None
    """

    log.info("Recieved CTR-C, Exiting...")
    sys.exit(0)

def process_image(file_path, camera_id, delete_image):
    """
    Function: process_image
    Summary: takes the given file and sends to API for processing
    Attributes: 
        @param (file_path):path to image
        @param (camera_id):Camera Name
        @param (delete_image):Boolean to delete the image & thumb or not
    Returns: None
    """
    file = os.path.basename(file_path)
    # If file is a image, process it
    if file.endswith(".jpg"):
        timestamp_str = file.split(" ")[0] + " " + file.split(" ")[1]
        timestamp = datetime.datetime.strptime(timestamp_str, "%m-%d-%Y %H-%M-%S")
        iso_timestamp = timestamp.isoformat()
        log.info("Processing File: %s", file_path) #

        with open(file_path, 'rb') as image_file:
            ret = requests.post(
                    URL,
                    data={
                        camera_id: f"{camera_id}",
                        regions: ['us-il'],
                        timestamp: f"{iso_timestamp}",
                        config: json.dumps({(region: "strict")})
                        },
                    files=dict(upload=image_file),
                    headers={'Authorization': f'Token {SECRET_KEY}'},
                    timeout=120
                    )

        log.info(json.dumps(ret.json(), indent=2))
        time.sleep(2)
        if delete_image:
            log.info("Deleting image: %s", file_path)
            os.remove(file_path)
    elif file.endswith(".thm"):
        if delete_image:
            log.info("Deleting image: %s", file_path)
            os.remove(file_path)

def main():
    """
    Function: main()
    Summary: This function serves as the entry point of the script.
    """

    # Remove the default handler created by basicConfig()
    log.getLogger().handlers.clear()

    # Set up logging, feel free to use what ever log
    # path you want. Just make sure the user the script
    # runs as, has access to that path.
    log.basicConfig(
        level=log.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            log.FileHandler('/tmp/platerecognizer.log')
        ]
    )

    signal.signal(signal.SIGINT, signal_handler)

    for dir_path in DIRECTORIES:
        # Pull Camera ID(name) from path.
        camera = os.path.basename(dir_path)

        # Loop through dates in camera path to find new images.
        date_path = os.listdir(dir_path)
        for final_path in date_path:

            # Loop through files and start processing them
            final_path = os.path.join(dir_path, final_path)
            log.info("Starting run for: %s", final_path)
            if os.path.isdir(final_path):
                files = os.listdir(final_path)

                # Sort the files in the directory so they are processed in order.
                files_sorted = sorted(files, key=lambda x: os.path.basename(x))

                for file in files_sorted:
                    file_path = os.path.join(final_path, file)
                    process_image(file_path, camera_id=camera, delete_image=DELETE)

if __name__ == "__main__":
    main()
