#!/usr/bin/env bash
# assemble_example.sh — normalize clips, then join with the concat FILTER.
#
# Why this shape (learned the hard way in production):
# - Stock clips arrive at mixed frame rates (24/30/50/60) and codecs. The
#   ffmpeg concat demuxer produces broken output from mixed inputs.
# - Normalizing every clip to one spec first, then joining with the
#   concat filter + aresample=async=1, is the reliable path.
#
# Usage: ./assemble_example.sh narration.wav clip1.mp4 clip2.mp4 ... out.mp4
set -euo pipefail

NARRATION="$1"; shift
OUT="${@: -1}"; set -- "${@:1:$(($#-1))}"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
FILTER=""; INPUTS=(); i=0

# 1) Normalize every clip: 1080x1920 (crop-fill), 30fps, yuv420p, no audio
for clip in "$@"; do
  ffmpeg -v error -i "$clip" \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p" \
    -an -c:v libx264 -preset veryfast "$TMP/n$i.mp4"
  INPUTS+=(-i "$TMP/n$i.mp4")
  FILTER+="[$i:v]"
  i=$((i+1))
done

# 2) Concat filter for video + the narration as the only audio track.
#    (Trim/pad the video stream to the narration length beforehand if your
#    beats are pre-timed; see PIPELINE.md step 6.)
ffmpeg -v error "${INPUTS[@]}" -i "$NARRATION" \
  -filter_complex "${FILTER}concat=n=$i:v=1:a=0[v]" \
  -map "[v]" -map "$i:a" -c:v libx264 -preset veryfast -c:a aac \
  -movflags +faststart -shortest "$OUT"

echo "wrote $OUT"
