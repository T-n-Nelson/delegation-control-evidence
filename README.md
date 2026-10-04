# Delegation Control Across Separate Authority Domains

Nelson Trasatti, independent researcher with interests and expertise across several technical fields, including cybersecurity, and a specialization in agentic AI. My current research focuses on AI agents and artificial intelligence.

An executed **deterministic synthetic development pilot**, dated 4 October 2026. Eight authored schedules were executed under three controls using two separate SQLite authority stores per execution. There were **24 executions, zero model calls and no production effects**. These cases are a finite engineering demonstration, not independent model tasks, a reserved scientific campaign or a safety certification.

| Control | Effects after revocation request | Effects after acknowledged revocation | Legitimate completions |
|---|---:|---:|---:|
| Admission snapshot | 3 | 1 | 4/4 |
| Local action-time check | 2 | 0 | 4/4 |
| Freshness gate and barrier | 0 | 0 | 3/4 |

The freshness condition refuses an authorized operation while the authority channel is unavailable. This availability loss is retained. In all conditions a receipt for a previously committed operation can be recovered after revocation without creating another effect. No duplicate or out-of-scope effect occurred in these selected cases.

## Inspect and verify

Download this repository and run with Python 3.10 or newer, without installing packages:

```text
python verify.py
```

The checker reads local files only. It checks file hashes, case/condition coverage, recorded event ordering, correspondence between effects and exported durable rows, receipt references, and independently recalculates the metrics. It imports no private runtime, uses no model, and makes no network call.

The repository's `.gitattributes` preserves exact file bytes on Windows and other systems. Do not apply automatic line-ending conversion or format the evidence files before verification.

`protocol.json` contains every synthetic input and schedule. `runs.json` contains complete exported observations and events for all 24 executions. `results.json` contains aggregate counts. `execution.json` identifies the protocol and private runner hashes and execution times. `manifest.json` covers every public file except itself.

## Boundaries

This package supports **saved-evidence verification**, not independent reproduction of the private runtime. The experiment runner, proprietary testbed engine, orchestration and integrations are not included. Hashes establish consistency with this package; they do not authenticate authorship, attest the original database or prove security. The checker is a separate implementation within the same project, not an external scientific replication.

The stores run on one trusted host in a sequential controlled schedule. Transport availability is simulated. Synchronous freshness observation and commit are indivisible at the schedule level: the prototype does **not** qualify a network check-to-commit race, concurrent effects, process crashes, malicious hosts, cryptographic delegation or real organizational federation. The third condition combines fresh authority observation with explicit revocation acknowledgment; its result cannot be attributed to a barrier alone. The schedules were authored for development, not sampled from a deployment population. Delay is measured in event steps, not network latency.

## Related work and next study

This extends the engineering question in Conserving Delegated Authority, a bounded empirical working paper with model-generated plans and a shared authority journal. It does not replace or inflate that study's results. The proposed next study would investigate concurrent cross-domain effects, explicit revocation contracts, model-dependent plans and legitimate completion under delayed messages. That campaign has not been run.

Individual FG-TIDA contributions: [UC4](https://github.com/FG-TIDA/use-cases/issues/4), [Theme 13 mapping](https://github.com/FG-TIDA/themes/issues/13#issuecomment-5900725441), [Theme 16 mapping](https://github.com/FG-TIDA/themes/issues/16#issuecomment-5900748338). These links identify contributions and collaborators; they do not imply endorsement by the ITU or ownership of other participants' work. No collaborator materials are redistributed here.

## Rights

Copyright 2026 Nelson Trasatti. No license is granted over the proprietary runtime. This initial evidence release has no general open-source license; viewing public code does not itself grant broader reuse rights. A public checker can be run locally to inspect the supplied evidence. A broader redistribution/modification license remains to be selected by the owner.
