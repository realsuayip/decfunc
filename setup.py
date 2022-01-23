import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="decfunc",
    version="1.0.0",
    author="Şuayip Üzülmez",
    author_email="suayip.541@gmail.com",
    description="Creating decorators with arguments made easy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/realsuayip/decfunc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
