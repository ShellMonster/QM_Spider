import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="QM_Spider",
    version="0.0.41",
    author="@道长",
    author_email="ctrlf4@yeah.net",
    license='Apache License 2.0',
    description="QiMai Spider library",
    long_description="QiMai Spider library",
    long_description_content_type="text/markdown",
    url="https://github.com/ShellMonster/QM_Spider",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    # requires = [
    #     'requests',
    #     'datetime',
    #     'pandas',
    #     'numpy',
    #     'scipy',
    #     'pyecharts',
    #     'zmail',
    #     'multiprocess',
    #     'python-dateutil'
    # ],
    install_requires=[
        'requests',
        'datetime',
        'pandas',
        'numpy',
        'scipy',
        'pyecharts',
        'zmail',
        'multiprocess',
        'python-dateutil'
    ]
)

# requires = [
#     'requests >= 2.25.1',
#     'datetime >= 4.3',
#     'pandas >= 1.1.3',
#     'numpy >= 1.19.2',
#     'scipy >= 1.5.2',
#     'pyecharts >= 1.9.0',
#     'zmail >= 0.2.8',
#     'multiprocess >= 0.70.11.1'
# ]
#
# install_requires=[
#     'requests >= 2.25.1',
#     'datetime >= 4.3',
#     'pandas >= 1.1.3',
#     'numpy >= 1.19.2',
#     'scipy >= 1.5.2',
#     'pyecharts >= 1.9.0',
#     'zmail >= 0.2.8',
#     'multiprocess >= 0.70.11.1'
# ]
