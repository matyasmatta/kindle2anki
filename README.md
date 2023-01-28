# Kindle2Anki

Simple and elegant way of converting Kindle Vocabulary into properly formatted Anki flashcards.

**Supported languages**
- Spanish (SpanishDict)

**Export format**
- field 1: Spanish word formatted (nouns have articles, ...)
- field 2: translation into English
- field 3: wordType (N/V/Adv/Adj/Conj)
- field 4: gender (only for nouns) 

**How to use**
- connect Kindle to computer
- download KindleMate from https://kmate.me/
- in KindleMate: Options - Words Copy/Export format - leave only "Stem"
- in KindleMate: choose all words you want to export, right-click - export to file - and choose "Anki"
- open Kindle2Anki and choose the exported file
- submit file
- console may appear, ignore all errors - they are non-critical
- output.exe file will appear in Kindle2Mate source folder
- open Anki and import the whole file (I recommend "Spanish" card type from Duolingo Vocab pack, see https://ankiweb.net/shared/info/247695077)
- for next use make sure output.txt is _empty_ (else it will be appended, Anki should detect duplicates and ignore them fortunately)
- you can add SpanishDict sound files via AwesomeTTS, see https://ankiweb.net/shared/info/1436550454 (HyperTTS does not have SpanishDict, yet!)
