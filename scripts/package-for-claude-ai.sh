#!/usr/bin/env bash
# Builds one upload-ready zip per skill for claude.ai / the Claude apps (Customize > Skills > upload).
# Each zip's single top-level entry is the skill folder, which is what the uploader expects.
set -euo pipefail
cd "$(dirname "$0")/../skills"
mkdir -p ../dist
for skill in */; do
  skill=${skill%/}
  rm -f "../dist/$skill.zip"
  zip -qr "../dist/$skill.zip" "$skill" -x '*.DS_Store'
  echo "dist/$skill.zip"
done
