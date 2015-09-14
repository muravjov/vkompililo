import os
import o_p

from lxml import etree
# например, описание символов, &gcirc; и т.д., дано в revo/dtd/vokosgn.dtd
parser = etree.XMLParser(load_dtd=True, remove_comments=True)

def open_xml_tree(pth):
    with open(pth) as f:
        #print(meta_f.read())
        # если parser не указан, то берется по умолчанию - XMLParser
        tree = etree.parse(f, parser=parser).getroot()
    return tree

import words as rvut_words
import definitions as rvut_definitions
import make_kondratjev
import make_wells
import parse_vip
import re

import contextlib

@contextlib.contextmanager
def make_gen_accumulator():
    lst = []
    def add(gen):
        res = gen.__enter__()
        lst.append(gen)
        
        return res
    yield add
    
    for gen in lst:
        gen.__exit__(None, None, None)

def find_kap_words(kap_parent):
    lst = []
    for word in rvut_words.get_words_from_kap(kap_parent.find("kap")):
        # запятая влечет пустой элемент
        # disting ... <var><kap><tld/>indulo</kap></var>,
        if word:
            lst.append(word)
    return lst
    

def for_drv_words_headwords(tree):
    # ec.html - <drv> povas esti en <subart> ankaŭ
    #for drv in tree.iterfind("art/drv"):
    for drv in tree.iterfind("art//drv"):
        yield drv, find_kap_words(drv)
        
    for subart in tree.iterfind("art//subart"):
        if subart.find(".//drv") is None:
            # konsideras, ke subart mem estas kavazaŭ drv
            yield subart, find_kap_words(subart.getparent())
    

def calc_words(headwords):
    lst = []
    def on_word(word):
        lst.append(word)
    for word in headwords:
        make_kondratjev.with_x_hdw(word, on_word)
    return lst

# http://stackoverflow.com/a/480227
def preserve_unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def gen_trans_text(lang, snc_dct, numerator_func, translations, final_sep):
    tr_lst = []

    # baza traduko
    drv_tr = translations.get(lang)
    if drv_tr:
        tr_lst.append(", ".join(drv_tr))

    # precizigantoj
    snc_lst = []
    snc_tr  = preserve_unique(snc_dct.get(lang, []))
    if len(snc_tr) == 1:
        snc_lst.append(snc_tr[0])
    else:
        for i, tr in enumerate(snc_tr):
            snc_lst.append("%(numerator_func(i))s %(tr)s" % s_.EvalFormat())
    if snc_lst:
        tr_lst.append(" ".join(snc_lst))

    tr_txt = final_sep.join(tr_lst)
    # :TRICKY: estas jena traduko:
    # hazardi ...
    # <trd lng="ru"></trd>
    #assert tr_txt
    return tr_txt

import s_
import itertools
import flatten as rvut_flatten
import copy

def main():
    dct_prefix = "/home/ilya/.stardict/dic/esperanto"
    dst_fname = o_p.join(dct_prefix, "REVO_Eksplika/Eksplika-REVO.txt")
    
    # :REFACTOR:
    dirname = os.path.dirname
    # :REFACTOR: realpath() - apliki tion al ĉiuj uzoj
    prj_fdir = dirname(os.path.realpath(__file__))
    import shutil
    def copy_prj_fname(prj_fname, dst_fpath):
        o_p.force_makedirs(os.path.dirname(dst_fpath))
        shutil.copy(o_p.join(prj_fdir, prj_fname), dst_fpath)
    
    prefix_eoru = dirname(dirname(prj_fdir))
    unpacked_revo = o_p.join(prefix_eoru, "stuff/revo/revo")

    dictionaries = {}
    with make_gen_accumulator() as add_gen:
        def create_dictionary(dst_fname, css_link=None):
            remove_srcfile = True # False # 
            on_article = add_gen(make_kondratjev.dictionary_generator(dst_fname, css_text=None, is_html=True, remove_srcfile=remove_srcfile))
            if css_link:
                orig_on_article = on_article
                def on_article(key_names, txt):
                    css_link
                    txt = """<link href="%(css_link)s" rel="stylesheet" type="text/css" />%(txt)s""" % locals()
                    return orig_on_article(key_names, txt)
            return on_article
        on_explika_article = create_dictionary(dst_fname, "revo.css")
        
        res_fdir = o_p.join(dirname(dst_fname), "res")
        copy_prj_fname("sample/revo/revo.css", o_p.join(res_fdir, "revo.css"))
        # kopias figurojn por beleco
        dst_smb = o_p.join(res_fdir, "smb")
        if not o_p.exists(dst_smb):
            shutil.copytree(o_p.join(unpacked_revo, "smb"), dst_smb)

        xml_fpath = o_p.join(unpacked_revo, "xml")
        def open_xml_article(xml_fname):
            xml_fname = o_p.join(xml_fpath, xml_fname)
            tree = open_xml_tree(xml_fname)
            return tree
        
        def fname2prefix(src_fname):
            return o_p.without_ext(src_fname)
        
        prefix_dct = {}
        def get_words(prefix):
            words = prefix_dct.get(prefix)
            if words is None:
                
                words = prefix_dct[prefix] = []
                tree = open_xml_article(prefix + ".xml")

                for drv, headwords in for_drv_words_headwords(tree):
                    words.extend(calc_words(headwords))

                    #print(words)
                    #print(rvut_definitions.get_translations(drv).get("de"))
                    #print()
                    
            return words
        
        fname_lst = os.listdir(xml_fpath)
        if False: # True: # 
            fname_lst = [
                "ten.xml", 
                "distin.xml",
                "apenau.xml", # <trd> in <subdrv>
                "pri.xml",    # artikolo sen <drv>
                "sur.xml",    # <ekz> ne en <(sub)snc>, sed en <subart>
                "al.xml",     # <trdgrp> ĝuste en <art>
                "stift.xml",  # kaj <ekz> ankaŭ en <art>
                
                "lima.xml", # перевод относился к <kap>, хотя был внутри текста (гад с 'la') - и таких статей много
                
                "kverk.xml",  # diversaj homaj eraroj
                "jxak1.xml",
                
                "anim.xml",   # <ekz> sen <ind>
                "blank.xml",  #
                
                "milv.xml",   # <bld> anstataŭ <>ekz
                
                "hel.xml",    # trdgrp en <dif>
                "hazard.xml", # malplena trd etikedo
                "iks.xml",    # vortoj kun signo '|'
            ]
        
        for src_fname in fname_lst:
            prefix = fname2prefix(src_fname)
            all_names = get_words(prefix)
                    
            html_fname = o_p.join(unpacked_revo, "art", prefix + ".html")
            body = make_wells.get_html_body(html_fname, False)
            
            h1 = body.find("h1")
            hr = body.find("hr")
            
            div = etree.Element("div")
            el = h1.getnext()
            while el != hr:
                div.append(el)
                el = h1.getnext()
                
            def append_sub(name):
                sub_el = body.find("div[@class='%(name)s']" % locals())
                if not(sub_el is None):
                    div.append(etree.Element("hr"))
                    div.append(sub_el)
                    
            append_sub("fontoj")
            append_sub("notoj")
            
            # renovigas referencojn en stilo 
            # kapt.html#kapt.0i => bword://kapti#kapt.0i
            for lnk in parse_vip.iter_tags(div, "a"):
                href = lnk.get("href")
                if href:
                    m = re.match(r"(?P<lnk_fname>[^/]+\.html)#(?P<anchor>.+)$", href)
                    if m:
                        lnk_fname, anchor = m.group("lnk_fname"), m.group("anchor")
                        lnk_word = get_words(fname2prefix(lnk_fname))[0]
                        # GD ne atentas #anchor, ColorDict - eĉ rifuzas sekvi la ligilon
                        #lnk.set("href", "bword://%(lnk_word)s#%(anchor)s" % locals())
                        lnk.set("href", "bword://%(lnk_word)s#%(anchor)s" % locals())

            # :REFACTOR:
            for img in parse_vip.iter_tags(div, "img"):
                src = img.get("src")
                if src:
                    # egala funkciado por Goldendict (GD) k ColorDict (CD)
                    m = re.match(r"^\.\./", src)
                    if m:
                        img.set("src", src[3:])
                
            txt = parse_vip.gen_html_text(div)
            #print(txt)
            on_explika_article(all_names, txt)
            
            # eo-nacia vortaro
            national_dct = {}
            tree = open_xml_article(src_fname)

            def append_translations(translations, src_trs):
                for lang, lst in src_trs.items():
                    translations[lang] = lst + translations.setdefault(lang, [])
         
            used_tr_nodes = {}
            national_headwords = {}
            def get_count_translations(node):
                res = rvut_definitions.get_translations(node)
                # hazard.xml havas malplena tradukojn
                clean_res = {}
                for lang, lst in res.items():
                    lst = list(filter(bool, lst))
                    if lst:
                        clean_res[lang] = lst
                res = clean_res
                
                append_translations(national_headwords, res)
                
                # :REFACTOR:
                for trd in node.findall('trd'):
                    used_tr_nodes[trd] = True

                for trdp in node.findall('trdgrp'):
                    used_tr_nodes[trdp] = True

                    for trd in trdp.findall('trd'):
                        used_tr_nodes[trd] = True
                
                return res
            
            def iterate_translations(translations, sub_node_dct, numerator_func, final_sep):
                for lang in sub_node_dct.keys() | translations.keys():
                    yield lang, gen_trans_text(lang, sub_node_dct, numerator_func, translations, final_sep)
                    
            def notify_node(warning_txt, node):
                print(warning_txt, src_fname, parse_vip.gen_html_text(node))
                    
            # :TRICKY: plej simpla maniero por kalkuki jam traktitajn nodojn
            ekz_node_set = set()
            def find_ekz_translations(ekz_dct, node, flat_translations):
                #for trd in parse_vip.iter_tags(node, "ekz/trd|trdgrp"):
                def trd_iter(ekz_name, name):
                    return parse_vip.iter_tags(node, "%(ekz_name)s/%(name)s" % locals())
                def trd_iters(ekz_name):
                    return trd_iter(ekz_name, "trd"), trd_iter(ekz_name, "trdgrp")
                for trd in itertools.chain(*(trd_iters("ekz") + trd_iters("bld"))):
                    ekz = trd.getparent()
                    
                    if ekz in ekz_node_set:
                        continue
                    else:
                        ekz_node_set.add(ekz)

                    def make_orig_txt(ind_node):
                        return ', '.join(rvut_words.get_words_from_kap(ind_node))
                    
                    ind_node = ekz.find('ind')
                    if ind_node is None:
                        # kalkulas orig_txt mem, kolektante ĉiujn etikedojn ĝis apero de trd aŭ trdgrp
                        # anim.xml:
                        # <ekz>
                        #  <tld/>ita parolado<fnt>K</fnt>,
                        #  <trd lng="hu">lelkes besz&eacute;d</trd>
                        # </ekz>                        
                        ind_node = etree.Element("ind")
                        ind_node.text = ekz.text
                        for child in ekz.getchildren():
                            if child.tag in ["trd", "trdgrp"]:
                                break
                            else:
                                child = copy.deepcopy(child)
                                ind_node.append(child)
                                
                        tree.append(ind_node)
                        orig_txt = make_orig_txt(ind_node)
                        ind_node.getparent().remove(ind_node)
                    else:
                        orig_txt = make_orig_txt(ind_node)
                    
                    for lang, tr_lst in get_count_translations(ekz).items():
                        # :REFACTOR:
                        lst = ekz_dct.setdefault(lang, [])
                        
                        tr_lst = ", ".join(tr_lst)
                        ekz_txt = "<i><b>%(orig_txt)s</b>: %(tr_lst)s</i>" % locals()
                        lst.append(ekz_txt)
                    
                #return
                
                # :TRICKY: iuj <trd> kumulas tradukon mem k indikon de originala nomo (Latina prezipe) =>
                # nur <trd> povas esti tia, ne <trdgrp>, ĉar tio estas perokula etikedo (angla - tag)
                # malĝuste - hel.xml!
                rest_translations = {}
                for trd in parse_vip.iter_tags(node, "trd"):
                    if trd not in used_tr_nodes:
                        par_node = trd.getparent()
                        if par_node.tag == "trdgrp":
                            lang = par_node.get("lng")
                            
                            used_tr_nodes[par_node] = True
                        else:
                            lang = trd.get("lng")
                        
                        foreign_word = rvut_flatten.flatten_node(trd)
                        if foreign_word:
                            # :REFACTOR:
                            rest_translations.setdefault(lang, []).append(foreign_word)
                        # :REFACTOR:
                        used_tr_nodes[trd] = True
                append_translations(flat_translations, rest_translations)
                append_translations(national_headwords, rest_translations)
            
            def append_ekz_translations(dct, ekz_dct):
                # :TRICKY: ke lasi subsnc_dct simplan kaj ne ŝanĝi iterater_translations,
                # do ĵuste aldonas ekzemplojn al lasta ero de subsnc_dct
                for lang, ekz_lst in ekz_dct.items():
                    ekz_txt = "; ".join(ekz_lst)
                    lst = dct.setdefault(lang, [])
                    if lst:
                        lst[-1] += "; " + ekz_txt
                    else:
                        lst.append(ekz_txt)

            def append_national_article(lang, names, txt):
                o_p_article, dst_fname = dictionaries.get(lang, (None, None))
                if o_p_article is None:
                    dict_fpath = o_p.join(dct_prefix, "REVO_%(lang)s" % locals())
                    # :REFACTOR:
                    dst_fname = o_p.join(dict_fpath, "REVO-%(lang)s.txt" % locals())
                    o_p_article = create_dictionary(dst_fname, "revo-traduko.css")
                    dictionaries[lang] = o_p_article, dst_fname
                    
                    copy_prj_fname("sample/revo/eo-nacia/revo-traduko.css", o_p.join(dict_fpath, "res/revo-traduko.css"))
                    
                o_p_article(names, txt)

            def append_row(translations, snc_dct, headwords, drv):
                # sur.xml: <ekz> povas esti ekster ajna <snc>
                ekz_dct = {}
                find_ekz_translations(ekz_dct, drv, translations)
                append_ekz_translations(translations, ekz_dct)
                 
                assert headwords
                hw_txt = "<b>%s</b>" % "</b>, <b>".join(headwords)
                
                typ = None
                vspec = drv.find("gra/vspec")
                if vspec is not None:
                    typ = vspec.text
                    
                if typ:
                    hw_txt = "%(hw_txt)s <i>%(typ)s</i>" % locals()
                
                for lang, tr_txt in iterate_translations(translations, snc_dct, arab_num, " <b>|</b> "):
                    opa_args = national_dct.setdefault(lang, ([], []))
                        
                    names, txt = opa_args
                    names.extend(calc_words(headwords))
                    
                    row_txt = """<div class="paragrafo">%(hw_txt)s %(tr_txt)s</div>""" % locals()
                    txt.append(row_txt)
                    
                    # nacia-eo article
                    n_keywords = national_headwords.get(lang)
                    assert n_keywords
                    # devas purigi poste originalan n_keywords, ne ŝanĝitan
                    #n_keywords = [word.replace("|", "/") for word in n_keywords]
                    clean_keywords = [word.replace("|", "/") for word in n_keywords]
                    append_national_article(lang, clean_keywords, row_txt)
                    n_keywords.clear()

            for drv, headwords in for_drv_words_headwords(tree):
                #print(src_fname)
                #print(translations)
                #print()
                
                def latin_num(i):
                    return "%(chr(ord('a') + i))s)" % s_.EvalFormat()
                snc_dct = {}
                ekz_snc_dct = {}
                for snc in parse_vip.iter_tags(drv, "snc"):
                    subsnc_dct = {}
                    ekz_subsnc_dct = {}
                    for subsnc in parse_vip.iter_tags(snc, "subsnc"):
                        subsnc_translations = get_count_translations(subsnc)
                        for lang, tr_lst in subsnc_translations.items():
                            lst = subsnc_dct.setdefault(lang, [])
                            lst.append(", ".join(tr_lst))
                            
                        find_ekz_translations(ekz_subsnc_dct, subsnc, subsnc_dct)
                        
                    append_ekz_translations(subsnc_dct, ekz_subsnc_dct)
                    for lang, tr_txt in iterate_translations(get_count_translations(snc), subsnc_dct, latin_num, "; "):
                        lst = snc_dct.setdefault(lang, [])
                        lst.append(tr_txt)
                        
                    find_ekz_translations(ekz_snc_dct, snc, snc_dct)
                    
                def arab_num(i):
                    return "<b>%(i+1)s.</b>" % s_.EvalFormat()

                append_ekz_translations(snc_dct, ekz_snc_dct)
                
                def merge_trs(translations, drv):
                    src_trs = get_count_translations(drv)
                    append_translations(translations, src_trs)
                    
                # ankoraŭ estas iome da <subdrv> en <drv> => aldonu
                translations = {}
                for subdrv in parse_vip.iter_tags(drv, "subdrv"):
                    merge_trs(translations, subdrv)
                # k subart ankaŭ eblas havi <trd> ĝuste en subart - sur.xml: hu => rá-
                merge_trs(translations, drv)

                append_row(translations, snc_dct, headwords, drv)

            # :TRICKY: al.xml havas tradukojn ekstere subart, drv
            art_node = tree.find("art")
            append_row(get_count_translations(art_node), {}, find_kap_words(art_node), art_node)
            
            for lang, opa_args in national_dct.items():
                names, txt = opa_args
                append_national_article(lang, names, "".join(txt))
                
            strict_check = False # True # 
            def alarm_not_processed(trd):
                is_ok = trd in used_tr_nodes
                
                if not is_ok:
                    if strict_check:
                        assert is_ok
                    else:
                        notify_node("Not processed trd:", trd.getparent())

            # kontrolo, ke ĉiuj nodoj estas traktita
            for trd in parse_vip.iter_tags(tree, "trd"):
                alarm_not_processed(trd)
            for trd in parse_vip.iter_tags(tree, "trdgrp"):
                alarm_not_processed(trd)
    
    # zip'u vortarojn
    revo_dicts_fpath = o_p.join(dirname(unpacked_revo), "revo-dicts")
    o_p.force_makedirs(revo_dicts_fpath)
    # shutil povas zipfile!
    #import zipfile
        
    print("\nAtingeblaj REVO vortaroj:")
    def zip_dict(dst_fname):
        dir_fname, basename = os.path.split(dst_fname)
        root_dir, dir_fname = os.path.split(dir_fname)
        # alie ne funkcias - t.e. se vortara datumo estas ĝuste en zip, ne en ia dosierujo
        fname = shutil.make_archive(o_p.join(revo_dicts_fpath, dir_fname), "zip", root_dir, base_dir=dir_fname)
        
        ifo_fname = os.path.splitext(dst_fname)[0] + ".ifo"
        with open(ifo_fname) as ifo_f:
            properties = {}
            for line in ifo_f:
                lst = line.split("=")
                if len(lst) >= 2:
                    key, value = lst[0].strip(), lst[1].strip()
                    if key and value:
                        properties[key] = value
        
        words_cnt = int(properties.get("wordcount"))
        synwordcount = properties.get("synwordcount")
        if synwordcount:
            words_cnt +=  int(synwordcount)
        fname = os.path.basename(fname)
        print("http://new.bombono.org/download/revo/%(fname)s\t%(words_cnt)s" % locals())
        
    zip_dict(dst_fname)
    for lang, (func, dst_fname) in dictionaries.items():
        zip_dict(dst_fname)
            

if __name__ == '__main__':
    main()