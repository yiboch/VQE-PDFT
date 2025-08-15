# VQE-PDFT: Quantum-Classical Hybrid Framework for Complex Correlated Systems

&#x20;

This repository contains the computational code supporting the research paper:

"Integrating Quantum Computing with Multiconfiguration Pair-Density Functional Theory for Biological Electron Transfer"

## Overview

This codebase implements VQE-PDFT, a hybrid quantum-classical method that integrates variational quantum eigensolver with multiconfiguration pair-density functional theory (MC-PDFT).

## Repository Structure

```
├── patches/
│   ├── ash_diff.patch          # Modifications to ASH package (VQE-PDFT interface)
│   └── tencirchem_diff.patch   # Modifications to TenCirChem (empirical HEA circuits)
└── src/
    ├── CT7_benchmark/           # CT7/04 dataset validation
    │   ├── eval_dissociation_ct7.py
    │   └── mol_all/            # Test molecules (7 charge-transfer complexes)
    ├── four_point/              # Four-point electron transfer calculations
    │   ├── example_2071/       # ErCRY4 protein snapshot 2071
    │   └── singlepoint_main.py
    └── geom_opt/                # Geometry optimization for four-point method
        ├── geomopt.py
        └── system_all.xml

```

## Code Organization

### Software Modifications

* ASH package: Interface implementation for VQE-PDFT integration

* TenCirChem package: Empirical hardware-efficient ansatz (HEA) circuit implementation

### Benchmark Validation

* CT7_benchmark/: VQE-PDFT validation on the Charge-Transfer CT7/04 dataset

* mol_all/: Seven molecular systems for dissociation energy calculations

### Biological Application

* four_point/: Four-point method implementation for electron transfer rate calculations

* example_2071/: Representative protein configuration from MD simulation (snapshot frame 2071)

* geom_opt/: Geometry optimization procedures for four-point calculations

## Dependencies

* ASH (commit: bdf9c89)

* TenCirChem (version: 2024.10)

Apply the provided patch files to integrate VQE-PDFT functionality.

* Python 3.9+

## Usage Notes

* example_2071/ represents one of 20 protein conformation analyzed in the article

* Complete dataset and additional snapshots are available as described in the Supplementary Information

* The four-point method calculates electron transfer parameters for biological systems using QM/MM multiscale approach

## License

This project is licensed under the MIT License. See LICENSE for details.

Third-party software modifications are documented in the patch files and comply with original licensing terms.
