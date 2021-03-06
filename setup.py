from setuptools import setup, find_packages

setup(
    name="python-serializable-dataclass",
    version="0.1.0",
    packages=find_packages(exclude=("tests*",)),
    package_data={"lib": ["py.typed"]},
    author="jason",
    author_email="jiahuic@twitter.com",
    description="Easily makes python object as a serializable dataclass",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/tinyHui/python-serializable-dataclass",
    project_urls={"Tracker": "https://github.com/tinyHui/python-serializable-dataclass/issues"},
    license="GNU General Public License v3.0",
    keywords="dataclasses json",
    install_requires=[],
    python_requires=">=3.8",
    extras_require={"dev": ["pytest", "pytest-cov", "mypy", "flake8"]},
    include_package_data=True,
    scripts=["publish.py"],
)
