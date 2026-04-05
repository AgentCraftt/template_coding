import wave
import struct
import os
import pytest

from solution import stereo_to_mono


# Helper function to create a stereo wav file for testing
def create_stereo_wav(file_path, frames):
    with wave.open(file_path, "wb") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        wav_file.setnframes(len(frames))

        for frame in frames:
            packed_frame = struct.pack("<hh", frame[0], frame[1])
            wav_file.writeframes(packed_frame)


# Helper function to read a mono wav file and return frames
def read_mono_wav(file_path):
    with wave.open(file_path, "rb") as wav_file:
        frames = []
        while True:
            frame_data = wav_file.readframes(1)
            if not frame_data:
                break
            mono_value = struct.unpack("<h", frame_data)[0]
            frames.append(mono_value)
        return frames


def test_stereo_to_mono_conversion():
    input_wav = "test_stereo.wav"
    output_wav = "test_mono.wav"

    # Create a stereo wav file to test with
    frames = [(100, -100), (200, -200), (300, -300), (400, -400)]
    create_stereo_wav(input_wav, frames)

    # Perform the stereo to mono conversion
    stereo_to_mono(input_wav, output_wav)

    # Read in the output mono file to verify
    mono_frames = read_mono_wav(output_wav)

    # Expected mono frames by averaging the input frames
    expected_mono_frames = [(f[0] + f[1]) // 2 for f in frames]

    assert mono_frames == expected_mono_frames

    # Clean up
    os.remove(input_wav)
    os.remove(output_wav)


def test_raises_error_on_mono_input():
    input_wav = "test_mono_input.wav"
    output_wav = "should_not_create.wav"

    # Create a mono wav file
    frames = [100, 200, 300, 400]
    with wave.open(input_wav, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        wav_file.setnframes(len(frames))
        for frame in frames:
            wav_file.writeframes(struct.pack("<h", frame))

    # Try to convert it using stereo_to_mono which should raise an error
    with pytest.raises(wave.Error, match="Input file is not stereo"):
        stereo_to_mono(input_wav, output_wav)

    # Clean up
    os.remove(input_wav)
