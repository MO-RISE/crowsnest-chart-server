import os
import sys
import json
from pathlib import Path
from distutils.dir_util import copy_tree

THIS_DIR = Path(__file__).parents[1].resolve()
sys.path.append(str(THIS_DIR))

import pytest

from modify_style_specs import *


@pytest.fixture
def styles_path(tmpdir):

    styles_path = tmpdir

    # Copy style specs
    origin = THIS_DIR / "styles"
    copy_tree(str(origin), str(styles_path))

    yield styles_path


def test_modify(styles_path):

    new_host = "www.foobar.com"
    os.environ["TILE_SOURCE_URL_HOST"] = new_host
    os.environ["TILE_SOURCE_URL_HTTPS"] = "1"

    modify(styles_path)

    for p in Path(styles_path).iterdir():
        with open(p) as f:
            style_spec = json.load(f)
        for key, value in style_spec["sources"].items():
            src_url = value["url"]
            m = re.search("(https?)://([A-Za-z0-9_.:]+)(/[A-Za-z0-9_/.]+)", src_url)

            assert m.group(1) == "https"
            assert m.group(2) == new_host
