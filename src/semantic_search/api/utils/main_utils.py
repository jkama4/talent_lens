from .. import llm, constants

import csv

from pathlib import Path

from typing import Dict, List


def extract_consultant_data(
    csv_path: Path,
) -> List[Dict]:
    
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f=f)
        data = []
        for row in reader:
            data.append(row)

    return data