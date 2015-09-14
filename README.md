# vkompililo

:TODO:

## Installation

    $ pip install -r https://github.com/muravjov/vkompililo/raw/master/requirements.txt

## TODO:
- provi usi la dosierujon "res" por ekstera .css
- Wells:
  - remunti la libron, ĉar folioj kun malplena etikedo "title" ne estas vidata en CR
    por lista peto (request) => bezonas konsideri, ke ĉiuj prefikso "afds " havas >= 10 taŭgantojn
- skribi al aŭtoro de ColorDict pri la malsukcesa serĉado de:
  - "ĉ(argeni)"-vortoj
  - аббревиатура
- uzi "text dictionary file format" anstataŭ tabfile/babylon-text,
  vidu stardict_bin2text k male, TextDictinaryFile por priskribo
  de la formato
- ripari la difinojn de tipo(tipe) (типа) ilustr anstataŭ ilustri, ĉar
  originalo metis ciferon, ekzemple, ilustr<>1</>i

 REVO:
- kverk.xml: <trd lng="la">Quercus sempervirens</trd> estas ene de <klr> k nun
  ne povas esti trovata => refaru rvut_definitions.get_translations() por tiu kaŭzo
- optimumigo de tempa plenumo: malpligi nombro de malfermoj de dosieroj .xml 
  (malfermi nur po unufoje)
- eo-nacia:
  - indeksi ankaŭ kun ekzemplaj linioj (perdi la piedtenon) 
  - se traduko ne estas for kapvorto, do ne indeksu kun tiu vorto (hazardi, ru)
- por ColorDict laboras tio (ne por Goldendict): referencoj al dok/ povas esti malfermitaj, =>
  ripari ilin (sen ../dok) kaj kopii doc/ dosierujo en res/
