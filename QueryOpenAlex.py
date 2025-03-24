import csv
from diophila import OpenAlex

email = "YOUR EMAIL HERE"
openalex = OpenAlex(email)

biology_keywords = [
    "scRNA-seq data", "scRNAseq", "bulk RNA data", "transcriptomic data", "transcriptomics",
    "single-cell", "single cell", "biomarker discovery", "biomarker selection",
    "synthetic biological data", "synthetic biology", "bioinformatics", "molecular biology",
    "gene networks", "gene network", "protein folding", "protein structure",
    "single-cell research", "single cell research", "genomics", "genome sequencing",
    "proteomics", "metabolomics", "gene expression data", "gene expression",
    "biological sequences", "biological sequence", "protein structure prediction",
    "biological datasets", "DNA sequences", "RNA sequences", "epigenomics",
    "metagenomics", "transcriptomics", "lipidomics", "glycomics", "nutrigenomics"
]

generative_ai_keywords = [
    "Variational Autoencoder", "VAE", "Generative Adversarial Network", "GAN",
    "Denoising diffusion model", "DDM", "Denoising Diffusion Probabilistic Model", "DDPM",
    "Generative Models", "Generative AI", "Diffusion Models", "Autoencoder", "Generative neural networks"
]

output_file = "openalex_biology_generative_ai.csv"
fieldnames = ["Title", "Journal", "Year", "Abstract", "Cited By Count", "URL", "DOI"]

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over keywords
    for bio_kw in biology_keywords:
        for ai_kw in generative_ai_keywords:
            search_query = f'"{bio_kw}" "{ai_kw}"'
            filters = {
                "from_publication_date": "2015-01-01"
            }

            works = openalex.get_list_of_works(search=search_query, filters=filters)
            for page in works:
                for work in page['results']:
                    abstract_index = work.get("abstract_inverted_index", {})
                    if abstract_index:
                        position_word_pairs = []
                        for word, positions in abstract_index.items():
                            for pos in positions:
                                position_word_pairs.append((pos, word))
                        position_word_pairs.sort(key=lambda x: x[0])
                        abstract = " ".join(word for _, word in position_word_pairs)
                    else:
                        abstract = "N/A"
                    journal = work.get("host_venue", {}).get("display_name")
                    if not journal:
                        primary_location = work.get("primary_location", {})
                        source = primary_location.get("source") if primary_location else {}
                        if source is None:
                            source = {}
                        journal = source.get("display_name", "N/A")
                    writer.writerow({
                        "Title": work.get("display_name", "N/A"),
                        "Journal": journal,
                        "Year": work.get("publication_year", "N/A"),
                        "Abstract": abstract,
                        "Cited By Count": work.get("cited_by_count", 0),
                        "URL": work.get("id", "N/A"),
                        "DOI": work.get("ids", {}).get("doi", "N/A")
                    })

print(f"Query complete. Results saved to {output_file}")
