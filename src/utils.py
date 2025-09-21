import csv
import os
from typing import Dict

import pandas as pd
from google.colab import files


def prepare_csv(response: Dict[str, str], filename: str, prepare_table: bool, download: bool, error: float = None, direction: str = None, url: str = None) -> pd.DataFrame:
    if prepare_table:
        fieldnames = ['continent', 'country', 'region', 'city', 'coordinates', 'confidence_score', 'reasoning', 'error', 'direction', 'url']

        if error and url and direction:
            response['error'] = error
            response['direction'] = direction
            response['url'] = url

        data = [response]

        is_file = os.path.exists(f"/content/{filename}")

        with open(filename, "a", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not is_file:
                writer.writeheader()
            writer.writerows(data)

        if download:
            files.download(f'/content/{filename}')

    df = pd.read_csv(f"/content/{filename}")
    return df