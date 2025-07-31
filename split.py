import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_audio_to_exact_segments(input_file, start_utt_id, output_dir,
                                   silence_thresh_offset=16,
                                   keep_silence=100,
                                   initial_min_silence_len=300,
                                   max_min_silence_len=1500,
                                   step=100):
    audio = AudioSegment.from_file(input_file)
    silence_thresh = audio.dBFS - silence_thresh_offset

    min_silence_len = initial_min_silence_len
    segments = []

    # Try different min_silence_len values until exactly 100 segments
    while min_silence_len <= max_min_silence_len:
        segments = split_on_silence(audio,
                                    min_silence_len=min_silence_len,
                                    silence_thresh=silence_thresh,
                                    keep_silence=keep_silence)
        if len(segments) == 100:
            break
        min_silence_len += step

    if len(segments) != 100:
        print(f"[FAILED] {input_file}: Found {len(segments)} segments (not 100) after trying all thresholds.")
        return 0

    for i, segment in enumerate(segments):
        utt_id = start_utt_id + i
        filename = f"utt{utt_id:05d}.wav"
        output_path = os.path.join(output_dir, filename)
        segment.export(output_path, format="wav")

    print(f"[SUCCESS] {input_file}: Exported 100 segments from utt{start_utt_id:05d} to utt{start_utt_id+99:05d}")
    return 100


def batch_split_all_audio(audio_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Collect audio files and sort them numerically
    audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith(".wav")])

    current_utt_id = 1301  # Starting from utt01301

    for file in audio_files:
        input_path = os.path.join(audio_dir, file)
        segments_saved = split_audio_to_exact_segments(input_path, current_utt_id, output_dir)
        if segments_saved != 100:
            print(f"Stopped processing due to failure in {file}")
            break
        current_utt_id += 100


# Run the batch processing
batch_split_all_audio("audios", "output")
