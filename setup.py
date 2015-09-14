#!/usr/bin/env python
# coding: utf-8


from setuptools import setup
import os
import re

cur_dir = os.path.dirname(__file__)

# :TRICKY: после установки по умолчанию модули *.py появятся прямо в 
# env/lib/python<VERSION>/site-packages/*.py(c) ; у pip есть режим
# pip install --egg, в этом случае файлы установятся в site-packages/<name=fablib>
# с добавлением соответ. файла .pth
py_modules = []
for fname in os.listdir(os.path.join(cur_dir, 'src')):
    m = re.match("(.*)\.py$", fname)
    if m:
        py_modules.append(m.group(1))
        
setup(
    name = "vkompililo",
    version = 1,

    # лучше пользоваться requirements.txt
    #
    # :KLUGE: только так можно указывать зависимости, что не Pypi,
    # причем вызывать pip install --process-dependency-links;
    # при этом в pip 1.6 убрали это возможность, но вместо нее обещают 
    # https://github.com/pypa/pip/issues/2023#issuecomment-76086349
    #install_requires=["my_ansible==1"],
    #dependency_links=['git+https://github.com/muravjov/ansible.git@stable-1.9#egg=my_ansible-1'],   

    package_dir = {'': 'src'},
    py_modules = py_modules,
)
