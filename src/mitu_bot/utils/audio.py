# /Users/chuangyf/proj/mitu_bot/src/mitu_bot/utils/audio.py
import shutil
import subprocess
import time
import wave
import math
import audioop
import collections
import pyaudio

from ..config.settings import settings

def ensure_cmd_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None

def play_wav_with_system(path: str):
    # macOS: afplay -> ffplay -> aplay
    candidates = settings.audio_players
    player = next((c for c in candidates if ensure_cmd_exists(c.split()[0])), None)
    if not player:
        print(f"[Play] No player found among: {candidates}")
        return
    try:
        args = player.split() + [path]
        subprocess.run(args, check=False)
    except Exception as e:
        print(f"[Play] exception: {e}")

def frame_bytes(sr: int, ch: int, sampwidth: int, frame_ms: int) -> int:
    samples = int(sr * (frame_ms / 1000.0))
    return samples * ch * sampwidth

def write_wav(path: str, audio_bytes: bytes):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(settings.audio_channels)
        wf.setsampwidth(settings.audio_sample_width_bytes)
        wf.setframerate(settings.audio_sample_rate)
        wf.writeframes(audio_bytes)

def _rms(data: bytes, sampwidth: int) -> int:
    return audioop.rms(data, sampwidth)

def record_until_silence() -> bytes:
    sr = settings.audio_sample_rate
    ch = settings.audio_channels
    sw = settings.audio_sample_width_bytes
    frame_ms = settings.vad_frame_ms

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16 if sw == 2 else pyaudio.paInt8,
        channels=ch,
        rate=sr,
        input=True,
        frames_per_buffer=int(sr * frame_ms / 1000),
        input_device_index=None,
    )

    fb = frame_bytes(sr, ch, sw, frame_ms)
    voiced = bytearray()
    start_time = time.time()
    last_loud_time = None

    # Calibrate noise floor
    need_frames = int(settings.vad_calibrate_sec * 1000 / frame_ms)
    print(f"\nCalibrating noise for {settings.vad_calibrate_sec:.1f} sec...")
    noise_samples = []
    for _ in range(need_frames):
        chunk = stream.read(int(sr * frame_ms / 1000), exception_on_overflow=False)
        if len(chunk) == fb:
            noise_samples.append(_rms(chunk, sw))
    noise_floor = (sum(noise_samples) / max(1, len(noise_samples))) if noise_samples else 0
    threshold = max(200, noise_floor * settings.vad_threshold_boost)
    print(f"Noise floor RMS ≈ {noise_floor:.1f}. Threshold ≈ {threshold:.1f}")
    print("Start talking (Ctrl+C to Quit)")

    prebuf = collections.deque(maxlen=int(300 / frame_ms))  # 300ms pre-roll
    speech_started = False

    try:
        while True:
            data = stream.read(int(sr * frame_ms / 1000), exception_on_overflow=False)
            if len(data) != fb:
                continue
            level = _rms(data, sw)
            is_loud = level >= threshold

            if not speech_started:
                prebuf.append(data)
                if is_loud:
                    speech_started = True
                    last_loud_time = time.time()
                    for b in prebuf:
                        voiced.extend(b)
            else:
                voiced.extend(data)
                if is_loud:
                    last_loud_time = time.time()

                if last_loud_time and (time.time() - last_loud_time) >= settings.vad_silence_timeout_sec:
                    break

            if (time.time() - start_time) > settings.vad_max_utterance_sec:
                print("Speak time limit reached.")
                break
    except KeyboardInterrupt:
        print("\nRecording stopped by user.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

    return bytes(voiced)
