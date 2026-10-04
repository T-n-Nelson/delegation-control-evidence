# Development Pilot Protocol 0.1.0

This protocol defines an executed finite synthetic pilot, not a preregistered confirmatory study. Its JSON schedule file was written before the first recorded execution and its hash is pinned in the execution receipt. Development tests preceded the recorded pilot. No publicly preregistered timestamp or external review is claimed.

## Authority and effect contracts

Domain A stores the root authorization epoch and active/revoked state. Domain B stores its local replicated policy and synthetic archive. Each uses a separate SQLite file, created for one execution and closed afterward. A global coordinator event sequence orders this single-host schedule; it is not a distributed causal clock. Events describing effects are appended only after the receiver's archive transaction commits.

Admission snapshot remembers the queue-time permission. Local action check consults B's replicated authority before a new effect. Freshness and barrier additionally consults A over the simulated channel and refuses when freshness is unavailable. An acknowledgment requires observed delivery of the revoked state to B; a timeout cannot create an acknowledgment. Work accepted before revocation can still produce a post-acknowledgment effect under the deliberately weak admission baseline. Acknowledgment alone is therefore not a guarantee in every control.

All controls bind scope to the same synthetic project resource and use durable business-operation identity. Repeating an identical committed operation returns its receipt without another write; conflicting content is rejected. Receipt recovery remains allowed after revocation under this explicit contract. This permission is specific to the synthetic workflow, not a statement about revoked OAuth credentials.

## Inputs and complete census

`protocol.json` defines eight schedules: normal completion, delivered revocation, delayed revocation, revoked partition, authorized partition, lost-response retry, receipt recovery after revocation, and wrong scope. Each is executed under all three controls. No scenario is omitted for failing a desired outcome. There are 24 executions and no stochastic or model sampling.

Primary endpoints distinguish effects after a revocation request from effects after its completed acknowledgment. The former expresses immediate-stop intent; the latter expresses acknowledged-stop behavior. These have different semantics and neither is relabeled to hide a failure.

Legitimate completion eligibility is authored in advance: normal, authorized partition, lost-response retry, and recovery of a pre-revocation effect. Completion requires one durable row with correct synthetic bytes and a receipt. The revoked-before-effect and wrong-scope cases are not counted as legitimate workload successes. False blocking counts an eligible case with no effect and a refusal. An unacknowledged revocation has a null acknowledgment delay; null is not zero.

Duplicate effects, out-of-scope effects, recovered receipts and complete event traces are reported separately. The checker recalculates these endpoints from observations; it cannot attest that the observations were produced by the private runtime. Its durable-row cross-check concerns the exported snapshot, not direct access to the original database.

## Validity and next gates

Counts describe only this complete finite set. No confidence intervals, superiority in a population, hostile-agent resilience, human-oversight effectiveness or production claims are made. Fresh observation and commit have no intervening schedule action in this version. The funded study must explicitly test that gap, concurrent in-flight operations, recovery and mixed authority versions before a stronger distributed claim is possible.

Future model episodes, sample size, provider costs and reserved workloads require a separate protocol freeze. The development pilot must not be pooled with reserved outcomes. The private engine and application are not part of this public package.
