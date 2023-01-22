type = "ADJECTIVE"
word = "cocinada"

if "ADJECTIVE" in type:
    type = "Adj"
    if word.endswith("ado"):
        word = word + ", " + word[:-3] + "ada"
    elif word.endswith("ada"):
        word = word[:-3] + "ado" + ", " + word

print(word)