import whisper

model = whisper.load_model("base")

result = model.transcribe("new_extracted_audio.wav")

print("\nTRANSCRIBED TEXT:\n")
print(result["text"])