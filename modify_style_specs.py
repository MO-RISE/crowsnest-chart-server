"""Modify style specification files for vector files
"""
import os
import re
import json
from pathlib import Path


def modify(styles_path):
    """Modify style specification files for vector tiles

    Modifies the source URL in the style specification files located in 'styles_path' if one of the following
    environment variables are present:

        TILE_SOURCE_URL_HOST
            Change the source URL's host to the variable's value (e.g. 'localhost:8080' to 'www.foo.bar').

        TILE_SOURCE_URL_HTTPS
            Change the source URL's protocol to HTTPS.
    """
    env_vars = os.environ
    if any(
        (ev in env_vars for ev in ["TILE_SOURCE_URL_HOST", "TILE_SOURCE_URL_HTTPS"])
    ):

        print("Modifying the style specification files ....")

        new_protocol = "https" if "TILE_SOURCE_URL_HTTPS" in env_vars else None

        new_host = (
            env_vars["TILE_SOURCE_URL_HOST"]
            if "TILE_SOURCE_URL_HOST" in env_vars
            else None
        )

        for path in Path(styles_path).iterdir():
            with open(path, encoding="utf-8") as file:
                style_spec = json.load(file)
            for key, value in style_spec["sources"].items():
                src_url = value["url"]
                match = re.search(
                    "(https?)://([A-Za-z0-9_.:]+)(/[A-Za-z0-9_/.]+)", src_url
                )
                new_protocol = (
                    "https" if "TILE_SOURCE_URL_HTTPS" in env_vars else match.group(1)
                )
                new_host = (
                    env_vars["TILE_SOURCE_URL_HOST"]
                    if "TILE_SOURCE_URL_HOST" in env_vars
                    else match.group(2)
                )
                new_src_url = new_protocol + "://" + new_host + match.group(3)
                style_spec["sources"][key]["url"] = new_src_url
            with open(path, "w", encoding="utf-8") as file:
                json.dump(style_spec, file, indent=4)
            print(f"  Successfully modified the file '{path.name}'")
            print(f"   from: {src_url}")
            print(f"   to: {new_src_url}")


if __name__ == "__main__":
    modify("/data/styles")
