from text_cleanup import clean_text, porter_stem, remove_eng_stopwords, porter_stem

dirty_txt = """
    <div><h2>Lorem ipsum dolor :) sit amet, cats; stopword HE passed. Sed  will be sold sem. ;)
    </h2> <p>article<b>strong text</b> <a href="">Mauris ;( egestas erat quam, :< ut typed eros
    loses :> et.   ESFGF      ;< Daniel is a car dealer and   bought new cars ;-).</a></p></div>
    """

if __name__ == "__main__":
    print("Dirty text: \n", dirty_txt)
    cleaned_words = clean_text(dirty_txt)
    print("Cleaned text, displayed as words and emojis: \n", cleaned_words, "\n")
    cleaned_words_no_stopwords = remove_eng_stopwords(cleaned_words)
    print(
        "Cleaned text, displayed as words and emojis with no stopwords: \n",
        cleaned_words_no_stopwords,
        "\n"
    )
    stemmed_text = porter_stem(cleaned_words_no_stopwords)
    print("Stemmed word list: \n", stemmed_text)
