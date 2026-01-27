# bbl434_assignment1

A small Python utility to assemble a simple plasmid sequence from biological parts (origin of replication, restriction sites, a user gene, and antibiotic markers).

**Files**
- [main.py](main.py): Program that reads inputs and generates the plasmid FASTA.
- [input/Input.fa](input/Input.fa): Input gene sequence in FASTA format (single entry expected).
- [input/Design.txt](input/Design.txt): Design specification listing cloning sites and antibiotic markers (comma-separated).
- [output/Output.fa](output/Output.fa): Generated plasmid FASTA output.

**Quick start**
1. Ensure you have Python 3 installed.
2. Place your gene in `input/Input.fa` (FASTA header then sequence).
3. Edit `input/Design.txt` to list cloning sites and antibiotic markers, one per line, using the format `Label, Name`.
4. Run:

```bash
python main.py
```

The script writes the assembled plasmid to `output/Output.fa` with header `>Universal_Plasmid`.

**Design.txt format**
- Lines beginning with `*` or empty lines are ignored.
- Use labels containing `Multiple_Cloning` to indicate restriction enzymes, e.g. `Multiple_Cloning_Site1, EcoRI`.
- Use labels containing `Antibiotic_marker` for antibiotics, e.g. `Antibiotic_marker1, Ampicillin`.
- Supported restriction names (mapped in `main.py`): `EcoRI`, `BamHI`, `HindIII`, `XhoI`.
- Supported antibiotics (mapped in `main.py`): `Ampicillin`, `Kanamycin`, `Chloramphenicol`.

**Notes & recommendations**
- The output FASTA is written as a single long sequence line; many tools prefer wrapped lines (e.g., 60 chars). Consider adding wrapping if needed.
- `main.py` currently concatenates all FASTA entries if multiple are present — use a single-entry FASTA for the gene, or modify `read_fasta` for multi-entry support.
- Unknown enzyme or antibiotic names are silently ignored; add validation if you want explicit errors.

**Example**
- `input/Input.fa`:

```text
>GeneX
ATGAAACCCGGGTTTAAACCCGGGTTT
```

- `input/Design.txt`:

```text
Multiple_Cloning_Site1, EcoRI
Multiple_Cloning_Site2, BamHI
Antibiotic_marker1, Ampicillin
Antibiotic_marker2, Kanamycin
```

Running `python main.py` will produce `output/Output.fa` with the assembled sequence.

If you want, I can: wrap the FASTA output to 60 chars per line, add validation for `Design.txt`, or update `read_fasta` to return a specific entry — tell me which change you'd prefer.
