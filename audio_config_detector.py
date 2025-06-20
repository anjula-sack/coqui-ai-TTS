import librosa

# Load your audio file
audio_path = 'test_audio.wav'
y, sr = librosa.load(audio_path, sr=None)  # sr=None preserves original sample rate

# Suggested defaults for VITS model
win_length = 1024
hop_length = 256
num_mels = 80
mel_fmin = 0
mel_fmax = sr // 2  # Usually set to Nyquist frequency

# Print inferred values
print(f"Sample Rate: {sr}")
print(f"Window Length: {win_length}")
print(f"Hop Length: {hop_length}")
print(f"Num Mels: {num_mels}")
print(f"Mel Fmin: {mel_fmin}")
print(f"Mel Fmax: {mel_fmax}")

