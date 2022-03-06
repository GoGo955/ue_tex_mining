from text_cleanup import clean_text, remove_eng_stopwords

dirty_txt = """
    <div><h2>Lorem ipsum dolor :) sit amet, consectetur; adipiscing elit. Sed eget mattis sem. ;)
    </h2> <p>article<b>strong text</b> <a href="">Mauris ;( egestas erat quam, :< ut faucibus eros
    congue :> et.   ESFGF      ;< tristique augue risus eu risus ;-).</a></p></div>
    """

if __name__ == "__main__":
    print("Dirty text: \n", dirty_txt)
    cleaned_words = clean_text(dirty_txt)
    print("Cleaned text, displayed as words and emojis: \n", cleaned_words)
    cleaned_words_no_stopwords = remove_eng_stopwords(cleaned_words)
    print(
        "Cleaned text, displayed as a list of words and emojis with no stopwords: \n",
        cleaned_words_no_stopwords
    )
