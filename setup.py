from setuptools import setup, find_packages

setup(
    name="rnaseq-pipeline",
    version="1.0.0",
    description="RNA-seq analysis pipeline: QC → Trimming → Alignment → Annotation",
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "rnaseq-pipeline=pipeline.pipeline:main",
        ]
    },
)
