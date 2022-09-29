from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path

import shutil

__current_dir__ = Path(__file__).parent.resolve()
__static_dir__ = __current_dir__ / "static"
__templates_dir__ = __current_dir__ / "templates"
__output_dir__ = __current_dir__.parent / "docs"

if __output_dir__.exists():
    shutil.rmtree(__output_dir__)
__output_dir__.mkdir(parents=True)


class PageObject:
    def __init__(self, template: Template, **kwargs):
        self._meta = kwargs
        self._template: Template = template

    def render_html(self, to_path: Path):
        assert to_path.suffix != "html", f"{str(to_path.resolve())} suffix is not HTML."

        with open(to_path, mode="w", encoding="utf-8") as f:
            f.write(self._template.render())


env = Environment(loader=FileSystemLoader(__templates_dir__, encoding="utf-8"))


class TemplateFuncTools:
    @staticmethod
    def url(path: str):
        return path

    @staticmethod
    def insert_html(html_path: str):
        with open(html_path, "r") as f:
            html_raw = f.read()
        return html_raw


env.globals.update(
    {
        "url": TemplateFuncTools.url,
        "insert_html": TemplateFuncTools.insert_html
    }
)

base_template = env.get_template("base.html")
base_page = PageObject(base_template)

shutil.copytree(__static_dir__, __output_dir__ / "static")

if __name__ == "__main__":
    base_page.render_html(__output_dir__ / "index.html")
