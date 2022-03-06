import re


if __name__ == "__main__":
    # zad 1a
    no_digits_text = re.sub("\d", "", "Dzisiaj mamy 4 stopnie na plusie, 1 marca 2022 roku")
    print("Text cleared from digits:\n",no_digits_text)

    # zad 1b
    html_text = """
    <div><h2>Header</h2> <p>article<b>strong text</b> <a href="">link</a></p></div>
    """
    no_html_text = re.sub("<.*?>", " ", html_text)
    no_html_text = re.sub("\s{2,}", " ", no_html_text)
    print("Text cleared from html elements:\n", no_html_text)

    # zad 1c
    lore_ipsum = """
    Lorem ipsum dolor sit amet, consectetur; adipiscing elit.
    Sed eget mattis sem. Mauris egestas erat quam, ut faucibus eros congue et. In
    blandit, mi eu porta; lobortis, tortor nisl facilisis leo, at tristique augue risus eu risus.
    """
    no_punctuation_marks = re.sub("[^A-Za-z\s]+", "", lore_ipsum)
    print("Text cleared from punctuationmarks:\n", no_punctuation_marks)

    # zad 2
    hashtag_txt = """
    Lorem ipsum dolor
    sit amet, consectetur adipiscing elit. Sed #texting eget mattis sem. Mauris #frasista
    egestas erat #tweetext quam, ut faucibus eros #frasier congue et. In blandit, mi eu porta
    lobortis, tortor nisl facilisis leo, at tristique #frasistas augue risus eu risus.
    """
    hashtags = re.findall("(\#[A-Za-z0-9]+)", hashtag_txt)
    print("Hashtags are: ", hashtags)

    # zad 3
    emojis_txt = """
    Lorem ipsum dolor :) sit amet, consectetur; adipiscing elit. Sed eget mattis sem. ;)
    Mauris ;( egestas erat quam, :< ut faucibus eros congue :> et. In blandit, mi eu porta;
    lobortis, tortor :-) nisl facilisis leo, at ;< tristique augue risus eu risus ;-).
    """
    emojis = re.findall("[;:><()-]{2,3}", emojis_txt)
    print("Emojis are:", emojis)
