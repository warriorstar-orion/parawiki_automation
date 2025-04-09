import json
from urllib.parse import urlparse

import click
from mwclient import Site
from mwclient.page import Page


@click.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
@click.option("--recipe_data", required=True)
@click.option("--url", required=True)
def main(username, password, recipe_data, url):
    url = urlparse(url)
    site_args = {"host": url.hostname}
    if url.path:
        site_args["path"] = url.path
    if url.scheme:
        site_args["scheme"] = url.scheme

    site = Site(**site_args)
    site.login(username, password)

    with open(recipe_data, "r", encoding="utf-8") as f:
        wiki_data = json.load(f)

    for page_name, page_data in wiki_data.items():
        if not page_name.startswith("Template:RecursiveFood"):
            continue
        page: Page = site.pages[page_name]
        current_content = page.text()
        new_content = page_data["page_text"].strip()
        print(f"{page_name}...", end="")
        if current_content.strip() == new_content.strip():
            print("unchanged.")
            continue
        page.edit(new_content.strip(), bot=True, summary="Automated recipe update")
        print("modified.")
