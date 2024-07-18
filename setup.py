## python3 setup.py bdist_wheel
## python3 -m twine upload dist/* 
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='xrdpy',
     author="Badal Mondal",
     author_email="badalmondal.chembgc@gmail.com",
     maintainer="Pietro Pampili",
     maintainer_email="badalmondal.chembgc@gmail.com",
     description="xrdpy: Python package for 2D X-ray diffraction data analysis",
     long_description=long_description,
     long_description_content_type="text/markdown",
     install_requires=['numpy', 'scipy>= 1.0', 'matplotlib'],
     url="https://github.com/XRDmapAnalysis/xrdpy",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
         "Operating System :: OS Independent",
     ],
 )
