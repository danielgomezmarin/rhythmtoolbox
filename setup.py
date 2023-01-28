from setuptools import find_packages, setup

test_requires = ["pytest", "pytest-cov"]

setup(
    name="rhythmtoolbox",
    author="danielgomezmarin",
    version="0.1.0",
    url="https://github.com/danielgomezmarin/rhythmtoolbox",
    packages=find_packages(),
    extras_require={
        "test": test_requires,
    },
)
