import json
from pathlib import Path

def load_config(path):
    path = Path(path)
    data = json.loads(path.read_text(encoding=\"utf-8\"))
    # very light validation
    assert \"system\" in data, \"Missing 'system' section\"
    assert \"simulation\" in data, \"Missing 'simulation' section\"
    assert data[\"system\"].get(\"type\"), \"system.type required\"
    return data
