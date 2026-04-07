# NASA Image Puller

A CLI tool that searches NASA's [Astronomy Picture of the Day (APOD)](https://apod.nasa.gov/) archive by keyword and downloads the most relevant images. Give it a date range and a query like "nebula" or "supernova," and it returns the two best-matching images ranked by a simple text-scoring algorithm against each entry's description.

<p align="center">
  <img src="docs/images/pipeline.png" width="700"/>
</p>

## Summary

- **API**: NASA APOD REST API -- fetches every entry in a user-specified date range as JSON
- **Scoring**: Bag-of-words relevance scoring -- each APOD description is tokenized and matched against the query terms, producing an integer relevance score
- **Selection**: Top-2 ranking -- the two highest-scoring, non-YouTube entries are selected for download
- **Retry logic**: Automatic retry (up to 3 attempts) on both the API fetch and each image download, with per-attempt status reporting
- **Config**: API key loaded from local file (`NASA_API_KEY.txt`) or environment variable, falling back to `DEMO_KEY`

## Architecture

<p align="center">
  <img src="docs/images/architecture.png" width="650"/>
</p>

The project is split into three modules behind a thin `main.py` orchestrator:

- **`main.py`** -- Entry point. Calls each module in sequence and catches `AppError` for clean exits.
- **`modules/globals.py`** -- Loads the API key (file > env var > demo fallback) and defines the custom `AppError` exception class. Every module imports from here.
- **`modules/input_handler.py`** -- Prompts the user for start date, end date, and search query. Validates dates against the APOD archive range (1995-06-16 through today). Contains `search_descriptions()`, which scores and ranks results.
- **`modules/connection_handler.py`** -- Builds the API URL, makes the HTTP request with retry logic, and handles binary image downloads to disk.

## How the scoring works

The core of the tool is `search_descriptions()` in `input_handler.py`. For each APOD entry in the fetched date range:

1. YouTube results are **filtered out** (APOD sometimes links video instead of images)
2. The entry's `explanation` field is lowercased and split into tokens
3. Each token is checked for membership in the set of query terms
4. The total number of matches becomes that entry's **relevance score**

The two entries with the highest scores are selected and their image URLs are returned.

<p align="center">
  <img src="docs/images/scoring_example.png" width="550"/>
</p>

This is intentionally a simple bag-of-words approach -- no TF-IDF, no stemming, no fuzzy matching. For a keyword like "nebula" across a month of APOD data, it works surprisingly well because NASA descriptions tend to repeat the subject noun many times.

## Setup

1. Get a free API key at [https://api.nasa.gov](https://api.nasa.gov/#signUp)
2. Provide the key via **one** of these methods:
   ```
   # Option A: local file
   echo "YOUR_KEY_HERE" > NASA_API_KEY.txt

   # Option B: environment variable
   export NASA_API_KEY=YOUR_KEY_HERE
   ```
3. Install the single dependency:
   ```
   pip install requests
   ```

## Usage

```
python main.py
```

You'll be prompted for three inputs:

| Prompt | Format | Default |
|--------|--------|---------|
| Start date | `YYYY-MM-DD` | `2024-01-01` |
| End date | `YYYY-MM-DD` | `2024-01-31` |
| Search query | any keywords | *(required)* |

Valid dates range from **1995-06-16** (the first APOD entry) to **today**. Leave dates blank to use the defaults. The tool downloads the two best matches as `image1.jpg` and `image2.jpg` in the working directory.

**Example session:**
```
Start date (YYYY-MM-DD): 2024-03-01
End date (YYYY-MM-DD): 2024-03-31
Search query: nebula
Saved image1.jpg
Saved image2.jpg
```

## Project structure

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
    .env.example                 # Template for environment-based config
    .gitignore                   # Ignores downloaded images, keys, caches
```

## Process

I built this as a way to get comfortable with REST API consumption in Python. The APOD API is one of the cleanest public APIs out there -- no auth tokens, no OAuth, just an API key in the query string -- so it made a good starting point.

The first version had image editing functionality baked in (filters, crops, etc.), but I ended up **removing all of it** because it didn't serve the core purpose. The project is about *finding* the right image, not processing it. Scope creep is real, and I caught it early.

The scoring algorithm was the most interesting design decision. I considered using something heavier -- cosine similarity with TF-IDF vectors, or even pulling in a sentence transformer -- but the APOD descriptions are short enough and keyword-dense enough that a basic word-match works well. For a one-month date range (roughly 30 entries), the top-2 results almost always match what you'd pick manually.

One thing I'd flag: the current approach treats all query terms equally and doesn't handle **multi-word phrases**. Searching for "black hole" scores "black" and "hole" independently, which means an entry about a "black cat" and a "hole in the ozone" could theoretically outscore an actual black hole image. For a dataset like APOD this rarely matters in practice, but it's a real limitation.

## Limitations and future work

- **No phrase matching** -- query terms are scored independently, as noted above
- **No stemming or lemmatization** -- "galaxies" won't match a query for "galaxy"
- **Fixed top-2 selection** -- the number of downloaded images is hardcoded rather than configurable
- **No caching** -- repeated queries to the same date range re-hit the API every time
- **No progress bar** -- large date ranges fetch silently until complete

If I were to extend this, I'd add **TF-IDF weighting** so that common words like "the" and "star" don't inflate scores, make the result count configurable via a CLI flag, and add a local cache with SQLite so repeated queries are instant.

## Final notes

This is a small project, but it taught me a few things worth noting. First, **modular structure matters even at small scale** -- splitting globals, input handling, and connection logic into separate files made the retry logic and the scoring algorithm independently testable and readable. Second, **simple algorithms can outperform expectations** when the domain is narrow. The bag-of-words scorer works because NASA writes descriptions for humans, not search engines, and they naturally repeat the subject keyword. Third, I learned to **cut scope aggressively** -- the original image editing features added complexity without adding value to what the project was actually about.
