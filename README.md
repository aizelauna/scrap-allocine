# Allocine Scraper

Scraper of movies weekly releases from allocine.fr since the provided
date and until today.

Here is an exemple of weekly releases web page:
https://www.allocine.fr/film/agenda/sem-2021-03-03/

## Getting Started

```sh
git clone https://github.com/aizelauna/scrap-allocine.git
cd scrap-allocine

# Install scrap-allocine and its dependencies in a virtual environment
poetry install

# Scrap weekly pages since 2021/03/03 until today
poetry run scrap-allocine 2021-03-03
```

## Prerequisites

```sh
# Ubuntu
sudo apt install -y git

# Install poetry
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```
