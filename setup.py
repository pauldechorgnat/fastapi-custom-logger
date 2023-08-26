from setuptools import setup

with open("requirements.txt", "r", encoding="utf-8") as file:
    requirements = file.read().split("\n")

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="fastapi-middleware-logger",
    version="0.0.2",
    author="Paul Déchorgnat",
    author_email="paul.dechorgnat@gmail.com",
    url="https://github.com/pauldechorgnat/fastapi-custom-logger",
    description="Simple library to customize logger for FastAPI",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    classifiers=[
        "Framework :: FastAPI",
    ],
)
