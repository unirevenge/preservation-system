from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("requirements-prod.txt") as f:
    requirements_prod = f.read().splitlines()

setup(
    name="cade_system",
    version="6.0.0",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        "prod": requirements_prod,
    },
    entry_points={
        "console_scripts": [
            "cade-init=auto_init_cade:main",
            "cade-run=cade_production:main",
        ],
    },
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "": ["*.json", "*.ini", "*.md"],
    },
)
