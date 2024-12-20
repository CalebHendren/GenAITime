import csv

input_file = "openalex_biology_generative_ai.csv"
output_file = "openalex_biology_generative_ai_filtered.csv"

#Remove preprints and non-peer reviewed publications
excluded_substrings = ["bioRxiv", "medRxiv"]

biology_keywords = [
    "scrna-seq data", "scrnaseq", "bulk rna data", "transcriptomic data", "transcriptomics",
    "single-cell", "single cell", "biomarker discovery", "biomarker selection",
    "synthetic biological data", "synthetic biology", "bioinformatics", "molecular biology",
    "gene networks", "gene network", "protein folding", "protein structure",
    "single-cell research", "single cell research", "genomics", "genome sequencing",
    "proteomics", "metabolomics", "gene expression data", "gene expression",
    "biological sequences", "biological sequence", "protein structure prediction",
    "biological datasets", "dna sequences", "rna sequences", "epigenomics",
    "metagenomics", "transcriptomics", "lipidomics", "glycomics", "nutrigenomics"
]

generative_ai_keywords = [
    "variational autoencoder", "vae", "generative adversarial network", "gan",
    "denoising diffusion model", "ddm", "denoising diffusion probabilistic model", "ddpm",
    "generative models", "generative ai", "diffusion models", "autoencoder", "generative neural networks"
]

with open(input_file, mode="r", newline="", encoding="utf-8") as infile, \
     open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    seen_titles = set()
    for row in reader:
        journal = row.get("Journal", "")
        if any(substring in journal for substring in excluded_substrings):
            continue

        # Remove any duplicates
        title = row.get("Title", "")
        if title in seen_titles:
            continue

        # Check te insure one biology and one generative AI keyword
            # are included in Title OR Abstract
        title_text = row.get("Title", "").lower()
        abstract_text = row.get("Abstract", "").lower()
        combined_text = title_text + " " + abstract_text
        has_biology = any(bio_kw in combined_text for bio_kw in biology_keywords)
        has_ai = any(ai_kw in combined_text for ai_kw in generative_ai_keywords)
        if not (has_biology and has_ai):
        writer.writerow(row)
        seen_titles.add(title)

print(f"Filtering complete. Results saved to {output_file}")
