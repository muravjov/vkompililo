import logging
from dataclasses import dataclass, field
import re

from openpyxl import load_workbook
from openpyxl.cell.rich_text import CellRichText


def strip_name(name: str):
    return name.strip(" .")


ru_syn_pat = re.compile(r"Син.:\s(?P<lst>.*)")


def extract_ru_synonyms(ru_source: str):
    m = ru_syn_pat.search(ru_source)
    if not m:
        return []

    ##lst = re.split(r'[\, ]+', m["lst"])
    lst = []
    for s in re.split(r"[.,]+", m["lst"]):
        s = s.strip()
        if not s:
            continue
        lst.append(s)

    return lst


def main() -> None:
    file_path = "/Users/ilya/Downloads/Attachments_lunjo@mail.ru_2024-02-06_12-50-17/Sinonimia vortaro.xlsx"  # noqa: E501

    if False:
        import pandas as pd

        df = pd.read_excel(file_path)
        print(df.head())

    if False:
        ru_source = "адепт. Син.: апологет,  защитник, ревнитель, заступник, поклонник, поборник, борец,  (фанатичный) приверженец, панегирист, зелот, сторонник, энтузиаст, последователь, пропонент"  # noqa: E501
        print(extract_ru_synonyms(ru_source))

    if True:
        logging.basicConfig(level=logging.INFO)

        engine_kwargs = {
            "read_only": True,
            "data_only": True,
            "keep_links": False,
            "rich_text": True,
        }

        wb = load_workbook(
            file_path,
            **engine_kwargs,
        )

        class Column:
            RU = 2
            EO = 3
            EXAMPLES = 4
            REMARKS = 5

        @dataclass
        class ArticleSource:
            ru: list = field(default_factory=list)
            eo: list = field(default_factory=list)
            examples: list = field(default_factory=list)
            remarks: list = field(default_factory=list)

        @dataclass
        class Article:
            src: ArticleSource
            name: str
            ru_synonyms: list[str]

        articles: list[Article] = []
        for sheet in wb.worksheets:
            logging.info(f"processing {sheet.title}...")
            first_article_index = len(articles)

            if sheet.title == "Й":
                logging.warning("letter Й is skipped due to different formatting, TODO")
                continue

            content_shift = 0
            if sheet.title in ["В", "Е"]:
                content_shift = 1

            class state:
                cur_article = ArticleSource()

            def add_article():
                article = state.cur_article
                state.cur_article = ArticleSource()

                if not article.ru:
                    return
                assert article.eo

                root_cell = article.ru[0]
                value = root_cell.value
                if not value:
                    if value is not None:
                        logging.warning(
                            f"root cell {root_cell.coordinate} has empty name"
                        )

                    for cell in article.ru:
                        if cell.value:
                            logging.warning(
                                f"root cell {root_cell.coordinate} has empty name and not empty content {cell.value}"
                            )
                            break

                    return

                if isinstance(value, CellRichText):
                    name = str(value[0])
                elif isinstance(value, str):
                    name = value
                else:
                    name = str(value)
                    logging.warning(
                        f"unknown cell content type: {root_cell.coordinate}, {name}"
                    )

                if not name:
                    logging.warning(
                        f"root cell {root_cell.coordinate} has empty name as string"
                    )
                    return

                name = strip_name(name)
                if not name:
                    logging.warning(
                        f"root cell {root_cell.coordinate} has whitespaces in name only"
                    )
                    return

                # *
                ru_synonyms = extract_ru_synonyms(str(value))

                articles.append(
                    Article(src=article, name=name, ru_synonyms=ru_synonyms)
                )

            for row in sheet.iter_rows(min_row=2):

                article_end = False
                for column, cell in enumerate(row, start=1):
                    content_cln = column - content_shift
                    if content_cln == Column.RU:
                        top_style = cell.border.top.style

                        if top_style:
                            if top_style != "medium":
                                logging.warning(
                                    f"unknown border style for article: {top_style}, {cell.coordinate}"
                                )

                            add_article()

                        state.cur_article.ru.append(cell)

                        bottom_style = cell.border.bottom.style
                        if bottom_style:
                            if bottom_style != "medium":
                                logging.warning(
                                    f"unknown border style for article: {bottom_style}, {cell.coordinate}"
                                )

                            article_end = True

                    elif content_cln == Column.EO:
                        state.cur_article.eo.append(cell)
                    elif content_cln == Column.EXAMPLES:
                        state.cur_article.examples.append(cell)
                    elif content_cln == Column.REMARKS:
                        state.cur_article.remarks.append(cell)

                if article_end:
                    add_article()

            add_article()

            if first_article_index == len(articles):
                logging.warning("no articles added for the sheet")
            else:
                logging.info(
                    f"first article: {articles[first_article_index].src.ru[0].value}"
                )
                logging.info(f"last article: {articles[-1].src.ru[0].value}")

        logging.info(f"total: {len(articles)}")

    if False:
        engine_kwargs = {
            "read_only": True,
            "data_only": True,
            "keep_links": False,
            "rich_text": True,
        }

        wb = load_workbook(
            file_path,
            **engine_kwargs,
        )

        ##pprint.pprint([ws.title for ws in wb.worksheets])

        # for sheet in wb.worksheets:
        #    print(sheet.title)

        sheet = None  # type: ignore
        for sh in wb.worksheets:
            if sh.title == "А":
                sheet = sh
                break

        assert sheet
        ##print(sheet)

        # article start vs. not
        b2 = None
        b3 = None
        # eo keys
        c270 = None

        for row in sheet.iter_rows():
            ##print(row)
            for cell in row:
                if cell.data_type == "n":
                    # EmptyCell
                    continue

                if cell.coordinate == "B2":
                    b2 = cell
                if cell.coordinate == "B3":
                    b3 = cell
                if cell.coordinate == "C270":
                    c270 = cell

                print(f"{cell.coordinate}={cell.value}", end="\t")

            print()

        print(b2, b3, c270)


if __name__ == "__main__":
    main()
