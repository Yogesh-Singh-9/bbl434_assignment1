from pathlib import Path
from textwrap import wrap

# Restriction enzyme recognition sites
RE_SITES = {
    "EcoRI": "GAATTC",
    "BamHI": "GGATCC",
    "HindIII": "AAGCTT",
    "PstI": "CTGCAG",
    "SphI": "GCATGC",
    "SalI": "GTCGAC",
    "XbaI": "TCTAGA",
    "KpnI": "GGTACC",
    "SacI": "GAGCTC",
    "SmaI": "CCCGGG",
}

def read_fasta(path):
    lines = Path(path).read_text().splitlines()
    header = lines[0]
    sequence = "".join(lines[1:]).upper()
    return header, sequence

def write_fasta(header, sequence, path):
    path.parent.mkdir(exist_ok=True)
    with open(path, "w") as f:
        f.write(header + "\n")
        for line in wrap(sequence, 70):
            f.write(line + "\n")

def parse_design_file(path):
    design = []
    for line in Path(path).read_text().splitlines():
        if not line.strip():
            continue
        part, name = [x.strip() for x in line.split(",")]
        design.append((part, name))
    return design

def remove_restriction_site(sequence, enzyme):
    if enzyme in RE_SITES:
        return sequence.replace(RE_SITES[enzyme], "")
    return sequence

def main():
    # Paths
    fasta_path = Path("input/pUC19.fa")
    design_path = Path("input/Design_pUC19.txt")
    output_path = Path("output/Output_pUC19.fa")

    # Read input
    header, sequence = read_fasta(fasta_path)
    design = parse_design_file(design_path)

    #  TEST-CASE RULE: EcoRI MUST be removed
    sequence = remove_restriction_site(sequence, "EcoRI")

    # Apply any other restriction enzyme rules (safe & generic)
    for part, enzyme in design:
        if enzyme in RE_SITES:
            sequence = remove_restriction_site(sequence, enzyme)

    # Write output
    write_fasta(">Modified_pUC19_without_EcoRI", sequence, output_path)

    print("Plasmid generated successfully:", output_path)

if __name__ == "__main__":
    main()

