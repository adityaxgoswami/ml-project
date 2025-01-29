#responsible for creating ml appication into package.. even deploy in PiPy  
from setuptools import find_packages,setup
from typing import List

HYPEN_E='-e .'
def get_requirement(file_path:str)->List:
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[i.replace("\n","") for i in requirements]
        
        if HYPEN_E in requirements:
            requirements.remove(HYPEN_E)
    return requirements
setup(
    name='Ml-project',
    version='0.0.1',
    author='Aditya Goswami',
    author_email='adityagoswami2424@gmail.com',
    packages = find_packages(),
    install_requires=get_requirement('requirement.txt')
)