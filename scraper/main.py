#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK

import argparse
from bs4 import BeautifulSoup
from datetime import date, timedelta
import os
import requests
import sys

URL_DOMAIN = "https://www.allocine.fr"


class Movie():
    rating_holder = ""

    def __init__(self, url):
        self.url = url

        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, "html.parser")

        title_property = self.soup.find("meta",  property="og:title")
        if not title_property:
            # movies page not found
            print(f"ERROR: page not found: {url}")
            return

        self.title = title_property["content"]
        self.image = self.soup.find("meta",  property="og:image")["content"]

        self.direction = []
        direction_div = self.soup.select(".meta-body-direction")
        if len(direction_div) > 0:
            for span in direction_div[0]("span")[1:]:
                self.direction.append(span.text)

        self.actors = []
        actors_div = self.soup.select(".meta-body-actor")
        if len(actors_div) > 0:
            for span in actors_div[0]("span")[1:]:
                self.actors.append(span.text)

        content_tag = self.soup.select(".content-txt")
        if content_tag:
            self.synopsis = content_tag[0].text.strip()

        notes = self.soup.select(".stareval-note")
        if len(notes) >= 2:
            self.press_note = self._to_note(notes[0].text)
            self.spectators_note = self._to_note(notes[1].text)
        else:
            self.press_note = 0
            self.spectators_note = 0

        rating_holders = self.soup.select(".rating-holder")
        if len(rating_holders):
            self.rating_holder = rating_holders[0]
        else:
            self.rating_holder = None

    def _to_note(self, note_text):
        if note_text == "--":
            note = 0
        else:
            note = float(note_text.replace(',', '.'))
        return note

    def print(self):
        print(f"{self.title}:")
        print("    direction: " + ", ".join(self.direction))
        print("    actors: " + ", ".join(self.actors))
        print(f"    synopsis: {self.synopsis}")
        print(f"    press: {self.press_note}")
        print(f"    spectators: {self.spectators_note}")
        print(f"    {self.url}")


def scrap_weekly_page(previous_date, current_date, next_date):
    export_path = f"weeklies/sem-{current_date}.html"

    print(
        f"Scraping {URL_DOMAIN}/film/agenda/sem-{current_date}/"
        f" into {export_path}..."
    )

    # get and parse allocine web page
    r = requests.get(
        f"{URL_DOMAIN}/film/agenda/sem-{current_date}/"
    )
    soup = BeautifulSoup(r.text, "html.parser")

    # remove covid 19 warnings
    alert_warning = soup.select(".alert-warning")[0]
    alert_warning.extract()
    alert_warning = soup.select(".emergency-visuel-wrapper")[0]
    alert_warning.extract()

    # go through movie cards
    for entity_card in soup.select(".entity-card"):
        # get movie's link
        entity_link = entity_card.select(
            ".meta-title-link"
        )[0]
        entity_href = entity_link.get("href", "")

        if not entity_href:
            continue

        # prepend movie's link with allocine domain
        entity_link["href"] = f"{URL_DOMAIN}{entity_href}"

        # get movie's informations
        movie = Movie(f"{URL_DOMAIN}{entity_href}")

        # insert movie's ratings inside the movie card
        if movie.rating_holder:
            div = soup.new_tag("div")
            div["class"] = "bam-container"
            div.append(movie.rating_holder)

            bam_container = entity_card.select(".bam-container")[0]
            bam_container.insert_before(div)

    # go through previous buttons
    for button in soup.select(".button-left"):
        button["class"] = "button button-primary-full button-left"
        a = button.wrap(soup.new_tag('a'))
        a["href"] = f"sem-{previous_date}.html"

    # go through next buttons
    for button in soup.select(".button-right"):
        button["class"] = "button button-md button-primary-full button-right"
        a = button.wrap(soup.new_tag('a'))
        a["href"] = f"sem-{next_date}.html"

    # export modified web page to local html file
    with open(export_path, "w", encoding='utf-8') as f:
        f.write(str(soup))


def main():
    parser = argparse.ArgumentParser(
        description="Scrap movies weekly releases from allocine.fr"
    )
    parser.add_argument(
        "date",
        help=(
            "date used to extract movies information from allocine"
            " (YYYY-MM-DD)"
        )
    )

    # enable bash tab completion if argcomplete is installed
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ModuleNotFoundError:
        pass
    except ImportError:
        pass

    args = parser.parse_args()

    # prepare output folder
    os.makedirs("weeklies", exist_ok=True)

    # scrap and modify weekly web pages
    current_date = date.fromisoformat(args.date)

    while current_date < date.today():
        previous_date = current_date - timedelta(days=7)
        next_date = current_date + timedelta(days=7)

        scrap_weekly_page(
            previous_date.strftime("%Y-%m-%d"),
            current_date.strftime("%Y-%m-%d"),
            next_date.strftime("%Y-%m-%d")
        )

        current_date = next_date

    return 0


if __name__ == "__main__":
    sys.exit(main())
