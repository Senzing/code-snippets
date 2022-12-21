if [ ! -f truthset-project3.json ]
then
    cd $(dirname $0)
fi

G2Loader.py \
    --FORCEPURGE \
    --projectFile truthset-project3.json

G2Snapshot.py \
    --output_file_root truthset-load3-snapshot \
    --for_audit -q

G2Audit.py \
    --newer_csv_file truthset-load3-snapshot.csv \
    --prior_csv_file truthset-load3-key.csv \
    --output_file_root truthset-load3-audit

G2Explorer.py \
    --snapshot_json_file truthset-load3-snapshot.json \
    --audit_json_file truthset-load3-audit.json

