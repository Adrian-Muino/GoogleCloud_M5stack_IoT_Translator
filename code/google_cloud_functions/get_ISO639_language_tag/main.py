from langcodes import Language, standardize_tag
import json

def get_ISO639_language_tag(request):
    request_json = request.get_json()
    language_name = request_json['language_name']
    try:
        language_name_lower = language_name.lower()
        language = Language.get(language_name_lower, normalize=True)
        if language:
            iso639_tag = standardize_tag(language.bibliographic)
            return json.dumps({'iso639_language_tag': iso639_tag})
        else:
            return json.dumps({'iso639_language_tag': None})
    except:
        return json.dumps({'iso639_language_tag': None})
