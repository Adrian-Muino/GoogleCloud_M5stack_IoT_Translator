import langcodes

def get_BCP47_language_tag(request):
    try:
        language_input = request.args.get('language_input', '').lower()
        language = langcodes.find(language_input)
        bcp47_language_tag = language.language
        return bcp47_language_tag
    except Exception as e:
        return f"Error: {str(e)}"

