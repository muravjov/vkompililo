#!/usr/bin/env python
# coding: utf-8

import os
import o_p
import io

project_dir_fname = os.path.dirname(__file__)

download_data_fdir = None
def setup_download_data(src_fdir):
    global download_data_fdir
    download_data_fdir = src_fdir

def make_dpath(*fname):
    #download_data_fdir = o_p.join(project_dir_fname, "download_data")
    
    assert download_data_fdir, "call setup_download_data() first"
    return o_p.join(download_data_fdir, *fname)

def for_write(fpath):
    return open(fpath, "w")

def open_write_path(fpath):
    o_p.force_makedirs(os.path.dirname(fpath))
    return for_write(fpath)

def open_dpath(path, *fname):
    fpath = make_dpath(path, *fname)
    return open_write_path(fpath)

def make_sm_fpath(word):
    return make_dpath("words", word[0], word)

def save_search_mark(word, is_found=True):
    # для успеха - наличие пустого файла
    with open_write_path(make_sm_fpath(word)) as f:
        if not is_found:
            f.write("not found")

import lxml.html as l_html
from lxml import etree

def process_search_data(src_f, on_article):
    # http://lxml.de/tutorial.html
    is_xhtml = False
    tree = l_html.parse(src_f, l_html.xhtml_parser if is_xhtml else l_html.html_parser)
    articles = tree.getroot().body.getchildren()
    
    for article in articles:
        on_article(article)

def complement_html(txt):
    return """<!DOCTYPE html>
<html>
<head>
<title></title>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
<link href="css/common.css" rel="stylesheet" type="text/css" />
</head>
<body>

%(txt)s

</body>
</html>
""" % locals()

def process_vip_text(txt, on_article):
    txt = complement_html(txt)
    process_search_data(io.StringIO(txt), on_article)

def iter_tags(element, name):
    return element.iterfind(".//%(name)s" % locals())

import make_kondratjev
vip_hdw = make_kondratjev.with_x_hdw

def get_search_words(article):
    lst = []
    def on_word(word):
        word = word.replace('/', '')
        # <dfn></dfn> в статье про oleo
        if word:
            lst.append(word)
    for dfn in iter_tags(article, "dfn"):
        txt = dfn.text
        # <dfn class="rea"><em>Rea</em></dfn>
        if txt is None:
            txt = dfn.text_content()
            
        vip_hdw(txt, on_word)
        
    return lst

def gen_html_text(article):
    return etree.tostring(article, pretty_print=True, encoding="utf-8").decode("utf-8")

def save_word(word, txt):
    is_found = bool(txt)
    
    if is_found:
        def on_article(article):
            fname = article.get("id")
            assert fname, "Bad article id; the ban has been, probably."
            txt = gen_html_text(article)
            words = get_search_words(article)
        
            #print()
            #print(fname)
            #print(words)
            #print(txt)
            
            with open_dpath("articles", fname) as article_f:
                article_f.write(txt)
                
            for word in words:
                save_search_mark(word)
        process_vip_text(txt, on_article)
    save_search_mark(word, is_found)
    
def read_all_file(fname):    
    with open(fname) as src_f:
        return src_f.read()
    
def rewrite_text(fname, txt):
    with for_write(fname) as dst_f:
        dst_f.write(txt)
    
    
def gen_orig_html():
    src_fname = "/home/ilya/opt/programming/eoru/vkompililo/sample/marko"
    dst_fname = "/home/ilya/opt/programming/eoru/vkompililo/sample/marko_copy.html"
    
    txt = read_all_file(src_fname)
    rewrite_text(dst_fname, complement_html(txt))

def create_vip_vortaro(dst_fname, remove_srcfile=True):
    
    use_external_css = False
    css_txt = read_all_file(o_p.join(project_dir_fname, "sample/vip/vip.css"))
    
    def parse_dictionary(on_parsed_article):
        src_fdir = make_dpath("articles")
        
        # :REFACTOR:
        for fname in os.listdir(src_fdir):
            txt = read_all_file(os.path.join(src_fdir, fname))
            
            all_names = []
            vip_href_prefix = "?w="
            fixed_text = []
            php_len = len(vip_href_prefix)
            def on_article(article):
                all_names.extend(get_search_words(article))
                
                for a in iter_tags(article, "a"):
                    href = a.get("href")
                    assert href.startswith(vip_href_prefix)
                    # подсказка по bword:
                    # http://siripong-english.blogspot.ru/2011/04/custom-dictionary-w-stardict-in-babylon.html
                    a.set("href", "bword://" + href[php_len:])
                    
                fixed_text.append(gen_html_text(article))
            process_vip_text(txt, on_article)
            
            txt = fixed_text[0]
            css_txt
            article_txt = txt # "<style>%(css_txt)s</style>%(txt)s" % locals()
            on_parsed_article(all_names, article_txt)
    
    make_kondratjev.make_dictionary_ex(parse_dictionary, dst_fname, css_text=None if use_external_css else css_txt,
                                    remove_srcfile=remove_srcfile, is_html=True)

    ## меняем sametypesequence=m => sametypesequence=h
    #oft_fname = os.path.splitext(dst_fname)[0] + ".ifo"
    #oft_txt = read_all_file(oft_fname)
        
    #import re
    #oft_txt = re.sub(r"sametypesequence=m", "sametypesequence=h", oft_txt)
    #rewrite_text(oft_fname, oft_txt)

def main():
    if False:
        src_fname = "/home/ilya/opt/programming/eoru/vkompililo/sample/day_ban.html"
        with open(src_fname) as src_f:
            save_word("marko", src_f.read())
            
    if True:
        dst_fname = "/home/ilya/.stardict/dic/VIP/VIP2015.txt"
        create_vip_vortaro(dst_fname, False)
        
    if False:
        #src_fname = "sample/article_8347"
        #src_fname = "download_data/articles/article_11861"
        src_fname = "download_data/articles/article_5630" # article_6504" # article_16311" # 
        txt = read_all_file(o_p.join(project_dir_fname, src_fname))
        def on_article(article):
            print(get_search_words(article))
        process_vip_text(txt, on_article)

if __name__ == '__main__':
    main()
