import ollama
from pathlib import Path
import json


path = Path('backend/ollama_app')
with open(Path(path) / 'system_prompt.txt', 'r')as text:
    system_prompt = text.read()

with open(Path(path)/ 'json_schema.json') as _json:
    schema = json.load(_json)


ollama.create(
    model='json_generator',
    from_='phi4',
    system=system_prompt,

    
)

