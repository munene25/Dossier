from rest_framework.response import Response
from rest_framework.decorators import api_view
import ollama
from pathlib import Path
from resumes import utils
import json
from jsonschema import validate, ValidationError


path = Path(__file__).parent
with open(Path(path)/ 'json_schema.json') as _json:
    schema = json.load(_json)


@api_view(['GET'])
def generate(request):  
    test_resume_path = Path(__file__).parent.parent /'resumes'/'tests'/'test_resume.pdf'
    response = ollama.generate(
        model='json_generator',
        prompt=utils.parse_resume(test_resume_path),
        format=schema,
    )
    json_response = json.loads(response.response)
    try:
        validate(schema=schema, instance=json_response)
        return Response(json_response)
    except ValidationError as e:
        return Response({"error": "Unexpected error", "details": str(e), 'response': json_response}  , status=500)
    