from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', static_url='/static/', **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param folder: папка с шаблоном
    :param static_url: путь к статике
    :param kwargs: параметры
    :return:
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    env.globals['static'] = static_url
    template = env.get_template(template_name)
    return template.render(**kwargs)
