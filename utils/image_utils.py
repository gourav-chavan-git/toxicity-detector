import base64
from io import BytesIO
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud_image(text):
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    buffer = BytesIO()
    wc.to_image().save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str
