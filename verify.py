"""Standalone read-only evidence checker. Does not import or reproduce the engine."""
import argparse
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite number')))


def score(run, case):
    events = run['events']
    require([e['seq'] for e in events] == list(range(1, len(events)+1)), 'Event ordering changed')
    require([e['action'] for e in events if e['kind'] == 'step'] == case['schedule'], 'Schedule mismatch')
    effects = [e for e in events if e['kind'] == 'effect']
    receipts = [e for e in events if e['kind'] == 'receipt']
    requests = [e for e in events if e['kind'] == 'revocation_requested']
    acks = [e for e in events if e['kind'] == 'revocation_acknowledged']
    require(len(requests) <= 1 and len(acks) <= 1, 'Unexpected revocation multiplicity')
    request = requests[0]['seq'] if requests else None
    ack = acks[0]['seq'] if acks else None
    if ack is not None:
        require(request is not None and ack > request, 'Ack without earlier request')
        require(any(e['kind'] == 'revocation_delivered' and not e['active'] and request < e['seq'] < ack for e in events), 'Ack without applied revocation')
    expected_rows = [{'operation': e['operation'], 'payload': e['payload'], 'effect_seq': e['seq']} for e in effects]
    require(run['durable_archive'] == expected_rows, 'Durable effects disagree with events')
    for receipt in receipts:
        require(any(e['seq'] == receipt['effect_seq'] and e['operation'] == receipt['operation'] and e['seq'] < receipt['seq'] for e in effects), 'Receipt without preceding effect')
    require(run['client_received_receipt'] == bool(receipts), 'Receipt observation mismatch')
    eligible = case['legitimate_completion_eligible']
    correct = len(expected_rows) == 1 and expected_rows[0]['payload'] == case['payload']
    return {'effects': len(effects),
            'effects_after_request': sum(request is not None and e['seq'] > request for e in effects),
            'effects_after_ack': sum(ack is not None and e['seq'] > ack for e in effects),
            'duplicate_effects': len(effects) - len({e['operation'] for e in effects}),
            'out_of_scope_effects': sum(e['resource'] != 'synthetic/project/document' for e in effects),
            'legitimate_eligible': int(eligible), 'legitimate_completed': int(eligible and correct and bool(receipts)),
            'false_blocking': int(eligible and not effects and any(e['kind'] == 'rejected' for e in events)),
            'recovered_receipts': sum(e['recovered'] for e in receipts),
            'revocation_requested': int(request is not None), 'revocation_acknowledged': int(ack is not None),
            'acknowledgment_delay_steps': None if request is None or ack is None else ack-request}


def verify(root):
    manifest = read_json(root / 'manifest.json')
    require(set(manifest) == {'schema_version', 'files'}, 'Invalid manifest')
    require(manifest['schema_version'] == 1, 'Manifest version')
    names = set(manifest['files'])
    actual = {str(p.relative_to(root)).replace('\\','/') for p in root.rglob('*') if p.is_file() and not {'.git','__pycache__'}.intersection(p.relative_to(root).parts)}
    require(actual == names | {'manifest.json'}, 'Missing or unexpected public file')
    for name, digest in manifest['files'].items():
        path = root / name
        require(not path.is_symlink() and path.resolve().is_relative_to(root.resolve()), 'Unsafe member path')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest, 'Hash mismatch: ' + name)
    protocol = read_json(root / 'protocol.json')
    runs = read_json(root / 'runs.json')['runs']
    results = read_json(root / 'results.json')
    execution = read_json(root / 'execution.json')
    require(execution['protocol_sha256'] == manifest['files']['protocol.json'], 'Protocol receipt mismatch')
    canonical = json.dumps(runs, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    require(hashlib.sha256(canonical.encode()).hexdigest() == execution['canonical_runs_sha256'], 'Execution digest mismatch')
    cases = {case['id']: case for case in protocol['cases']}
    require(len(cases) == len(protocol['cases']), 'Duplicate case')
    pairs = {(case, mode) for case in cases for mode in protocol['conditions']}
    actual_pairs = [(r['case_id'], r['mode']) for r in runs]
    require(len(actual_pairs) == len(pairs) and set(actual_pairs) == pairs, 'Case/condition denominator mismatch')
    summary = {}
    for run in runs:
        computed = score(run, cases[run['case_id']])
        require(run['metrics'] == computed, 'Recorded metrics disagree with oracle')
        aggregate = summary.setdefault(run['mode'], {})
        for key, value in computed.items():
            if key != 'acknowledgment_delay_steps':
                aggregate[key] = aggregate.get(key, 0) + value
    require(results['summary'] == summary, 'Summary mismatch')
    require(results['executions'] == len(runs) and results['cases'] == len(cases), 'Total mismatch')
    require(results['model_calls'] == execution['model_calls'] == 0 and results['independent_model_tasks'] == 0, 'Evidence-kind mismatch')
    return {'status': 'PASS', 'executions': len(runs), 'cases': len(cases), 'summary': summary,
            'scope': 'saved evidence integrity and metric recalculation; not runtime reproduction or external attestation'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.root), sort_keys=True))
    except (ValueError, KeyError, TypeError, OSError) as error:
        raise SystemExit('VERIFICATION FAILED: ' + str(error))
