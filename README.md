# NASA Image Puller

A CLI tool that searches NASA's [APOD](https://apod.nasa.gov/) archive by keyword and downloads the most relevant images. Given a date range and a query like "nebula," it ranks every entry using a bag-of-words relevance scorer and downloads the top two matches.

<p align="center">
  <img src="docs/images/pipeline.png" width="700"/>
</p>

## Skills & Frameworks

Python, REST API consumption, HTTP retry logic, bag-of-words text scoring, modular architecture, CLI design, Requests library

## Summary

- **API**: NASA APOD REST API -- fetches every entry in a date range as JSON
- **Scoring**: Bag-of-words relevance scoring -- tokenizes each description and counts query-term matches
- **Selection**: Top-2 ranking with YouTube filtering
- **Retry logic**: Automatic retry (up to 3 attempts) on API fetch and image download
- **Config**: API key loaded from file, env var, or `DEMO_KEY` fallback

## Architecture

<p align="center">
  <img src="docs/images/architecture.png" width="650"/>
</p>

Three modules behind a thin `main.py` orchestrator:

- **`modules/globals.py`** -- API key loading (file > env var > demo fallback), base URL, custom `AppError` exception
- **`modules/input_handler.py`** -- Date/query prompts with validation, `search_descriptions()` relevance scorer
- **`modules/connection_handler.py`** -- HTTP requests with retry logic, binary image downloads

## Scoring Algorithm

For each APOD entry in the date range:

1. Filter out YouTube results (APOD sometimes links video)
2. Lowercase the `explanation` field and split into tokens
3. Count matches against the query term set
4. Select the two highest-scoring entries

<p align="center">
  <img src="docs/images/scoring_example.png" width="550"/>
</p>

I chose bag-of-words over TF-IDF or sentence transformers because NASA descriptions are short and keyword-dense -- the subject noun is naturally repeated, so simple word-matching reliably surfaces the best results.

**Known tradeoff**: query terms are scored independently, so "black hole" matches "black" and "hole" separately. Rarely matters for APOD data in practice.

## Setup

1. Get a free API key at [api.nasa.gov](https://api.nasa.gov/#signUp)
2. Provide the key:
   ```
   echo "YOUR_KEY_HERE" > NASA_API_KEY.txt
   # or: export NASA_API_KEY=YOUR_KEY_HERE
   ```
3. Install dependencies:
   ```
   pip install requests
   ```

## Usage

```
python main.py
```

| Prompt | Format | Default |
|--------|--------|---------|
| Start date | `YYYY-MM-DD` | `2024-01-01` |
| End date | `YYYY-MM-DD` | `2024-01-31` |
| Search query | any keywords | *(required)* |

Valid dates: **1995-06-16** through **today**. Downloads `image1.jpg` and `image2.jpg` to the working directory.

## Project Structure

```
nasa-image-puller/
    main.py                      # Entry point -- orchestrates the pipeline
    modules/
        __init__.py              # Re-exports all module interfaces
        globals.py               # API key loading, base URL, AppError
        connection_handler.py    # HTTP requests with retry, image downloads
        input_handler.py         # Date/query prompts, relevance scoring
    docs/
        images/                  # Diagrams for this README
        generate_diagrams.py     # Script that produces the diagrams
```
