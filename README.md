# Requirements Quality Factor Ontology Structure and Content

[![GitHub](https://img.shields.io/github/license/JulianFrattini/rqfo-data)](./LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6583690.svg)](https://doi.org/10.5281/zenodo.6583690)
[![Pytest](https://github.com/JulianFrattini/rqfo-data/actions/workflows/pytest.yml/badge.svg)](https://github.com/JulianFrattini/rqfo-data/actions/workflows/pytest.yml)

## Summary of Artifact

This artifact contains both the structure and the content of the requirements quality factor ontology. A quality factor is a normative metric which maps a textual requirement of a specific granularity to a scale which informs about the quality of this input. We attempt to harmonize the perspective on requirements quality factors and gather established factors, related data sets, and automatic detection approaches in this repository. The ontology was first proposed in our paper ["A Live Extensible Ontology of Quality Factors for Textual Requirements"](https://arxiv.org/abs/2206.05959) at the requirements engineering conference.

## Contributors Information

| Name                         | Affiliation                              | Email                             |
| ---------------------------- | ---------------------------------------- | --------------------------------- |
| Julian Frattini              | Blekinge Institute of Technology, Sweden | julian.frattini@bth.se            |
| Lloyd Montgomery             | University of Hamburg, Germany           | lloyd.montgomery@uni-hamburg.de   |
| Jannik Fischbach             | University of Cologne, Germany           | jannik.fischbach@netlight.com     |
| Dr. Michael Unterkalmsteiner | Blekinge Institute of Technology, Sweden | michael.unterkalmsteiner@bth.se   |
| Prof. Daniel Mendez          | Blekinge Institute of Technology, Sweden | daniel.mendez@bth.se              |
| Dr. Davide Fucci             | Blekinge Institute of Technology, Sweden | davide.fucci@bth.se               |

How to cite this artifact: Frattini, J., Montgomery, L., Fischbach, J., Unterkalmsteiner, M., Mendez, D., & Fucci, D. (2022, August). A Live Extensible Ontology of Quality Factors for Textual Requirements. In 2022 IEEE 30th International Requirements Engineering Conference (RE). IEEE.

## Description of Artifact

The artifact is composed of the following elements:

* `extractions` contains all json files representing an extraction. Each extraction refers to exactly one publication and lists all quality factors, descriptions, data sets, and approaches extracted from that publication according to the extraction guidelines.
* `structure` contains the json files that represent the structure of the ontology. Each file represents one of the contained taxonomies. The structure files are located in subfolders named after their major (ox) and minor (tx) version.
* `versions` contains all json version files. A version has an identifier, date, and associates each included publication to its most recent extraction.
* `checkconformity.py` detects all violations of extractions against the ontology structure which it is associated to.
* `contributors.json` lists all collaborators who have contributed at least one extraction.

## Versioning

The ontology has an identifier of the structure `v<major>.<minor>.<content>`. The respective ids will be incremented as follows:

* `ontology`: if a taxonomy contained in the ontology is added or removed
* `taxonomy`: if a taxonomy contained in the ontology is changed (i.e., dimensions or characteristics added or removed)
* `content`: if an extraction is added

## Related Resources

An interactive visualization of the data contained in this repository can be accessed at http://www.reqfactoront.com

We maintain a list of permanently available snapshots of the ontology:

* v1.0.0 (Aug'22): https://doi.org/10.5281/zenodo.6583690