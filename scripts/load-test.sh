#!/usr/bin/env bash
set -euo pipefail

# Target URL default (can be overridden via TARGET_URL environment variable)
URL="${TARGET_URL:-http://taskboard.local/api/health}"
REQUESTS="${REQUESTS:-500}"

echo "Starting load test targeting: $URL"
echo "Total requests to send: $REQUESTS"

success=0
failure=0

for i in $(seq 1 "$REQUESTS"); do
  status_code=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || true)
  if [[ "$status_code" =~ ^(200|201|204)$ ]]; then
    ((success++))
  else
    ((failure++))
  fi

  if (( i % 50 == 0 )); then
    echo "Progress: $i / $REQUESTS requests completed (Success: $success, Failures: $failure)"
  fi
done

echo "=========================================="
echo "Load test finished successfully!"
echo "Total sent: $REQUESTS"
echo "Successful: $success"
echo "Failed:     $failure"
echo "=========================================="
