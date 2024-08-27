import logging
from dataclasses import dataclass, field

from openpyxl import load_workbook


def main() -> None:
    file_path = "/Users/ilya/Downloads/Attachments_lunjo@mail.ru_2024-02-06_12-50-17/Sinonimia vortaro.xlsx"  # noqa: E501

    if False:
        import pandas as pd

        df = pd.read_excel(file_path)
        print(df.head())

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

        articles: list[Article] = []
        for sheet in wb.worksheets:
            logging.info(f"processing {sheet.title}...")

            if sheet.title == "Й":
                logging.warning("letter Й is skipped due to different formatting, TODO")
                continue

            content_shift = 0
            if sheet.title in ["В", "Е"]:
                content_shift = 1

            header = True

            class state:
                cur_article = ArticleSource()

            def add_article():
                article = state.cur_article
                state.cur_article = ArticleSource()

                if not article.ru:
                    return
                assert article.eo

                articles.append(Article(src=article))

            for row in sheet.iter_rows():

                for column, cell in enumerate(row, start=1):
                    # if cell.data_type == "n":
                    #    # EmptyCell
                    #    continue

                    content_cln = column - content_shift
                    if content_cln == Column.RU:
                        top_style = cell.border.top.style

                        if header:
                            if not top_style:
                                continue
                            header = False

                        if top_style:
                            if top_style != "medium":
                                logging.warning(
                                    f"unknown border style for article: {top_style}, {cell.coordinate}"
                                )

                            add_article()

                        state.cur_article.ru.append(cell)

                    elif content_cln == Column.EO:
                        state.cur_article.eo.append(cell)
                    elif content_cln == Column.EXAMPLES:
                        state.cur_article.examples.append(cell)
                    elif content_cln == Column.REMARKS:
                        state.cur_article.remarks.append(cell)

            add_article()
            logging.info(f"first article: {articles[0].src.ru[0].value}")
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
