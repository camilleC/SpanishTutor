from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="spanish-tutor",
    version="0.1.0",
    author="Camille Ciancanelli",
    author_email="your.email@example.com",  # Update this with your email
    description="An AI-powered Spanish language tutor that adapts to your proficiency level",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/camilleC/SpanishTutor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3", #It is written with Python 3
        "Programming Language :: Python :: 3.8", # Known to work with these versions
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ], 
    python_requires=">=3.8",  # Prevents incompatible install
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "spanish-tutor=spanish_tutor.src.main:main",
        ],
    },
) 