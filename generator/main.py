import shutil
from pprint import pprint
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

__current_dir__ = Path().parent.resolve()
__static_dir__ = __current_dir__ / "static"
__root_dir__ = __current_dir__ / "root"
__templates_dir__ = __current_dir__ / "templates"
__output_dir__ = __current_dir__.parent / "docs"
__pages_dir__ = __current_dir__ / "pages"

if __output_dir__.exists():
    shutil.rmtree(__output_dir__)

env = Environment(loader=FileSystemLoader(__templates_dir__, encoding="utf-8"))

BASE_URL = "/n4okins.github.io/docs"


class TemplateFuncTools:
    @staticmethod
    def solve_url(path: str):
        return BASE_URL + path


env.globals.update(
    {
        "solve_url": TemplateFuncTools.solve_url,
    }
)

base_template = env.get_template("base.html")
shutil.copytree(
    __root_dir__, __output_dir__,
    ignore=shutil.ignore_patterns("*.map", "*.scss", "*.ts", "__private*")
)

shutil.copytree(
    __static_dir__, __output_dir__ / "static",
    ignore=shutil.ignore_patterns("*.map", "*.scss", "*.ts", "__private*")
)


class PageObject:
    __ROUTING__ = dict()

    def __init__(self, path, title=None, ):
        self.html = ""
        self.src_path = Path(path)
        self.relative_path = Path(
            "/".join(
                self.src_path.relative_to(__current_dir__).parts[1:]
            )
        )
        self.title = title or (
            self.src_path.stem if self.src_path.stem != "index" else self.src_path.parent.stem
        )

        self.href_path = Path("./") / self.src_path.name
        self.dst_path = __output_dir__ / self.href_path
        self._navigation = f"<a href='{BASE_URL}'><span>/</span></a>"

        self.parents = []

        for p in self.relative_path.parents:
            self.parents.append(p)
            if p == __output_dir__:
                break

        self.depth = len(self.parents) - 1
        self.__ROUTING__[self.relative_path] = self

        (__output_dir__ / self.relative_path).parent.mkdir(exist_ok=True, parents=True)

    def __repr__(self):
        return f"PageObject('\\{self.relative_path}')"

    @property
    def navigation(self):
        paths = list(self.relative_path.parents)
        paths.pop()
        paths.insert(0, self.relative_path)
        paths.reverse()
        for p in paths:
            href = BASE_URL / p
            if href.stem == "index":
                continue
            self._navigation += "<span> » </span>"
            self._navigation += f"<a href='{href}'><span>{href.stem}</span></a>\n"

        return self._navigation

    def render(self, **kwargs):
        with open(self.src_path, "r", encoding="utf-8") as f:
            self.html = Template(source=f.read()).render(**kwargs)
        with open(__output_dir__ / self.relative_path, mode="w", encoding="utf-8") as f:
            f.write(base_template.render(**kwargs))


if __name__ == "__main__":
    others = {
        "BASE_URL": BASE_URL,
        "ROUTING": PageObject.__ROUTING__,
    }
    Index = PageObject(__templates_dir__ / "index.html", title="n4okins")
    Index.render(this=Index)
    page_objects = []

    for html_path in __pages_dir__.glob("**/*.html"):
        page_objects.append(PageObject(html_path))

    for html_path in __root_dir__.glob("**/*.html"):
        page_objects.append(PageObject(html_path, title=" "))

    for pages in page_objects:
        pages.render(this=pages, others=others)

    pprint(PageObject.__ROUTING__)
