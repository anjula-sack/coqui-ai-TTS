from pydub import AudioSegment
import os

def convert_m4a_to_wav(input_file, output_file, target_sample_rate=22050):
    # Load the .m4a file (pydub uses ffmpeg under the hood)
    print(f"Converting {input_file} to {output_file}")
    audio = AudioSegment.from_file(input_file, format="m4a")

    # Set frame rate to 22.05 kHz (downsample)
    audio = audio.set_frame_rate(target_sample_rate)

    # Export as .wav
    audio.export(output_file, format="wav")
    print(f"Converted and saved: {output_file}")

for file in os.listdir('./audios'):
    convert_m4a_to_wav(os.path.join('./audios', file), os.path.join('./audios', file + ".wav"))
