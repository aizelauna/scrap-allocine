# Allocine Scraper

## Description

Scraper of movies weekly releases from allocine.fr since the provided
date and until today.

This tool will:
- fetch weekly web page,
- fetch ratings from each movie web page,
- insert the ratings in the weekly web page,
- update previous and next buttons to link with local files,
- save the modified web page in the *weeklies* subfolder.

## Example

### Original card

![allocine-card-original](doc/allocine-card-original.jpg)

### Modified card

![allocine-card-modified](doc/allocine-card-modified.jpg)

### Weekly page

https://www.allocine.fr/film/agenda/sem-2020-10-28/

## Getting Started

```sh
git clone https://github.com/aizelauna/scrap-allocine.git
cd scrap-allocine

# Install scrap-allocine and its dependencies in a virtual environment
poetry install

# Scrap weekly pages since 2020/10/28 until today
poetry run scrap-allocine 2020-10-28
```

## Prerequisites

```sh
# Ubuntu
sudo apt install -y git

# Install poetry
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

