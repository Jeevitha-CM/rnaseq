# 🧬 RNA-seq Analysis Pipeline

[![CI](https://github.com/YOUR_USERNAME/rnaseq-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/rnaseq-pipeline/actions)
[![Python](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A reproducible, end-to-end **RNA-seq analysis pipeline** written in Python.  
Given paired-end FASTQ files, it runs every stage automatically and produces
gene-level count matrices ready for downstream differential expression analysis.

---

## Pipeline Overview

```
Raw FASTQ
   │
   ▼
[Stage 1]  FastQC          → Raw quality report
   │
   ▼
[Stage 2]  Trim Galore     → Adapter & quality trimming
   │
   ▼
[Stage 2b] FastQC          → Post-trim quality report
   │
   ▼
[Stage 3]  STAR            → Splice-aware alignment → sorted BAM
   │
   ▼
[Stage 4]  featureCounts   → Gene-level counts TSV
   │
   ▼
[Stage 5]  Report          → HTML summary + merged count matrix
```

---

## Requirements

### System tools (must be in `$PATH`)

| Tool | Purpose | Install |
|------|---------|---------|
| [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) | Quality control | `conda install -c bioconda fastqc` |
| [Trim Galore](https://github.com/FelixKrueger/TrimGalore) | Adapter trimming | `conda install -c bioconda trim-galore` |
| [STAR](https://github.com/alexdobin/STAR) | Read alignment | `conda install -c bioconda star` |
| [SAMtools](http://www.htslib.org/) | BAM processing | `conda install -c bioconda samtools` |
| [featureCounts](https://subread.sourceforge.net/) | Quantification | `conda install -c bioconda subread` |

> **Tip:** Install all at once with conda:
> ```bash
> conda create -n rnaseq -c bioconda fastqc trim-galore star samtools subread python=3.11
> conda activate rnaseq
> ```

### Python package

```bash
git clone https://github.com/YOUR_USERNAME/rnaseq-pipeline.git
cd rnaseq-pipeline
pip install -e .
pip install -r requirements.txt
```

---

## Input File Structure

Place paired-end FASTQ files in a directory following this naming convention:

```
data/raw/
├── sample1_R1.fastq.gz
├── sample1_R2.fastq.gz
├── sample2_R1.fastq.gz
└── sample2_R2.fastq.gz
```

The pipeline auto-discovers all `*_R1.fastq.gz` / `*_R2.fastq.gz` pairs.

---

## Running the Pipeline

```bash
rnaseq-pipeline \
  --input  data/raw/ \
  --output results/ \
  --genome /path/to/STAR_genome_index/ \
  --gtf    /path/to/genes.gtf \
  --threads 8
```

Or via Python:

```python
from pipeline import run_pipeline

run_pipeline(
    input_dir  = "data/raw/",
    output_dir = "results/",
    genome     = "/path/to/STAR_genome_index/",
    gtf        = "/path/to/genes.gtf",
    threads    = 8,
)
```

---

## Output Structure

```
results/
├── 01_raw_qc/
│   └── <sample>/          # FastQC HTML + ZIP reports (raw reads)
├── 02_trimmed/
│   └── <sample>/          # Trimmed FASTQ + Trim Galore reports
├── 02b_posttrim_qc/
│   └── <sample>/          # FastQC HTML + ZIP reports (trimmed reads)
├── 03_alignment/
│   └── <sample>/
│       ├── Aligned.sortedByCoord.out.bam
│       ├── Aligned.sortedByCoord.out.bam.bai
│       └── Log.final.out
├── 04_counts/
│   └── <sample>/
│       ├── counts.txt          # Raw featureCounts output
│       └── counts_clean.tsv    # Clean gene_id / count TSV
└── 05_report/
    ├── report.html             # Interactive HTML summary
    └── merged_counts.tsv       # All samples × all genes matrix
```

---

## Building a STAR Genome Index

If you don't have a pre-built index:

```bash
STAR \
  --runMode genomeGenerate \
  --genomeDir /path/to/STAR_genome_index \
  --genomeFastaFiles /path/to/genome.fa \
  --sjdbGTFfile /path/to/genes.gtf \
  --runThreadN 8
```

---

## Running Tests

```bash
pytest tests/ -v --cov=pipeline
```

All tests use mocking — no bioinformatics tools required to run the test suite.

---

## GitHub Actions CI

The workflow (`.github/workflows/ci.yml`) runs automatically on every push and pull request:

| Job | What it checks |
|-----|---------------|
| `lint` | flake8, black, isort |
| `test` | pytest on Python 3.9 / 3.10 / 3.11 with coverage |
| `integration-dry-run` | End-to-end mock run |
| `release` | Draft GitHub Release on merge to `main` |

---

## Connecting to GitHub

```bash
# 1. Initialise the repo
git init
git add .
git commit -m "feat: initial RNA-seq pipeline"

# 2. Create a repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/rnaseq-pipeline.git
git branch -M main
git push -u origin main

# 3. Open a PR → CI runs automatically!
```

---

## Project Structure

```
rnaseq_pipeline/
├── pipeline/
│   ├── __init__.py
│   ├── pipeline.py      # Orchestrator + CLI entry point
│   ├── qc.py            # FastQC wrapper
│   ├── trimming.py      # Trim Galore wrapper
│   ├── alignment.py     # STAR + SAMtools wrapper
│   ├── annotation.py    # featureCounts wrapper + matrix merge
│   └── report.py        # HTML report generator
├── tests/
│   └── test_pipeline.py # Unit tests (all mocked)
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI/CD
├── data/
│   ├── raw/             # Input FASTQ files (gitignored)
│   └── results/         # Pipeline output (gitignored)
├── logs/                # Run logs (gitignored)
├── requirements.txt
├── setup.py
└── README.md
```

---

## License

MIT © 2024
