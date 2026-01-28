# bbl434_assignment1

A small Python utility that assembles a simple plasmid construct from three inputs: an input FASTA sequence, a design file, and a marker database. The script locates an approximate origin of replication using GC skew, then concatenates the chosen origin fragment, restriction sites, and marker sequences into an output FASTA.

**Files**
- [main.py](main.py): Program that reads inputs and generates the plasmid FASTA.
- `input/` : sample inputs are provided (e.g. `pUC19.fa`, `Design_pUC19.txt`, `markers.tab`).
- `output/` : output FASTA(s) will be written here.

**Usage**
Run the script with three command-line arguments:

```bash
python main.py <input_fasta> <design_txt> <markers_tab>
```

Example using the provided samples:

```bash
python main.py input/pUC19.fa input/Design_pUC19.txt input/markers.tab
```

The script will write the assembled plasmid to `output/universal_plasmid.fa` and print the ORI position and final plasmid size. The FASTA header is `>Universal_Plasmid_Construct` and sequence lines are wrapped to 70 characters.

**Design file format (`Design.txt`)**
- Plain text, one entry per line, comma-separated: `Label, Name`.
- Empty lines or lines without a comma are ignored.
- If the `Label` contains the substring `site` (case-insensitive), the parser treats the `Name` as a restriction enzyme and appends its recognition sequence. Otherwise the `Name` is treated as a marker/feature and the corresponding marker sequence is appended.
- Whitespace around fields is trimmed.

Example lines from a design file:

```
BamHI_site, BamHI
AmpR_gene, Ampicillin
lacZ_alpha, Blue_White_Selection
```

**Marker database format (`markers.tab`)**
- The script expects a pipe-separated table. It skips header lines containing `Category` or `---`.
- It reads at least 4 columns; a short marker name is taken from column 3 (first word) and the description from column 4.

**Supported restriction enzymes (recognized names in `main.py`)**
- EcoRI, BamHI, HindIII, PstI, SphI, SalI, XbaI, KpnI, SacI, SmaI, NotI

**Supported marker names (as present in `main.py`)**
- Ampicillin, Kanamycin, Chloramphenicol, Blue_White_Selection

**Notes & recommendations**
- The script requires exactly three positional arguments; calling `python main.py` without arguments will print a usage message and exit.
- The ORI detection uses a simple cumulative GC-skew scan and returns the index of the minimal skew point (an estimate, not a precise annotation).
- Unknown enzyme or marker names found in the design file are silently ignored. If you prefer strict validation, I can add explicit warnings or failures.
- The output FASTA is wrapped to 70 characters per line and uses the header `>Universal_Plasmid_Construct`.

**Possible improvements**
- Add explicit validation and user-friendly error messages for unknown names.
- Allow specifying output filename via an optional argument.
- Make ORI window size configurable and/or annotate the assembled plasmid with feature positions.

If you want, I can implement any of the improvements above (wrap-length change, validation, output filename option). Tell me which you'd like.
