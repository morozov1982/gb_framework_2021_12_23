from os.path import join
from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка с шаблоном
    :param kwargs: параметры
    :return:
    """
    template_path = join(folder, template_name)

    with open(template_path, 'r', encoding='utf-8') as file:
        template = Template(file.read())

    return template.render(**kwargs)
