from setuptools import find_packages,setup
from typing import List

hypene_dot="-e ."

def get_requirement(file_path:str)->List[str]:
    requirements=[]
    try:
        with open(file_path) as file_obj:
            requirements=file_obj.readlines()
            requirements=[req.replace('\n','') for req in requirements]
            if hypene_dot in requirements:
                requirements.remove(hypene_dot)
            return requirements      
    except FileNotFoundError:
        print("file does not exist create the file first ")  
    
setup(name="the security porject",
    version="0.0.1",
    author="JOD",
    author_email="tsxmiky24@gamil.com",
    packages=find_packages(),
    install_requires=get_requirement("requirement.txt")
    )
