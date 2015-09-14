
import os
import o_p

import lxml.html as l_html
from lxml import etree

# :REFACTOR:
def get_html_body(pth, is_xhtml):
    with open(pth) as src_f:
        tree = l_html.parse(src_f, l_html.xhtml_parser if is_xhtml else l_html.html_parser)
        body = tree.getroot().body
    return body

def xhtml_tag(name):
    return "{http://www.w3.org/1999/xhtml}" + name

import parse_vip
import make_kondratjev

def make_wells(first_num, last_num, dst_fname):
    def parse_dictionary(on_parsed_article):
        dirname = os.path.dirname
        prefix_eoru = dirname(dirname(dirname(__file__)))
        unpacked_epub = o_p.join(prefix_eoru, "stuff/Wells/decrypted/depacked")
             
        for num in range(first_num, last_num+1):
            #num = 29 # K
            src_fname = o_p.join(unpacked_epub, "OEBPS/%03d.html" % num)
            body = get_html_body(src_fname, True)
    
            found_empty_p = False
            # альтернативный способ - .getchildren() + проверка .tag
            for p in body.iterfind(xhtml_tag("p")):
                txt = p.text_content().strip()
        
                if found_empty_p and txt:
                    # очередная статья
                    #print(txt)
                    
                    radix = None
                    lst = []
                    def on_word(word):
                        # <b>Kaboverd/o</b><b> </b>Cape Verde
                        if word:
                            lst.append(word)
                     
                    key_elements = list(parse_vip.iter_tags(p, xhtml_tag("b")))
                    assert key_elements
                    
                    for idx, el in enumerate(key_elements):
                        bold_txt = el.text_content().strip()
                        exceptions = [
                            "li diris, ~ ŝi atendas", # ke
                            "~e, ke", # kondiĉo 
                        ]

                        # "2" - kluso
                        def is_number(txt):
                            res = True
                            try:
                                int(txt)
                            except:
                                res = False
                            return res
                        
                        if bold_txt in exceptions or is_number(bold_txt):
                            w_lst = [] # [bold_txt]
                        else:
                            w_lst = [w.strip() for w in bold_txt.split(",")]
                            
                        def remove_bad_suffix(w):
                            for suffix in [
                                ":",  # boarding:
                                " 1", # can 1
                            ]:
                                if w.endswith(suffix):
                                    w = w[:-len(suffix)]
                            return w
        
                        # только первое слово - корень
                        # kost/i, ~o cost; multe~a expensive
                        if radix is None:
                            radix = w_lst[0]
                            slash = radix.find("/")
                            if slash >= 0:
                                radix = radix[:slash]
                                
                            radix = remove_bad_suffix(radix)
        
                        for w in w_lst:
                            for no_tilda_pattern in [
                                "(aerarmea) generalo", # air
                                "koncerne (with accus)", # as
                                "~ on daŭri", # run
                            ]:
                                if idx != 0 and w.find("~") == -1 and txt.find(no_tilda_pattern) != -1:
                                    w = "~ " + w
                            
                            # :TRICKY: некоторые термины содержат " ~ ", но без
                            # ручного анализа правильное значение не подставишь:
                            # - lav/i wash tr; ~ sin get washed, wash (oneself)
                            # - est/i be; ~as (there) is/are; kio ~ al vi? what’s the matter? [skip]
                            w = w.replace("/", "").replace("~", radix)
                            
                            # Kaliforni/o California; ≈o californium
                            change_case = w.find("≈") >= 0
                            if change_case:
                                w = w.replace("≈", radix)
                                # :REFACTOR:
                                w = w[0].swapcase() + w[1:]
                                
                            # digital/o 1 digitalis, foxglove; 2 ~a img2.png digital [= cifereca]
                            if w.startswith("2 "):
                                w = w[2:]
                            w = remove_bad_suffix(w)
                                
                            # Prote/o Proteus; ≈a protean; ≈o 1 protea (flower); 2 olm (amphibian)
                            # errors needs to be fixed by upstream
                            if w in ['a', 'o']:
                                continue
                            
                            if w == 'la' and txt.find("da is not used before la, other") != -1:
                                continue
                            
                            make_kondratjev.with_x_hdw(w, on_word)
                        
                        is_first = False
                    
                    assert lst
                    #print(lst)
                    on_parsed_article(lst, parse_vip.gen_html_text(p)) # txt)
                
                if not txt:
                    found_empty_p = True
    make_kondratjev.make_dictionary_ex(parse_dictionary, dst_fname, css_text=None, is_html=True)

def main():
    prefix = "/home/ilya/.stardict/dic/esperanto"
    make_wells(15, 42, o_p.join(prefix, "wells-eo-en/wells-eo-en.txt"))
    make_wells(44, 69, o_p.join(prefix, "wells-en-eo/wells-eo-en.txt"))

if __name__ == '__main__':
    main()