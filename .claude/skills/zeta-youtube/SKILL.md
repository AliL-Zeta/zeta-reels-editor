---
name: zeta-youtube
description: Ali's framework for a long FACECAM YouTube talk (16:9 4K, Darija/French/English, 20 min to 1h30+) - tighten edit, English subtitles, thumbnails, post caption, then social clips. Use when he brings a facecam YouTube video ("for youtube, editing and subtitles as usual"). Not for news reels with screenshots, vlogs, or vertical shorts - those keep their own rules (zeta-editor).
---

# Zeta YouTube facecam framework

Defaults from DJI_0103 "You are only competing with 1% of people" (2026-11-01). They are
DEFAULTS: when Ali gives new examples or asks for a change, follow him and update this file.
Scope: facecam YouTube talks only. Do not apply these choices to news reels (verified
screenshots, 9:16, cut-out cards), vlogs, or IG-first videos; those stay on `zeta-editor`.

Session dir `~/Movies/zeta/<name>/`; big outputs on his SSD in ONE new folder he allowed
(`/Volumes/Extreme Pro/<name>/`), never delete anything there. Reference scripts:
`~/Movies/zeta/DJI_0103/` (`fix_gaps.py`, `find_retakes.py`, `make_cut.py`, `render_cut.py`,
`make_captions.py`, `fix_caps.py`, `thumbs/make_thumbs.py`, `clipkit/`).

## Order of work (results first, short updates)

1. **Ask once** what "editing" means if he did not say (past answer: "Tighten it").
2. **Ingest + transcribe** (`zeta ingest`, `zeta transcribe` in background, caffeinate).
3. **Transcript QA**: words > 2 s, gaps > 3 s WITH speech-level audio = timing drift ->
   `realign_window(doc, wav, k-30, k+35, cfg, device="cpu")` on the original words (a
   re-transcription duplicates text). Check Gemini chunk joins; confirm suspected duplicates by a
   short Gemini listen before removing (on DJI_0103 both were real repetitions).
4. **Tighten** (no learned cut ratio; `zeta plan` is useless on long takes):
   Gemini proposes stutter / false-start / retake spans by word index; YOU check each in context.
   Keep rhetorical repetition and lists (most candidates). Then shorten measured silences
   >= 0.4 s to ~0.27 s of air (0.12 s before / 0.15 s after), never inside a word.
5. **4K master for grading** (`render_cut.py`): per-segment HEVC 10-bit 100 Mb/s + PCM audio,
   `-hwaccel videotoolbox -map 0:v:0` (software decode is 0.3x), seek `a - 0.5/fps`, concat with
   `-bsf:v setts=ts=N*1001/24000/TB`. Verify: video == audio duration, every segment start 0,
   frame-accurate vs source, AND scan packets for zeroed data (an SSD write zeroed 4 frames once).
   No subtitles burned: he grades first.
6. **English subtitles** on the cut timeline (`write_captions`, 16:9). Read ALL cues side by side
   with the Darija; fix mistranslations, names, garbled lines (listen before inventing).
   Swear words as he said them. Deliver `.en.srt` + `.ass` next to the cut.
   SYNC: cue starts are synced to his voice automatically (`captions.sync_starts`, needs
   `edit/audio/<source>.16k.wav`). After hand fixes, re-time without touching text
   (`DJI_0103/retime_subs.py`, against the cut master's own audio) and verify with
   `clipkit/cue_check.py`: target 0 early, <5% late. If he exports a shorter cut, map the subs onto
   HIS export (audio cross-correlation finds his cuts; `DJI_0103/subs_for_export.py`).
7. **He grades** (his LUT, his editor, maybe a shorter export). Fit his grade as a LUT from his
   export vs the cut (align by audio envelope; he may have trimmed; aligned, non-moving,
   subtitle-free frames), bake `grade/ali_grade.cube`. Reused for thumbnails and clips.
8. **Thumbnails**: SNEAKO style (memory `zeta-sneako-thumbnails`): graded frames (cut + LUT,
   not his export: it has burned subs), sharpest frame within +-1 s, 5 shots x his text options,
   words split around the head, tucked ~12 px (35 px hid letters). Give the folder path, open it.
9. **Post caption**: fix his spelling, keep his words and voice.
10. **Clips**: skill `zeta-clips` (find complete ideas, previews of cuts first, then style).

## Music

Clips get an original ambient bed under the voice (see `zeta-clips`). Open to change: he said
music is something to "play on later" - ask/offer options when he brings references.
