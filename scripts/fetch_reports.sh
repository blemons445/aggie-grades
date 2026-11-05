#!/bin/bash
# Downloads the registrar's grade distribution PDFs for the given terms, one college at a time.
# Usage: scripts/fetch_reports.sh "2026 SPRING" "2025 FALL" ...   (needs curl; run from the repo root)
mkdir -p reports
for t in "$@"; do set -- $t
  cut -d'|' -f1 scripts/colleges.txt | while read c; do
    f="reports/$1-$2-$c.pdf"; [ -s "$f" ] && continue
    curl -sS -m 90 "https://web-as.tamu.edu/gradereports/Report?year=$1&term=$2&college=$c" -o "$f" 2>/dev/null
    file "$f" | grep -q PDF || rm -f "$f"
    sleep 0.7
  done
done
