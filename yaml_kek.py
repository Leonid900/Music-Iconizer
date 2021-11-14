import yaml
from pprint import pprint
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent


with open(BASE_DIR.joinpath('mysong.yaml')) as f:
    templates = yaml.safe_load(f)

pprint(templates)
