
from wiktionaryparser import WiktionaryParser

def get_definition(language, word, count=4):

    parser = WiktionaryParser()
    parsed = parser.fetch(word, language)

    definition = []
    count += 1
    definition_count = 1
    while definition_count < count:
        try:
            definition.append(parsed[0]['definitions'][0]['text'][definition_count])
            definition_count += 1
        except:
            break
    
    if get_wordtype(language, word) == "verb":
        if "transitive" or "reflexive" in definition:
            definition = definition[0].split(")")
            try:
                definition = definition[1]
            except:
                definition = definition[0]
            if "(" in definition:
                definition = definition.split("(")
                definition = definition[0]
    if type(definition) is list:
        if len(definition) == 2:
            definition = definition[1]
        else:
            definition = definition[0]
        if definition.startswith(" "):
            definition = definition[1:]
        if definition.endswith(" "):
            definition = definition[0:-1]
    return definition

def get_wordtype(language, word):
    parser = WiktionaryParser()
    parsed = parser.fetch(word, language)

    wordtype = parsed[0]['definitions'][0]['partOfSpeech']
    return wordtype

def get_example(language, word, count = 1):
    parser = WiktionaryParser()
    parsed = parser.fetch(word, language)

    examples = []
    inner_counter = 0
    while inner_counter < count:
        try:
            to_append = parsed[0]['definitions'][0]['examples'][inner_counter]
            to_append = to_append.split("―")
            to_append = to_append[0].split(".")
            to_append = to_append[0] + "."
            examples.append(to_append)
            inner_counter += 1
        except:
            break
    try:
        if examples[0][0].isupper() == False:
            examples = examples[0][0:-2]
    except:
        pass
    try:
        if len(examples[0]) > 150:
            examples = ""
        examples = examples[0]
    except:
        pass
    if examples.startswith("Synonym"):
        global synonyms
        synonyms = examples[9:-1]
        examples = ""
    return examples

def get_gender(language, word):
    parser = WiktionaryParser()
    parsed = parser.fetch(word, language)

    gender = parsed[0]['definitions'][0]['text'][0]
    gender = gender.split("\xa0")
    gender = gender[1]
    gender = gender[0]
    return gender


def get_additionals(language, word):
    additionals = ""
    wordtype = get_wordtype(language, word)
    if wordtype == 'noun':
        gender = get_gender(language, word)
        if gender == "f":
            word = "die " + word
        if gender == "m":
            word = "der " + word
        if gender == "n":
            word = "das " + word
        
    elif wordtype == 'verb':
        preterite = get_preterite(language, word)
        perfectum = get_perfectum(language, word)
        additionals = preterite + ", " + perfectum
    return word, additionals

def get_preterite(language, word):
    parser = WiktionaryParser()
    parsed = parser.fetch(word, language) 
    preterite = parsed[0]['definitions'][0]['text'][0]
    preterite = preterite.split("tense ")
    preterite = preterite[1]
    preterite = preterite.split(", past")
    preterite = preterite[0]
    return preterite

def get_perfectum(language, word):
    parser = WiktionaryParser()
    parsed = parser.fetch(word, language) 
    participle = parsed[0]['definitions'][0]['text'][0]
    participle = participle.split("participle ")
    participle = participle[1]
    participle = participle.split(", auxiliary")
    participle = participle[0]

    auxiliary = parsed[0]['definitions'][0]['text'][0]
    auxiliary = auxiliary.split("auxiliary ") 
    auxiliary = auxiliary[1]
    auxiliary = auxiliary[:-1]

    if auxiliary == "sein":
        auxiliary = "s. "
    if auxiliary == "haben":
        auxiliary = "h. "
    
    perfectum = auxiliary + participle

    return perfectum

        
    
def get_data(word):
    global synonyms
    synonyms = ""
    additionals = ""
    example = ""
    
    definition = get_definition('german', word, 1)
    wordtype = get_wordtype('german', word)
    try:
        example = get_example('german', word)
    except:
        pass
    try:
        word, additionals = get_additionals('german', word)
    except:
        pass

    return word, definition, wordtype, example, additionals, synonyms

if __name__ == '__main__':
    word = "vertiefen"
    word, definition, wordtype, example, additionals, synonyms = get_data(word)
    print(word, definition, wordtype, example, additionals, synonyms)