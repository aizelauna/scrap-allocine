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

## Deploy

```shell
# Build Wheel package
poetry build

# Install scrap-allocine as a CLI tool to the current user environment
pipx install $(ls dist/*.whl)
```

## Prerequisites

```sh
# Ubuntu
sudo apt install -y git python3-argcomplete

# Enable argcomplete
sudo activate-global-python-argcomplete3

# Install pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install poetry
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

