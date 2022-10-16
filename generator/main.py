import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

__current_dir__ = Path().parent.resolve()
__static_dir__ = __current_dir__ / "static"
__templates_dir__ = __current_dir__ / "templates"
__output_dir__ = __current_dir__.parent / "docs"
__pages_dir__ = __current_dir__ / "pages"

if __output_dir__.exists():
    shutil.rmtree(__output_dir__)
__output_dir__.mkdir(parents=True)

env = Environment(loader=FileSystemLoader(__templates_dir__, encoding="utf-8"))


class TemplateFuncTools:
    @staticmethod
    def solve_url(path: str):
        return path

    @staticmethod
    def path_navbar(html_path: str):
        return (
                "<a href='./'><span>Home</span></a>" +
                "<span>»</span>" +
                f"<a href='./{html_path}'><span>Portfolio</span></a>"
        )


env.globals.update(
    {
        "solve_url": TemplateFuncTools.solve_url,
    }
)

base_template = env.get_template("base.html")

shutil.copytree(
    __static_dir__, __output_dir__ / "static",
    ignore=shutil.ignore_patterns("*.map", "*.scss", "*.ts", "__private*")
)

shutil.copytree(
    __pages_dir__, __output_dir__ / "pages",
    ignore=shutil.ignore_patterns("*.map", "*.scss", "*.ts", "__private*")
)


class PageObject:
    def __init__(self, path):
        self.src_path = Path(path)
        self.title = self.src_path.stem

        with open(self.src_path, "r", encoding="utf-8") as f:
            self.html = f.read()

        self.dst_path = __output_dir__ / self.src_path.name

    def render(self):
        with open(self.dst_path, mode="w", encoding="utf-8") as f:
            f.write(base_template.render(page=self))


if __name__ == "__main__":
    Index = PageObject(__pages_dir__ / "index.html")
    Index.render()
    for html_path in __pages_dir__.glob("*.html"):
        PageObject(html_path).render()


