import os
import re
import runpy
from itertools import chain

from setuptools import find_packages, setup


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OPTIONAL_DEPENDENCIES = ("autograd", "tensorflow", "theano")


def parse_requirements_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.read().splitlines()]


if __name__ == "__main__":
    requirements = parse_requirements_file("requirements/base.txt")

    install_requires = []
    optional_dependencies = {}
    for requirement in requirements:
        # We manually separate hard from optional dependencies.
        if any(requirement.startswith(optional_dependency)
               for optional_dependency in OPTIONAL_DEPENDENCIES):
            package = re.match(r"([A-Za-z0-9\-_]+).*", requirement).group(1)
            optional_dependencies[package] = [requirement]
        else:
            install_requires.append(requirement)

    dev_requirements = parse_requirements_file("requirements/dev.txt")
    extras_require = {
        "test": dev_requirements,
        **optional_dependencies
    }
    extras_require["all"] = list(chain(*extras_require.values()))

    pymanopt = runpy.run_path(
        os.path.join(BASE_DIR, "pymanopt", "__init__.py"))

    with open(os.path.join(BASE_DIR, "README.md")) as f:
        long_description = f.read()

    setup(
        name="pymanopt",
        version=pymanopt["__version__"],
        description=("Toolbox for optimization on manifolds with support for "
                     "automatic differentiation"),
        url="https://pymanopt.org",
        author="Jamie Townsend, Niklas Koep and Sebastian Weichwald",
        license="BSD",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Mathematics",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
        ],
        keywords=("optimization,manifold optimization,"
                  "automatic differentiation,machine learning,numpy,scipy,"
                  "theano,autograd,tensorflow"),
        packages=find_packages(exclude=["tests"]),
        install_requires=install_requires,
        extras_require=extras_require,
        long_description=long_description,
        long_description_content_type="text/markdown",
        data_files=[
            "CONTRIBUTING.md",
            "CONTRIBUTORS",
            "LICENSE",
            "MAINTAINERS",
            "README.md"
        ]
    )
