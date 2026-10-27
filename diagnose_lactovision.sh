#!/usr/bin/env bash
# LactoVision launcher diagnostic for macOS
set -u

DOWNLOADS="$HOME/Downloads"
ROOT=""
for candidate in "$DOWNLOADS/LactoVision_Phase5_Ready" "$DOWNLOADS/LactoVision_Phase5_Ready "; do
  if [[ -d "$candidate/backend" && -d "$candidate/ai" ]]; then
    ROOT="$candidate"
    break
  fi
done

if [[ -z "$ROOT" ]]; then
  echo "Could not locate LactoVision project folder."
  echo "Run: ls -ld ~/Downloads/LactoVision_Phase5_Ready*"
  exit 1
fi

echo "Project: $ROOT"
echo
echo "===== Backend log (last 80 lines) ====="
if [[ -f "$ROOT/logs/backend.log" ]]; then
  tail -n 80 "$ROOT/logs/backend.log"
else
  echo "No backend log found."
fi

echo
echo "===== Frontend log (last 80 lines) ====="
if [[ -f "$ROOT/logs/frontend.log" ]]; then
  tail -n 80 "$ROOT/logs/frontend.log"
else
  echo "No frontend log found."
fi

echo
echo "===== Frontend package scripts ====="
if [[ -f "$ROOT/frontend/package.json" ]]; then
  node -e 'const p=require(process.argv[1]); console.log(JSON.stringify(p.scripts || {}, null, 2))' "$ROOT/frontend/package.json" 2>&1
else
  echo "No frontend/package.json found at expected location."
fi

echo
echo "===== npm / node versions ====="
command -v node >/dev/null 2>&1 && node --version || echo "node not found"
command -v npm >/dev/null 2>&1 && npm --version || echo "npm not found"

echo
echo "Diagnostic complete. Copy this output back here; do not include .env contents."
