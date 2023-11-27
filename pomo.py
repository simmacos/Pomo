import time, os, contextlib
import sys
import wave
import pyaudio
from plyer import notification

audio_file_path = 'clock.wav'

if len(sys.argv) < 2:
    print("Insert minutes as argument!")
    sys.exit()

min = int(sys.argv[1])

def main(minutes):
    print("The Pomo Timer is set")

    for _ in range(minutes):
        time.sleep(2)
        print("       ||  ")

    print("      STOP")

    with ignoreStderr():
        audio_interface = pyaudio.PyAudio()

    playAudio(audio_file_path)
    notif()

def notif():
    notification.notify(
        title="Pomodoro is up",
        message="Time to stretch!",
        app_name="pomo",
        app_icon='clock.wav',
        timeout=5
    )

def playAudio(file_path):
    CHUNK = 1024

    wf = wave.open(file_path, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )

    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()

@contextlib.contextmanager
def ignoreStderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)

main(min)
