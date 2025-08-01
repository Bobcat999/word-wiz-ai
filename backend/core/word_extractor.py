#%%
import torch
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import re


def default_model_output_processing(transcription):
    # Filter out our transcription
    filtered_transcription = transcription[0]

    # split by words
    filtered_transcription = re.split(r" |-", filtered_transcription)

    return filtered_transcription

class WordExtractor:
    def __init__(self, model_name =  "jonatasgrosman/wav2vec2-large-xlsr-53-english", model_output_processing=default_model_output_processing):
        # Replace with your pre-trained phoneme model identifier from Hugging Face
        self.model_name = model_name
        # Load the phoneme tokenizer and model
        self.processor = Wav2Vec2Processor.from_pretrained(
            self.model_name,
        )

        self.model = Wav2Vec2ForCTC.from_pretrained(self.model_name)

        self.blank_token_id = self.processor.tokenizer.pad_token_id # for CTC loss

        self.model_output_processing = model_output_processing

    def extract_words(self, audio, sampling_rate=16000):
        # Load the audio file
        # Tokenize the audio file
        input_values = self.processor(audio, sampling_rate=sampling_rate, return_tensors="pt").input_values
        # retrieve logits from the model
        with torch.no_grad():
            logits = self.model(input_values).logits

        # take the probs
        probs = torch.softmax(logits, dim=-1)
        top2_probs, top2_ids = torch.topk(probs, k=2, dim=-1)

        # take argmax and decode, greedy decoding
        predicted_ids = torch.argmax(logits, dim=-1)

        # Decode the collapsed token sequences to get phoneme transcription strings
        # (The tokenizer's decode method will convert token ids to phoneme symbols)
        transcription = self.processor.batch_decode(predicted_ids)
        transcription = self.model_output_processing(transcription) # convert and filter our output


        return transcription

if __name__ == '__main__':
    from grapheme_to_phoneme import grapheme_to_phoneme
    from audio_recording import record_and_process_pronunciation

    # Load the audio file
    audio, sampling_rate = librosa.load("./temp_audio/output.wav", sr=16000)
    # Create the phoneme extractor
    extractor = WordExtractor()

    # Extract the phonemes
    phonemes = extractor.extract_words(audio, sampling_rate)
    ground_truth_phonemes = grapheme_to_phoneme("zero three five one")
    # phonemes, ground_truth_phonemes = record_and_process_pronunciation("the quick brown fox jumped over the lazy dog", extractor)

    print(phonemes)
    print(ground_truth_phonemes)
