import sys

# -------------------------
# Default biological parts
# -------------------------

ORIGIN_OF_REPLICATION = "ATGCGTACGATCGATCGATCGATCGATCG"

ANTIBIOTIC_GENES = {
    "Ampicillin": "ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTG",
    "Kanamycin": "ATGGATTACAAGGATGACGACGATAAGTAGCGTTGCGG",
    "Chloramphenicol": "ATGGAGAAAAAAATCACTGGATATACCACCGTTGATATATCC"
}

RESTRICTION_SITES = {
    "EcoRI": "GAATTC",
    "BamHI": "GGATCC",
    "HindIII": "AAGCTT",
    "XhoI": "CTCGAG"
}

# -------------------------
# Helper functions
# -------------------------

def read_fasta(filename):
    seq = ""
    with open(filename, "r") as f:
        for line in f:
            if not line.startswith(">"):
                seq += line.strip()
    return seq


def read_design(filename):
    cloning_sites = []
    antibiotics = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("*"):
                continue

            left, right = line.split(",")

            left = left.strip()
            right = right.strip()

            if "Multiple_Cloning" in left:
                cloning_sites.append(right)
            elif "Antibiotic_marker" in left:
                antibiotics.append(right)

    return cloning_sites, antibiotics


def build_mcs(enzyme_list):
    mcs = ""
    for enzyme in enzyme_list:
        if enzyme in RESTRICTION_SITES:
            mcs += RESTRICTION_SITES[enzyme]
    return mcs


def build_antibiotic_region(antibiotics):
    region = ""
    for drug in antibiotics:
        if drug in ANTIBIOTIC_GENES:
            region += ANTIBIOTIC_GENES[drug]
    return region


# -------------------------
# Main logic
# -------------------------

def main():
    input_fasta = "input/Input.fa"
    design_file = "input/Design.txt"
    output_fasta = "output/Output.fa"

    gene_sequence = read_fasta(input_fasta)
    cloning_sites, antibiotics = read_design(design_file)

    mcs = build_mcs(cloning_sites)
    antibiotic_region = build_antibiotic_region(antibiotics)

    plasmid = ORIGIN_OF_REPLICATION + mcs + gene_sequence + antibiotic_region

    with open(output_fasta, "w") as f:
        f.write(">Universal_Plasmid\n")
        f.write(plasmid + "\n")

    print("✅ Plasmid successfully generated: output/Output.fa")


if __name__ == "__main__":
    main()
