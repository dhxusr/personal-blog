"""
main functions.

- create_article.

- delete_article.

- edit_article.
"""

from pathlib import Path
import json


MAIN_PATH = Path("pages")
ADMIN_PATH = MAIN_PATH / "admin"
ARTICLES_PATH = MAIN_PATH / "articles"
ADMIN_PAGE = ADMIN_PATH / "index.html"
GUEST_PAGE = MAIN_PATH / "index.html"

def add_line(article: str, number: str) -> None:

    # lines to add in the home page every time an article is created
    ADMIN_LINE = f"""\t        <li  class="article">
                    <h2><a href="/pages/articles/{number}.json">{article}</a></h2>
                    <div class="button">
                        <form action="edit/{number}.json" method="get" style="display:inline;">
                            <button type="submit" class="delete-button">
                                Edit
                            </button>
                        </form>
                        <form action="delete/{number}.json" method="post" style="display:inline;">
                            <button type="submit" class="delete-button">
                                Delete
                            </button>
                        </form>
                    </div>
                </li>
    """
    GUEST_LINE = f"""\t        <li class="article">
                    <h2><a href="/pages/articles/{number}.json">{article}</a></h2>
                </li>
    """
    files = [
        # file to edit for admins
        {"path": ADMIN_PAGE, "line_to_add": ADMIN_LINE},
        # file to edit for guess
        {"path": ADMIN_PAGE, "line_to_add": GUEST_LINE},
    ]

    for file in files:

        home_path = file["path"]
        new = home_path.with_name("new.html")  # new file for rewrite the home page

        with open(new, "w") as new_file:
            with open(home_path, "r") as hfile:

                for line in hfile.readlines():
                    new_file.write(line)
                    if (
                        '<ul class="article_list">' in line
                    ):  # beginning of the list of articles
                        new_file.write(file["line_to_add"])

        home_path.unlink()  # deleting the old file
        new = new.rename(new.with_name("index.html"))


def remove_line(article_title: str, number: str | int) -> None:

    article_line = (
        f'<h2><a href="/pages/articles/{number}.json">{article_title}</a></h2>'
    )
    files = [ADMIN_PAGE, GUEST_PAGE]

    for home_file in files:

        with open(home_file, "r") as hfile:
            lines = hfile.readlines()

        # getting the article's line index
        article_index = None
        for idx, line in enumerate(lines):
            if article_line in line:
                article_index = idx - 1  # backwards one position where the <li> begins
                break

        if article_index is not None:
            lines_to_remove = 15 if home_file is files[0] else 3
            for i in range(lines_to_remove):
                lines.pop(article_index)

        with open(home_file, "w") as page:
            page.writelines(lines)


def _get_articles(title=False) -> list | tuple:

    if not isinstance(title, (bool, str)):
        title = False

    articles = []
    for file in ARTICLES_PATH.iterdir():

        with open(file, "r") as article_file:
            article = json.load(article_file)

            if not title:
                articles.append((article, file.name))

            elif title == True:
                articles.append(article["title"])

            else:
                if article["title"] == title:
                    return (article, file.name)

    return articles


def create_article(article: dict):

    articles = _get_articles(title=True)
    article_number = len(articles) + 1
    article_file = ARTICLES_PATH / f"{article_number}.json"

    while article_file.exists():
        article_number += 1
        article_file = article_file.with_name(f"{article_number}.json")

    while article["title"] in articles:
        title_number = articles.count(article["title"]) + 1
        article["title"] = f"{article['title']} {title_number}"

    with open(article_file, "w") as _file:
        json.dump(article, _file, indent=4)

    title = article["title"]
    add_line(title, article_number)


def delete_article(article_file: str):

    path = ARTICLES_PATH / article_file

    with open(path, "r") as _file:
        title = json.load(_file)["title"]

    number = path.stem
    path.unlink()
    remove_line(title, number)


def edit_page(article_file: str) -> bytes:

    edit_page = ADMIN_PATH / "edit.html"
    article_file = ARTICLES_PATH / article_file

    # getting article's content
    with open(article_file, "r") as _file:
        article = json.load(_file)

    title = article["title"]
    date = article["date"]
    content = article["content"]

    lines_group = [
        # old
        # new
        # form lines
        ("<form>", f'\t    <form action="{article_file.name}" method="post">\n'),
        # title lines
        (
            '<input type="text" id="title" name="title" required>',
            f'\t\t<input type="text" id="title" name="title" required value="{title}">\n',
        ),
        # date lines
        (
            '<input type="date" id="date" name="date" required>',
            f'\t\t<input type="date" id="date" name="date" required value="{date}">\n',
        ),
        # content lines
        (
            '<textarea id="content" name="content" required></textarea>',
            f'\t\t<textarea id="content" name="content" required>{content}</textarea>\n',
        ),
    ]

    with open(edit_page, "rb") as page:
        lines = page.readlines()

    grp_idx = 0
    for idx, line in enumerate(lines):

        bline = bytes(lines_group[grp_idx][0], "UTF-8")
        if bline in line:
            lines[idx] = bytes(lines_group[grp_idx][1], "UTF-8")
            grp_idx = 0 if grp_idx == 3 else grp_idx + 1

    return lines


def edit_article(article: dict, file: str):

    if not isinstance(article, dict):
        raise TypeError(
            f"Error: invalid argument of type: {type(article)} must ba 'dict'."
        )

    if not isinstance(file, (str)):
        raise TypeError(f"Error: invalid argument of type: {type(file)} must be 'str'.")

    # getting the old title to search it in home pages
    with open(ARTICLES_PATH / file, "r") as article_file:
        old_title = json.load(article_file)["title"]

    # applying changes to the article's file
    with open(ARTICLES_PATH / file, "w") as article_file:
        json.dump(article, article_file, indent=4)

    # editing the title in the home page if changed
    if old_title != article["title"]:

        line_to_edit = [
            f'<h2><a href="/pages/articles/{file}.json">{old_title}</a></h2>',
            f'\t\t    <h2><a href="/pages/articles/{file}">{article["title"]}</a></h2>\n',
        ]

        home_pages = [ADMIN_PAGE, GUEST_PAGE]

        # editing the home page
        for page in home_pages:

            # getting lines
            with open(page, "r") as hpage:
                lines = hpage.readlines()

            # searching the corresponding line
            for idx, line in enumerate(lines):
                if line_to_edit[0] in line:
                    lines[idx] = line_to_edit[1]

            # applying change
            with open(page, "w") as hpage:
                hpage.writelines(lines)


def show_article(article_file: Path) -> bytes:

    with open(article_file, "r") as _file:
        article = json.load(_file)

    text = [
        bytes(f'          <p class="content">{line}\n</p>\n', "UTF-8")
        for line in article["content"].split("\n")
    ]

    lines_to_add = [
        bytes(f'    <div class="article">\n', "UTF-8"),
        bytes(f'        <h1>{article["title"]}</h1>\n', "UTF-8"),
        bytes(f'        <div class="date">{article["date"]}</div>\n', "UTF-8"),
        bytes(f'        <div class="content">\n', "UTF-8"),
        bytes(f"        </div>\n", "UTF-8"),
        bytes(f"    </div>\n", "UTF-8"),
    ]

    lines_to_add[:4] += text

    lines = []
    with open(MAIN_PATH / "showsrc.html", "rb") as src:

        for line in src.readlines():
            lines.append(line)

            if bytes("<body>", "UTF-8") in line:
                lines += lines_to_add

    return lines


if __name__ == "__main__":
    pass
