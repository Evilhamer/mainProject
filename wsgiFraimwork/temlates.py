from jinja2 import Template , FileSystemLoader
from jinja2.environment import Environment
import os


def render(template_name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    tmp = env.get_template(template_name)
    return tmp.render(**kwargs)





    """
    :param template_name: имя шаблона
    :param folder: папка с шаблонами
    :param kwargs: параметры
    :return:
    """

    # file_path = os.path.join(folder, template_name)
    #
    # with open(file_path, encoding='utf-8') as f:
    #     template = Template(f.read())
    # return template.render(**kwargs)
