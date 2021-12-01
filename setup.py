import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NetzplanAPP-Sebastian-Meisel",
    version="0.0.1",
    author="Sebastian Meisel",
    author_email="sebastian.meisel@gmail.com",
    description="Netzplan (PM) Online erstellen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SebastianMeisel/NetzplanAPP",
    project_urls={
        "Bug Tracker": "https://github.com/SebastianMeisel/NetzplanAPP/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Framework :: Flask",
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
