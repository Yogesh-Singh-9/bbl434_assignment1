import sys
import os

# ---------- FASTA sequence loader ----------
def load_fasta_sequence(fasta_path):
    dna = []
    with open(fasta_path, "r") as fh:
        for line in fh:
            if not line.startswith(">"):
                dna.append(line.strip().upper())
    return "".join(dna)


# ---------- Origin of replication detection using GC skew ----------
def detect_ori_by_gc_skew(dna_seq):
    cumulative = 0
    skew_track = []

    for nt in dna_seq:
        if nt == "G":
            cumulative += 1
        elif nt == "C":
            cumulative -= 1
        skew_track.append(cumulative)

    return skew_track.index(min(skew_track))


# ---------- Read design rules ----------
def parse_design_file(design_path):
    enzyme_list = []
    marker_list = []

    with open(design_path, "r") as fh:
        for row in fh:
            row = row.strip()
            if not row or "," not in row:
                continue

            key, value = [x.strip() for x in row.split(",")]

            if "site" in key.lower():
                enzyme_list.append(value)
            else:
                marker_list.append(value)

    return enzyme_list, marker_list


# ---------- Marker database reader ----------
def load_marker_database(tab_path):
    marker_db = {}

    with open(tab_path, "r") as fh:
        for row in fh:
            row = row.strip()
            if not row or "|" not in row or "Category" in row or "---" in row:
                continue

            columns = [c.strip() for c in row.split("|")]
            if len(columns) >= 4:
                short_name = columns[2].split()[0]
                description = columns[3]
                marker_db[short_name] = description

    return marker_db


# ---------- Reference sequences ----------
RESTRICTION_SITES = {
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
    "NotI": "GCGGCCGC"
}

MARKER_SEQUENCES = {
    "Ampicillin": "ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTG",
    "Kanamycin": "ATGAGCCATATTCAACGGGAAACGTCTTGCTCGAGGCC",
    "Chloramphenicol": "ATGGAGAAAAAAATCACTGGATATACCACCGTTGATATATCC",
    "Blue_White_Selection": "ATGACCATGATTACGCCAAGCTTGCATGCCTGCAGGTCGAC"
}


# ---------- Main execution ----------
if len(sys.argv) != 4:
    print("Usage: python main.py Input.fa Design.txt markers.tab")
    sys.exit(1)

input_fasta, design_txt, marker_tab = sys.argv[1:4]

# Read genome
genome_seq = load_fasta_sequence(input_fasta)

# Locate ORI
ori_pos = detect_ori_by_gc_skew(genome_seq)
ori_fragment = genome_seq[max(0, ori_pos - 500): min(len(genome_seq), ori_pos + 500)]

# Interpret design instructions
chosen_enzymes, chosen_markers = parse_design_file(design_txt)
marker_info = load_marker_database(marker_tab)

# Assemble plasmid
plasmid_seq = ori_fragment

for enzyme in chosen_enzymes:
    if enzyme in RESTRICTION_SITES:
        plasmid_seq += RESTRICTION_SITES[enzyme]

for marker in chosen_markers:
    if marker in MARKER_SEQUENCES:
        plasmid_seq += MARKER_SEQUENCES[marker]

# ---------- Write FASTA output ----------
os.makedirs("output", exist_ok=True)
output_file = os.path.join("output", "universal_plasmid.fa")

with open(output_file, "w") as out:
    out.write(">Universal_Plasmid_Construct\n")
    for i in range(0, len(plasmid_seq), 70):
        out.write(plasmid_seq[i:i+70] + "\n")

print("FASTA file created successfully")
print("ORI position:", ori_pos)
print("Final plasmid size:", len(plasmid_seq), "bp")
print("Output file:", output_file)

