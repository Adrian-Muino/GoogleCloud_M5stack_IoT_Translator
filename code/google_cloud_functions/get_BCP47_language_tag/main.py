from langcodes import Language
import json

def get_BCP47_language_tag(request):
    request_json = request.get_json()
    language_name = request_json['language_name']
    try:
        lang = Language.find(language_name)
        return json.dumps({'bcp47_language_tag': lang.bcp47})
    except:
        return json.dumps({'bcp47_language_tag': None})
