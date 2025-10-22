import wave
import struct


def stereo_to_mono(input_wav: str, output_wav: str) -> None:
    """
    This function converts a stereo WAV file to mono.

    :param input_wav: Path to the input stereo WAV file
    :param output_wav: Path to output the mono WAV file
    :return: None
    """
    with wave.open(input_wav, "rb") as in_wave:
        params = in_wave.getparams()
        if params.nchannels != 2:
            raise wave.Error("Input file is not stereo")

        # Extract parameters
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params

        with wave.open(output_wav, "wb") as out_wave:
            # Set parameters for mono output
            out_wave.setnchannels(1)
            out_wave.setsampwidth(sampwidth)
            out_wave.setframerate(framerate)
            out_wave.setnframes(n_frames)
            out_wave.setcomptype(comptype, compname)

            # Process each frame
            for _ in range(n_frames):
                frame_data = in_wave.readframes(1)
                left, right = struct.unpack("<hh", frame_data)

                # Average the left and right channels
                mono_value = (left + right) // 2
                out_wave.writeframes(struct.pack("<h", mono_value))


# Sample usage:
# stereo_to_mono('stereo_sample.wav', 'mono_output.wav')
