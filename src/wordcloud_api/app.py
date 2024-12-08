import ssl
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import nltk
from pydantic import BaseModel
import uvicorn
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tempfile
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


app = FastAPI()


class TextInput(BaseModel):
    text: str


def download_nltk_deps():
    try:  # Solves SSL error: Thanks: https://github.com/gunthercox/ChatterBot/issues/930#issuecomment-322111087
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download("stopwords")
    nltk.download("punkt_tab")
    nltk.download("wordnet")


def preprocess_text(text: str) -> str:
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return " ".join(tokens)


@app.post("/create_wordcloud")
async def create_wordcloud(input_text: TextInput):
    processed_text = preprocess_text(input_text.text)

    if len(processed_text.split()) == 0:
        raise HTTPException(
            status_code=400,
            detail="No words found in the input text after preprocessing.",
        )

    # Generate wordcloud
    wordcloud = WordCloud(
        width=800, height=400, random_state=21, max_font_size=110
    ).generate(processed_text)

    # Create a temp file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        plt.figure(figsize=[10, 8])
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(tmp.name, bbox_inches="tight")

        # Return the image
        return FileResponse(tmp.name, media_type="image/png")


if __name__ == "__main__":
    download_nltk_deps()
    uvicorn.run(app, host="0.0.0.0", port=8000)
