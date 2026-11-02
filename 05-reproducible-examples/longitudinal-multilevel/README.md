# Longitudinal multilevel research demonstration

**Status:** Public methodological demonstration with simulated observations. No human participants; no empirical findings about any student population.

## Research question

How can a researcher separate changes across repeated observations from variation between students and academic programmes, while preserving the distinction between a measured score and culturally situated processes of making sense of the future?

## Design

The demonstration simulates repeated scores for students nested within programmes. The data-generating process is disclosed in the Python script; all variables are hypothetical. The model is intended to support decisions about nested dependence, repeated measures, uncertainty, missingness and sensitivity, rather than to show that a particular theoretical effect has been discovered.

## Methodological questions

- How should time be represented and centered?
- Do students differ in their initial values and changes across observations?
- What changes when student and programme clustering are ignored?
- How might systematic missingness influence fitted coefficients?
- What diagnostics and sensitivity analyses would make the inference more defensible?

## Interpretive constraints

A score about future orientation does not, by itself, identify the content or meaning of a life project. Cultural-semiotic analysis would require appropriate evidence of practices, experiences, relationships, narratives and contexts, with a documented path between materials and interpretation. Statistical association does not identify a psychological mechanism or a causal effect without additional design assumptions.

## Running

```bash
python -m pip install -r requirements.txt
python analysis.py
```

The analysis prints sample structure, regression estimates, mixed-model estimates, confidence intervals and a missing-data sensitivity comparison. An R counterpart and independently checked numerical parity remain planned; this demonstration does not claim them completed.
