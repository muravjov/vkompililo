
def parse_dictionary(on_parsed_article):
    fpath = "/home/ilya/opt/programming/eoru/muravjov-src.txt"
    with open(fpath) as f:
        articles = f.read().split("\n\n")
        
        pat = "^(?P<word>.+?) - "
        import re
        for article in articles:
            if article:
                words = []
                for m in re.finditer(pat, article, flags=re.M):
                    word = m.group("word").strip()
                    word_lst = word.split(" = ")
                    words.extend(word_lst)
                    
                # :TODO: скрыть
                if not words:
                    print(article)
                    print()
                else:
                    # :TRICKY: это пользовательский словарь, и там есть в одной статье слова совсем не синонимы,
                    # например, tamburo (барабан) и kruco (крест); подобное ведет (в Goldendict) к лишним находкам,
                    # поэтому (а также для выделенного доступа) добавляем префикс "."
                    words = ["." + word for word in words]
                    on_parsed_article(words, article)
                    
def main():
    dst_fpath = "/home/ilya/.stardict/dic/esperanto/muravjov/muravjov"
    import make_kondratjev
    make_kondratjev.make_dictionary_ex(parse_dictionary, dst_fpath)

if __name__ == '__main__':
    main()