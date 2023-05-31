from wiktionaryparser import WiktionaryParser

def get_german_definitions(word):
    language_code = 'en'  # English language code
    url = f"https://{language_code}.wiktionary.org/api/rest_v1/page/definition/{word}"

    response = requests.get(url)
    data = response.json()

    definitions = []

    if 'definitions' in data and len(data['definitions']) > 0:
        for entry in data['definitions']:
            if 'definitions' in entry:
                for definition in entry['definitions']:
                    if 'text' in definition:
                        definitions.append(definition['text'])

    return definitions

# Example usage
word = "Haus"
definitions = get_german_definitions(word)
print(f"Definitions for '{word}':")
for i, definition in enumerate(definitions):
    print(f"{i+1}. {definition}")
