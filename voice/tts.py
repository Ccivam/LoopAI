import pyttsx3
import tempfile
import os
import time

engine = pyttsx3.init()

def speak_to_file(text):
    # Create a persistent temp file
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_file.close()  # Close the file so pyttsx3 can write to it

    # Save text to audio
    engine.save_to_file(text, tmp_file.name)
    engine.runAndWait()

    # Wait a tiny bit to ensure file is fully written
    time.sleep(0.1)

    # Verify file exists
    if not os.path.exists(tmp_file.name):
        raise RuntimeError("TTS failed to generate audio file")

    return tmp_file.name
