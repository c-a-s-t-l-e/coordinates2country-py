from setuptools import setup, find_packages

setup(
    name="coordinates2country",
    version="1.0.9",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'coordinates2country': ['resources/*'],
    },
    install_requires=[
        'Pillow',  # For image processing
    ],
    author="Abram Astle",
    author_email="castle676767@gmail.com",
    description="Fast reverse geocoding without internet connection",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/coordinates2country-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
