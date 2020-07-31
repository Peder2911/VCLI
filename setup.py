
from setuptools import setup,find_packages
setup(
        name="vcli",
        version="0.0.1",
        install_requires=["fire>=0.3.1"],
        author="Peder G. Landsverk",
        author_email="pglandsverk@gmail.com",
        packages=find_packages(),
        scripts=["bin/views"]
)
