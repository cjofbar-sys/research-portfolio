# Public/private research documentation architecture

The public repository `research-portfolio` contains approved scientific summaries, documented outputs and reproducible examples. A separate **private research archive**, managed by the researcher, should preserve evidence records, unpublished formulations, editorial decisions and application dossiers.

## Source-of-truth boundaries

- **Public:** text whose disclosure has been reviewed, verified metadata, reproducible synthetic demonstrations, and approved diagrams.
- **Private:** original Research Studio protocol, detailed claims and their source locations, chronology of intellectual/editorial decisions, private project notes, unpublished manuscripts, confidential referee details and individual application materials.
- **Private project repositories:** independently governed software and study implementations. Reference them from the private archive through stable identifiers; avoid copying whole repositories.
- **Lovable website:** presentation layer for released public claims, linked to stable public documents.

## Proposed private archive

```
research-program-archive/
  README.md
  governance/
    provenance-and-disclosure.md
    editorial-decision-log.md
    scientific-writing-protocol.md
  01-research-corpus/
  02-evidence-register/
  03-intellectual-development/
  04-project-records/
  05-methodological-laboratory/
  06-publications-and-manuscripts/
  07-academic-trajectory/
  08-applications/
    waterloo/
    iast/
    cornell/
  09-collaborations-and-funding/
  10-public-release-queue/
  templates/
  registers/
```

## Record metadata

Each record should have a stable ID, title, document type, relevant research question, source/provenance, date, version or Git commit, owner/contributors, evidentiary status, confidentiality classification, relation to public output, review decision and links to associated records.

A publication transition is explicit: **private working version → verification and disclosure review → approved public text → public commit and site link**. A public revision never erases the private reasoning or source record that supports it.

## Security

GitHub private repository visibility is necessary but not sufficient for highly sensitive information. Do not commit access tokens, passwords, unredacted participant records, sensitive personally identifying information or restricted third-party materials. Use appropriate secure storage for sensitive files, and keep only references and admissible metadata in Git. Git history retains deleted content unless specially rewritten.

This document describes the organization. It does not assert that the private archive has already been created.
