import setuptools

with open("cdkinit/README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="cdk",
    version="0.0.1",
    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "cdk"},
    packages=setuptools.find_packages(where="cdk"),
    install_requires=[
        "aws-cdk.core==1.63.0",
    ],
    python_requires=">=3.6",
    classifiers=[],
)
