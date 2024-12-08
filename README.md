# WordCloud API

A FastAPI application that generates wordcloud images from input text.

## Features

- Create wordcloud images from text input
- Preprocess text using tokenization, stopword removal, and lemmatization
- Generate PNG images of wordclouds
- RESTful API endpoint for easy integration

## Getting Started

0. Install `uv` if you haven't already:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

1. Clone the repository:
```
git clone https://github.com/ntsmac/wordcloud-api.git
cd wordcloud-api
```

2. Run the application (uv manages the dependencies!):
   ```
   uv run fastapi dev
   ```

## Usage

Send a POST request to `/create_wordcloud` with a JSON body containing the text:

```json
{
  "text": "Your text here..."
}
```

The API will respond with a PNG image of the generated wordcloud.

## Testing

To run tests:
```
pytest
```
