from jinja2 import Template
import os


def render(template_name, folder='template', **kwargs):
    file = os.path.join(folder, template_name)
    with open(file, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
