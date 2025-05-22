from detoxify import Detoxify
from googletrans import Translator
from better_profanity import profanity
from langdetect import detect, LangDetectException
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

translator = Translator()
profanity.load_censor_words()

tokenizer = AutoTokenizer.from_pretrained("tuner007/pegasus_paraphrase")
paraphrase_model = AutoModelForSeq2SeqLM.from_pretrained("tuner007/pegasus_paraphrase")
paraphrase_model.eval()
model = Detoxify('original')

def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return 'en'

def translate_to_english(text, detected_lang):
    return translator.translate(text, dest='en').text if detected_lang != 'en' else text

def translate_back(text, lang):
    try:
        return translator.translate(text, dest=lang).text if lang != 'en' else text
    except Exception:
        return text

def paraphrase_text(text):
    try:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=60
        )
        generated_ids = paraphrase_model.generate(
            **inputs,
            max_length=60,
            num_beams=5,
            num_return_sequences=1,
            temperature=1.5,
            early_stopping=True
        )
        return tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    except Exception:
        return "Couldn't paraphrase."

def check_toxicity_level(text):
    results_raw = model.predict([text])
    return {
        key.replace('_', ' '): round(value[0] * 100, 2)
        for key, value in results_raw.items()
    }

def clean_text(text):
    words = text.split()
    return ' '.join(['****' if profanity.contains_profanity(w.lower()) else w for w in words])
