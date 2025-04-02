from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="egxpy",
    version="1.1.0",
    packages=["egxpy"],
    url="https://github.com/omar-Abouyoussef/egxpy",
    project_urls={
        "Web App": "https://egxpy-lab.streamlit.app/",
        "Source": "https://github.com/omar-Abouyoussef/egxpy",
        "Tracker": "https://github.com/omar-Abouyoussef/egxpy/issues",
    },
    license="MIT License",
    author="@omar-Abouyoussef",
    author_email="o.abouyoussef73@gmail.com",
    description="Historical Data And Portfolio Optimization For EGX",
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[
        "setuptools",
        "pandas",
        "numpy",
        "datetime",
        "holidays",
        "retry",
        "git+https://github.com/rongardF/tvdatafeed.git"
        "scipy"
    ],
)
