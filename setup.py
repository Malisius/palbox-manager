from setuptools import find_packages, setup

setup(
    name="palbox-manager",
    version="0.1.0",
    description="A webapp to install and manage your Palworld dedicated server",
    author="Peter Oertel",
    author_email="me@peteroertel.com",
    install_requires=["flask"],
    packages=find_packages(),
    entry_points={
        "console-scripts": ["palbox-manager = manager.__main__:main"]
    },
)
