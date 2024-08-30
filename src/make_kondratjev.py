import argparse
import contextlib
import os
import re
import shlex
import subprocess

# :TRICKY: .*? - not greedy search
pat = re.compile(r"\((?P<aldono>.*?)\)")


def handle_diversified_word(word, on_word):
    def handle_word(word):
        handle_diversified_word(word, on_word)

    var_cnt = len(pat.findall(word))
    if var_cnt >= 1:
        m = pat.search(word)
        start, middle, end = (
            word[: m.start()],
            word[m.start("aldono") : m.end("aldono")],
            word[m.end() :],
        )

        # (retina) purpuraĵo
        handle_word((start + end).strip())
        handle_word(start + middle + end)
    else:
        on_word(word)


def make_hdw(to_x_system, all_index_variants=True):
    index_replaces = []

    if all_index_variants:
        index_replaces.extend(
            [
                ["ё", "е"],
            ]
        )

    d_letters = [
        ["c", "ĉ"],
        ["g", "ĝ"],
        ["h", "ĥ"],
        ["j", "ĵ"],
        ["s", "ŝ"],
        ["u", "ŭ"],
    ]

    def append_wr(letter, d_letter):
        index_replaces.append([letter + "x", d_letter])

    for letter, d_letter in d_letters:
        append_wr(letter, d_letter)
        append_wr(letter.upper(), d_letter.upper())

    if not to_x_system:
        index_replaces = [[new_letter, letter] for letter, new_letter in index_replaces]

    def func(word, on_word):
        def on_orig_word(word):
            word2 = word
            for letter, new_letter in index_replaces:
                word2 = word2.replace(letter, new_letter)

            # :TRICKY: соблюдаем порядок - с умляутами всегда раньше
            if to_x_system:
                on_word(word2)

            if all_index_variants and word2 != word:
                on_word(word)

            if not to_x_system:
                on_word(word2)

        handle_diversified_word(word, on_orig_word)

    return func


# классика: добавляет cx-варианты
with_x_hdw = make_hdw(False)


def parse_dictionary(src_fdir, on_parsed_article, all_index_variants=True):
    clean_replaces = [
        ["/", ""],
        ["`", ""],
        # [ж`алоб	|а] plendo;
        ["\t", ""],
    ]

    hdw = make_hdw(True, all_index_variants=all_index_variants)

    def append_index(word, lst):
        def on_word(word):
            lst.append(word)

        hdw(word, on_word)

    def parse_names(s, radixes):
        if not radixes:
            radixes = []
            gather_radixes = True
        else:
            gather_radixes = False

        raw_names = s.split(", ")

        names = []

        def add_word(name, gather_radixes):
            for w, r in clean_replaces:
                name = name.replace(w, r)

            stop = name.find("|")
            if stop != -1:
                radix = name[:stop]
                name = radix + name[stop + 1 :]
            else:
                radix = name

            if gather_radixes and radix:
                # append_index(radix, radixes)
                radixes.append(radix)

            # [скалол`аз ] grimpisto.
            name = name.strip()
            if name:
                append_index(name, names)

        for name in raw_names:
            cxu_finajxo = name.startswith("~")

            # 2008-05-06 23:30 avo
            # [~взр`осл|ость] plenkreskeco, adolteco;
            # [~ый] 1. _прил._ plenkreska, adolta;
            #   2. _сущ._ plenkreskulo, adolto.
            # if cxu_finajxo:
            if cxu_finajxo and radixes:
                assert radixes

                name = name[1:]
                for radix in radixes:
                    add_word(radix + name, False)
            else:
                add_word(name, gather_radixes)

        return names, radixes

    pat = re.compile("\r?\n\r?\n", flags=re.M)

    for fname in os.listdir(src_fdir):
        with open(os.path.join(src_fdir, fname), "rb") as src_f:
            txt = src_f.read().decode("cp1251")

            lst = pat.split(txt)
            for block in lst:
                lines = block.splitlines()

                find_sign = False
                for num, line in enumerate(lines):
                    if line.startswith("["):
                        find_sign = True
                        break

                lines = lines[num:] if find_sign else []
                radixes = []

                all_names = []
                for line in lines:
                    m = re.search(r"^\[(?P<name>[^\]]+)\]", line)
                    if m:
                        names, new_radixes = parse_names(m.group("name"), radixes)

                        all_names.extend(names)
                        if not radixes:
                            radixes = new_radixes

                on_parsed_article(all_names, lines)


# чтоб warning-ов не было по поводу \s, \., \/ и т.д.
def deliniarize(lines):
    lines = [line.replace("\\", "\\\\") for line in lines]
    return "\\n".join(lines)


@contextlib.contextmanager
def dictionary_generator(
    dst_fname,
    convert_accents=False,
    css_text=None,
    remove_srcfile=True,
    is_html=False,
    solid_text_format=True,
    gen_source_only=False,
):
    dir_fname = os.path.dirname(dst_fname)
    if not os.path.exists(dir_fname):
        os.makedirs(dir_fname)

    if css_text:
        css_text = deliniarize(css_text.splitlines())

    def style_article(article):
        if css_text:
            article = "<style>%(css_text)s</style>%(article)s" % locals()
        return article

    def make_on_parse(on_parsed_article):
        def on_parse(all_names, lines):
            if solid_text_format:
                lines = lines.splitlines()
            article = deliniarize(lines)

            # :TODO(ilya): вообще-то это лучше вынести в parse_dictionary(), так как
            # это частная особенность eoru.ru
            if convert_accents:
                # вставляем U-знак ударения
                # надо после ударной буквы, а не до
                # article = article.replace("`", "\u0301")
                strike_indexes = [i for i, ltr in enumerate(article) if ltr == "`"]
                for i in strike_indexes:
                    try:
                        article = (
                            article[:i] + article[i + 1] + "\u0301" + article[i + 2 :]
                        )
                    except Exception:
                        # set/protekta - почему-то ударение в конце статьи
                        pass

            # print(all_names)
            # print('\n'.join(lines))
            # print()

            on_parsed_article(all_names, article)

        return on_parse

    use_babylon = True
    if use_babylon:
        compiler_name = "babylon"
        with open(dst_fname, "w") as dst_f:
            fmt = "h" if is_html else "m"
            dst_f.write(
                """
#stripmethod=stripnewline
#sametypesequence=%(fmt)s
"""
                % locals()
            )

            def on_parsed_article(all_names, article):
                if all_names:
                    all_names = "|".join(all_names)
                    article = style_article(article)
                    dst_f.write(
                        """
%(all_names)s
%(article)s
"""
                        % locals()
                    )

            yield make_on_parse(on_parsed_article)

            # и после последней статьи должно быть 2 переноса строк
            dst_f.write("\n")

    else:
        article_dct = {}

        def on_parsed_article(all_names, article):
            for name in set(all_names):
                new_article = article
                old_article = article_dct.get(name)
                if old_article:
                    new_article = "%(old_article)s\\n\\n%(new_article)s" % locals()

                article_dct[name] = new_article

        yield make_on_parse(on_parsed_article)

        with open(dst_fname, "w") as dst_f:
            # для детерминированности результатов всегда сортируем по ключу;
            # :TRICKY: можно и по locale.strcoll(), только надо иметь локаль соответ., либо PyICU ставить,
            # http://stackoverflow.com/a/1098160

            # for name, article in article_dct.items():
            for name in sorted(article_dct):
                article = style_article(article_dct[name])
                dst_f.write("%(name)s\t%(article)s\n" % locals())

        compiler_name = "tabfile"

    if gen_source_only:
        return

    print("Compiling dictionary:", dst_fname)

    # dpkg --search /usr/lib/stardict-tools/tabfile = stardict-tools
    stardict_tools_path = os.environ.get(
        "STARDICT_TOOLS_PATH", "/usr/lib/stardict-tools"
    )
    compiler_bin = os.path.join(stardict_tools_path, compiler_name)

    subprocess.check_call(shlex.split("%(compiler_bin)s %(dst_fname)s" % locals()))

    if remove_srcfile:
        os.remove(dst_fname)


def make_dictionary_ex(
    parse_dictionary,
    dst_fname,
    convert_accents=False,
    css_text=None,
    remove_srcfile=True,
    is_html=False,
    solid_text_format=True,
    gen_source_only=False,
):
    with dictionary_generator(
        dst_fname,
        convert_accents=convert_accents,
        css_text=css_text,
        remove_srcfile=remove_srcfile,
        is_html=is_html,
        solid_text_format=solid_text_format,
        gen_source_only=gen_source_only,
    ) as on_parsed_article:
        parse_dictionary(on_parsed_article)


def make_dictionary(src_fdir, dst_fname, gen_source_only=False):
    def parse_dictionary_func(on_parsed_article):
        parse_dictionary(src_fdir, on_parsed_article)

    make_dictionary_ex(
        parse_dictionary_func,
        dst_fname,
        convert_accents=True,
        solid_text_format=False,
        gen_source_only=gen_source_only,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gen_source_only",
        action="store_true",
        help="generate source texts for stardict compiler only",
    )
    parser.add_argument("src_fdir")
    parser.add_argument("dst_fdir")
    args = parser.parse_args()

    # make_dictionary(src_fdir, dst_fname)
    join = os.path.join
    make_dictionary(
        join(args.src_fdir, "VortaroER-daily"),
        join(args.dst_fdir, "kondratjev-eo-ru/kondratjev-esperanto-rusa.txt"),
        gen_source_only=args.gen_source_only,
    )
    make_dictionary(
        join(args.src_fdir, "VortaroRE-daily"),
        join(args.dst_fdir, "kondratjev-ru-eo/kondratjev-rusa-esperanto.txt"),
        gen_source_only=args.gen_source_only,
    )


if __name__ == "__main__":
    main()
