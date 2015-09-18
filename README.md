# vkompililo

To compile various Esperanto dictionaries to Stardict format. In particular, can
bake such dictionaries as:

- Russian-Esperanto-Russian, Kondratjev: http://eoru.ru
- English-Esperanto-English Dictionary, John C. Wells: [the book at Google Play](https://play.google.com/store/books/details/John_C_Wells_English_Esperanto_English_Dictionary?id=f0Zunqj2fa0C&hl=en)
- Reta Vortaro, REVO: http://www.reta-vortaro.de

## Installation & Use

    $ virtualenv -p python3 vk-env
    $ vk-env/bin/pip install -r https://github.com/muravjov/vkompililo/raw/master/requirements.txt

To compile the Kondtratjev' dictionary:

    $ vk-env/bin/python -m make_kondtratjev src_fdir dst_fdir

To compile the Wells' dictionary  (to ~/.stardict/dic/esperanto):

    $ vk-env/bin/python -m make_wells

To compile REVO (to ~/dic/esperanto/REVO-*):

    $ vk-env/bin/python -m make_revo


## (eo) Kiel instali ReVo en telefonon kun Android

<!---
![Colordict kun REVO](http://new.bombono.org/download/revo/Screenshot_2015-09-16-21-12-34.png =250x)
<img src="" style="width: 50px;"/>
-->
<img alt="Colordict kun REVO" src="http://new.bombono.org/download/revo/Screenshot_2015-09-16-21-12-34.png" width="400">

Ĉiuj dezirantoj povas instali vortarojn de REVO en sia telefonon, kaj uzi ilin pere de aplikoj [Colordict](https://play.google.com/store/apps/details?id=com.socialnmobile.colordict&hl=en) aŭ Goldendict (Android).

Kial tiu versio de la vortaro [ReVo](http://www.reta-vortaro.de/revo/) estas pli bona ol jam ekzistanta apliko [PReVo](https://play.google.com/store/apps/details?id=uk.co.busydoingnothing.prevo&hl=en)?
La avantaĝoj estas jenaj:

- oni povas uzi diversajn vortarojn en Colordict/Goldendict samtempe
  (ne nur Esperantajn vortarojn, sed iu ajn, kiun oni instalis, ekzemple angla-rusa)
- PReVo ne havas tradukojn de ekzemploj, kiu estas en la web-veriso http://www.reta-vortaro.de/revo/ kaj
  en tiu versio; la ekzemplo: teni => teni la vorton: ser fiel a la palabra dada (fr.) (des pli oni ne povas serĉi laŭ ilin)
- ergonomio de PReVo estas ne tiom bona: ŝanĝo de ŝerĉado de na nacia lingvo al Esperanto kaj male estas ne simpla,- 
  devas elekti en la menu ero "Elektu lingvon", elekti la lingvon mem - ĝenerale, bezonas pikadi per fingro en telefonerkanon.

Sube estas donitaj (tunojn de) referencoj al vortaroj, kiun instali? Unue, la eksplika parto de REVO estas apartigita en aparta vortaro, REVO_Eksplika.zip, - tiu ĉi formo estas la sama, kiun havas (N)PIV. La restaj vortaroj estas nacia, ekzemple, REVO_ru.zip estas Esperanto-Rusa-Esperanta "tranĉaĵo" de REVO.

La algoritmo de instalo se vi uzas Colordict, Android estas jena:
- lanĉu ColorDict
- piku la supran dekstran piktogramon-"dosierujon"
- piku denove tien, en la piktogramon-"elŝuti"
- en kampon de enigo "Direct Download" skribu la adreson de bezonata vortaro, ekzemple
  http://new.bombono.org/download/revo/REVO_Eksplika.zip
  (ke ne erari mi kopiis URL el letero de poŝtelefona poŝta kliento)
- premu OK => la vortaro estas ŝarĝigata kaj konektata, povas esti uzata

Se vi havas problemojn pri instalo de vortaroj:
- laŭeble ColorDict indas esti renovigita ĝis versio 4.3.0 (aŭ pli alta)
- se la algoritmo supre ne funkcias, do bezonas elŝuti vortara arkivo al komputilo, malpaki ĝin,
  konekti telefonon al la komputilo kaj transmeti la dosierujon kun la vortaro al la telefono en la dosierujon "dictdata"
- iafoje estas utila indeksi instalitajn vortarojn en la telefono: Settings => Apps => trovu ColorDict en la listo =>
  Force stop & Clear data => relanĉi ColorDict denove
- provu uzi GoldenDict anstataŭ ColorDict

La referencoj al vortaroj REVO estas donitaj sube (dekstren de ilin - nombroj de vortoj en vortaro, ne de artikoloj).

## (en) How to install REVO to phone with Android

Evereone can install REVO dictionaries to phone and use them via apps Goldendict or Colordict (Android).

Why this dictionary version is better than already existsing app [PReVo](https://play.google.com/store/apps/details?id=uk.co.busydoingnothing.prevo&hl=en) ?
Here are the advantages:

- Colordict/Goldendict searches through all installed dictionaries
  (not only through Esperanto ones, but through all that you've installed, for example, English-Russian)
- PReVo doesn't have translations of use cases/phrases, that the web version, http://www.reta-vortaro.de/revo/ and this version has; example: okazo => *okazo kreas ŝteliston: opportunity makes the thief* (moreover, you can't search by them)
- PReVo' usability is weak: search switch from English to Esperanto and back is not simple,- you have to select the menu item "Elektu Lingvon", select language self ... - in general, you have to poke with a finger at the phone screen a little

There are (tons of) links to dictionaries below, what to install? Firstly, the explanatory part of REVO is split off into a separate dictionary, REVO_Eksplika.zip, - it is the same as (N)PIV. Other dictionaries are national, f.e., REVO_en.zip is a  English-Esperanto-English "slice" of REVO.

The algorithm to install for ColorDict, Android is as follows:
- run ColorDict
- press the uppper right "folder" icon
- press over there again, the "download" icon
- input a needed dictionary URL into the entry "Direct Download", for example, 
  http://new.bombono.org/download/revo/REVO_Eksplika.zip
  (not to make a mistake I copied url from a letter of mobile email client)
- press ОК => the dictionary is downloading and being activated, you try to use it

If you have a problem while installing a dictionary:
- when applicable ColorDict should be updated to version 4.3.0 (or higher)
- if the algorithm above doesn't work, then you should download dictionary arсhive manually to computer, unarchieve it,
  connect phone to the computer and transfer the folder with the dictionary to the phone in the folder "dictdata"
- sometimes it's useful to reindex installed dictionaries on the phone: Settings => Apps => find ColorDict in the list =>
  Force stop & Clear data => rerun ColorDict again
- try use GoldenDict instead of ColorDict

Links to REVO dictionaries are below (to the right - word count in a dictionary, not article' count)

## (ru) Как установить REVO на телефон с Android

Все желающие могут установить себе словари REVO, на телефон, и
использовать их с помощью Goldendict или Colordict (Android).

Чем эта версия словарей http://www.reta-vortaro.de/revo/ лучше
уже имеющегося приложения [PReVo](https://play.google.com/store/apps/details?id=uk.co.busydoingnothing.prevo&hl=en) ?
Вот список преимуществ:

- в Colordict/Goldendict поиск идет по всем установленным словарям,
  (и не только E-словарям, а по всем, которые установите, к примеру англо-русский)
- в PReVo нет переводов примеров использования, кои есть в web-версии http://www.reta-vortaro.de/revo/ и
  в данной версии; пример teni => perdi la piedtenon: терять опору (и тем более по ним нельзя искать)
- эргономика у PReVo хромает: переключение поиска с русского на E и назад
  не просто - нужно выбрать пункт в меню Elektu lingvon, выбрать язык - в общем,
  потыкать пальцем в экран придется

Ниже даны (тонны) ссылок на словари, какие ставить? Во-первых, толковая часть REVO выделена в отдельный словарь, REVO_Eksplika.zip, - в таком виде он один-в-один как (N)PIV. Остальные словари - национальные, например,
REVO_ru.zip это эсперанто-русско-эсперантский "срез" REVO.

Алгоритм установки для ColorDict, Android:
- открываем ColorDict
- тыкаем в верхнюю правую иконку-"папку"
- тыкаем туда же в иконку-"скачать"
- в поле ввода Direct Download пишем адрес нужного словаря, например
  http://new.bombono.org/download/revo/REVO_Eksplika.zip
  (чтоб не ошибиться я скопировал url из письма из мобильного почтового клиента на телефоне)
- жмем ОК => словарь загружается и подключается, можно пользоваться

Если возникли проблемы с установкой словарей:
- при возможности версию ColorDict следует обновить до 4.3.0 (или выше)
- если вышеуказанный алгоритм не работает, то нужно вручную закачать архив на компьютер, распаковать его,
  подключить телефон к компьютеру и перенести папку со словарем на телефон в папку dictdata
- иногда полезно переиндексировать установленные словари на телефоне: Настройки => Приложения => найти в списке ColorDict =>
  Остановить & Стереть данные => запустить ColorDict снова
- попробуйте использовать GoldenDict вместо ColorDict

Ссылки на словари REVO даны ниже (справа - число слов в словаре, не статей).

## Referencoj al REVO vortaroj / Links to REVO dictionaries / Ссылки на словари REVO

http://new.bombono.org/download/revo/REVO_Eksplika.zip 32531  
http://new.bombono.org/download/revo/REVO_ru.zip 54845  
http://new.bombono.org/download/revo/REVO_en.zip 38603  
http://new.bombono.org/download/revo/REVO_fr.zip 67785  
http://new.bombono.org/download/revo/REVO_hu.zip 52596  
http://new.bombono.org/download/revo/REVO_de.zip 50836  
http://new.bombono.org/download/revo/REVO_cs.zip 47254  
http://new.bombono.org/download/revo/REVO_nl.zip 41781  
http://new.bombono.org/download/revo/REVO_sk.zip 41678  
http://new.bombono.org/download/revo/REVO_be.zip 38036  
http://new.bombono.org/download/revo/REVO_pl.zip 37533  
http://new.bombono.org/download/revo/REVO_es.zip 27238  
http://new.bombono.org/download/revo/REVO_pt.zip 26927  
http://new.bombono.org/download/revo/REVO_ca.zip 23378  
http://new.bombono.org/download/revo/REVO_vi.zip 5  
http://new.bombono.org/download/revo/REVO_sl.zip 25  
http://new.bombono.org/download/revo/REVO_ka.zip 3  
http://new.bombono.org/download/revo/REVO_ku.zip 200  
http://new.bombono.org/download/revo/REVO_qu.zip 2  
http://new.bombono.org/download/revo/REVO_uk.zip 277  
http://new.bombono.org/download/revo/REVO_kek.zip 107  
http://new.bombono.org/download/revo/REVO_jbo.zip 5  
http://new.bombono.org/download/revo/REVO_ia.zip 33  
http://new.bombono.org/download/revo/REVO_eu.zip 31  
http://new.bombono.org/download/revo/REVO_is.zip 26  
http://new.bombono.org/download/revo/REVO_lv.zip 31  
http://new.bombono.org/download/revo/REVO_sw.zip 48  
http://new.bombono.org/download/revo/REVO_lt.zip 26  
http://new.bombono.org/download/revo/REVO_kk.zip 22  
http://new.bombono.org/download/revo/REVO_fa.zip 7776  
http://new.bombono.org/download/revo/REVO_hr.zip 180  
http://new.bombono.org/download/revo/REVO_lat.zip 353  
http://new.bombono.org/download/revo/REVO_os.zip 27  
http://new.bombono.org/download/revo/REVO_mn.zip 3  
http://new.bombono.org/download/revo/REVO_zh.zip 611  
http://new.bombono.org/download/revo/REVO_el.zip 2448  
http://new.bombono.org/download/revo/REVO_tp.zip 734  
http://new.bombono.org/download/revo/REVO_gd.zip 30  
http://new.bombono.org/download/revo/REVO_to.zip 2  
http://new.bombono.org/download/revo/REVO_mk.zip 49  
http://new.bombono.org/download/revo/REVO_mo.zip 3  
http://new.bombono.org/download/revo/REVO_bg.zip 9008  
http://new.bombono.org/download/revo/REVO_he.zip 2861  
http://new.bombono.org/download/revo/REVO_ro.zip 1217  
http://new.bombono.org/download/revo/REVO_grc.zip 124  
http://new.bombono.org/download/revo/REVO_it.zip 18364  
http://new.bombono.org/download/revo/REVO_af.zip 22  
http://new.bombono.org/download/revo/REVO_ga.zip 3  
http://new.bombono.org/download/revo/REVO_ko.zip 13  
http://new.bombono.org/download/revo/REVO_ja.zip 303  
http://new.bombono.org/download/revo/REVO_ky.zip 2  
http://new.bombono.org/download/revo/REVO_fi.zip 1760  
http://new.bombono.org/download/revo/REVO_id.zip 7790  
http://new.bombono.org/download/revo/REVO_yi.zip 2  
http://new.bombono.org/download/revo/REVO_oc.zip 668  
http://new.bombono.org/download/revo/REVO_br.zip 6950  
http://new.bombono.org/download/revo/REVO_sr.zip 59  
http://new.bombono.org/download/revo/REVO_vo.zip 1019  
http://new.bombono.org/download/revo/REVO_sv.zip 8105  
http://new.bombono.org/download/revo/REVO_gl.zip 15  
http://new.bombono.org/download/revo/REVO_da.zip 185  
http://new.bombono.org/download/revo/REVO_cy.zip 6  
http://new.bombono.org/download/revo/REVO_no.zip 1527  
http://new.bombono.org/download/revo/REVO_iu.zip 2  
http://new.bombono.org/download/revo/REVO_tr.zip 2989  
http://new.bombono.org/download/revo/REVO_ie.zip 4  
http://new.bombono.org/download/revo/REVO_la.zip 4138  
http://new.bombono.org/download/revo/REVO_ar.zip 77  

## (eo) TODO:
- provi usi la dosierujon "res" por ekstera .css
- Wells:
  - remunti la libron, ĉar folioj kun malplena etikedo "title" ne estas vidata en CR
    por lista peto (request) => bezonas konsideri, ke ĉiuj prefikso "afds " havas >= 10 taŭgantojn
  - aldoni serĉado por cx-variantoj
- skribi al aŭtoro de ColorDict pri la malsukcesa serĉado de:
  - "ĉ(argeni)"-vortoj
  - аббревиатура
- uzi "text dictionary file format" anstataŭ tabfile/babylon-text,
  vidu stardict_bin2text k male, TextDictinaryFile por priskribo
  de la formato
- ripari la difinojn de tipo(tipe) (типа) ilustr anstataŭ ilustri, ĉar
  originalo metis ciferon, ekzemple, ilustr<>1</>i

 REVO:
- estas pli bone skribi originalon kun kunteksto, por ekzemploj:
  pri.xml: priŝteli *la mastron* (per griza tiparo)
- aldoni ne artikolojn:
  - bibliografo
  - trezoro
- <bld> povas esti elŝutita de reta-vortaro.de (figuroj)
- kverk.xml: <trd lng="la">Quercus sempervirens</trd> estas ene de <klr> k nun
  ne povas esti trovata => refaru rvut_definitions.get_translations() por tiu kaŭzo
- optimumigo de tempa plenumo: malpligi nombro de malfermoj de dosieroj .xml 
  (malfermi nur po unufoje)
- eo-nacia:
  - indeksi ankaŭ kun ekzemplaj linioj (perdi la piedtenon) 
  - se traduko ne estas for kapvorto, do ne indeksu kun tiu vorto (hazardi, ru)
- por ColorDict laboras tio (ne por Goldendict): referencoj al dok/ povas esti malfermitaj, =>
  ripari ilin (sen ../dok) kaj kopii doc/ dosierujo en res/ ;
  vidu ankaŭ [tiun koncernon](https://groups.yahoo.com/neo/groups/revuloj/conversations/messages/23355)
