from django.shortcuts import render
from utils.nlp_utils import (
    detect_language,
    translate_to_english,
    translate_back,
    check_toxicity_level,   # updated function name
    clean_text,             # updated function name
    paraphrase_text
)
from utils.image_utils import generate_wordcloud_image
from langdetect.lang_detect_exception import LangDetectException


def home(request):
    return render(request, 'index.html')


def check_toxicity(request):
    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        if not comment:
            return render(request, 'partials/toxicity_result.html', {'error': 'Please enter a comment to analyze.'})

        try:
            lang = detect_language(comment)
            translated = translate_to_english(comment, lang) if lang != 'en' else comment  # updated to pass detected lang
            toxicity_scores = check_toxicity_level(translated)  # updated function name

            return render(request, 'partials/toxicity_result.html', {
                'comment': comment,
                'translated': translated if lang != 'en' else None,
                'results': toxicity_scores
            })
        except LangDetectException:
            return render(request, 'partials/toxicity_result.html', {'error': 'Language detection failed. Try a longer input.'})


def clean_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        if not comment:
            return render(request, 'partials/clean_result.html', {'error': 'Please enter a comment to clean.'})

        try:
            lang = detect_language(comment)
            translated = translate_to_english(comment, lang) if lang != 'en' else comment  # updated to pass detected lang

            cleaned = clean_text(translated)  # updated function name
            paraphrased = paraphrase_text(cleaned)

            cleaned_back = translate_back(cleaned, lang) if lang != 'en' else cleaned
            paraphrased_back = translate_back(paraphrased, lang) if lang != 'en' else paraphrased

            return render(request, 'partials/clean_result.html', {
                'comment': comment,
                'clean_comment': cleaned_back,
                'paraphrased_comment': paraphrased_back
            })

        except LangDetectException:
            return render(request, 'partials/clean_result.html', {'error': 'Language detection failed. Try a longer input.'})


def wordcloud_view(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '').strip()
        if not comment_text:
            return render(request, 'partials/wordcloud_result.html', {'error': 'Please enter text for word cloud.'})

        image_base64 = generate_wordcloud_image(comment_text)
        return render(request, 'partials/wordcloud_result.html', {'wordcloud_image': image_base64})



