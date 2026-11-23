---
name: zeta-clips
description: Cut social clips (Instagram / TikTok / Facebook) out of one of Ali's long YouTube talks - find complete punchy ideas (spliced from different parts if needed), minimal edit in the reference-reel look, Ali's grade, hand-timed English phrase captions, and a cinematic outro that zooms into the real YouTube watch page. Use whenever Ali asks for "clips", "a reel from the YouTube video", or "the punchy part".
---

# Zeta clips (from a YouTube talk)

Part of the facecam YouTube framework (`zeta-youtube`, step 10). Everything below is the
DEFAULT Ali approved on DJI_0103; when he sends a new reference or asks for a change, follow
him and update this file. Not for news reels / vlogs (those stay on `zeta-editor`).

Approved on DJI_0103 (2026-11-01), clip 1 "Americans": the reference implementation is
`~/Movies/zeta/DJI_0103/clipkit/` (`caps.py`, `render.py`, `music.py`, `yt_page.png`,
`yt_logo_white.png`) and `~/Movies/zeta/DJI_0103/make_clips.py` (spans -> EDL -> preview).

## 1. Find the clips (the job Ali judges first)

A clip is ONE complete idea: hook -> argument -> payoff, 45 s to 1:45. Read the whole
transcript (the reviewed `final.en.srt` side by side with the Darija), then propose 3-4:

* Lead with the hardest line ("Americans are fucking dumbasses"), or the thesis
  ("your competition is 1%"). Ali may move the start to the setup sentence before it.
* Splicing across the video is allowed when it builds one argument (the 1% funnel used
  7 spans). Keep the evidence beats skeptics need (Ali added "there is no data for this").
* Never cut rhetorical repetition; reuse the main cut's hand-checked stutter list.
* Give each candidate: time range, the beats in one line each, length. Recommend one.
* Then 720p previews of the CUTS only (no captions, no outro) for him to watch first.

Spans are source word indices (inclusive) -> `derive_cuts.derive` -> the same silence
tighten as the main cut -> `edl.build(..., aspect="16:9")`. Check no edge inside a kept word.

## 2. The look (reference: jettfranzen reel, saved as a screen recording)

* 1.4:1 landscape 1512x1080 (not 9:16). Crop the 16:9 frame so Ali sits right of centre,
  empty wall on the left (`crop_x` 150 of 3840; 0 when he sits further left).
* No zooms, no b-roll, no effects. Grade = Ali's LUT (`grade/ali_grade.cube`), fitted from
  his own graded export by matching frames (polynomial RGB fit on aligned, subtitle-free,
  non-moving frames; baked to a 33^3 .cube). Re-fit for each new video he grades.
* Per-clip framing in `<clip>/final/layout.json` (`crop_x`, `text_x`): proof every clip, he
  moves between parts of the talk (clip 3 needed crop_x 0, text_x 310).
* Captions: short English phrases (<= ~45 chars, 2 lines of 24), Avenir Next Demi Bold 66 px,
  white, 2.6 px black outline, centred at x 360 / y 390 on the wall at eye level. Hand-written
  translations keyed to word spans (`phrases.json`), mapped via `EDL.to_output_time`; merge any
  phrase under ~0.9 s (rewrite shorter rather than drop meaning). Phrase starts are synced to his
  voice in the clip's own audio (caps.py + `captions.sync_starts`, render.py re-runs it); check
  with `clipkit/cue_check.py`. Swear words as he said them.
  Font was picked from 5 stills (Helvetica, Futura, Montserrat, Avenir, Baskerville): when a
  new look is asked, show 5 options the same way. libass picks the wrong face silently
  (SF Pro came out thin, "Avenir Next" + bold came out italic): use the exact face name.
* Music: an original ambient bed (`music.py`), NOT sad (newyt 2026-11-07: major Cadd9-G-Fmaj7-G, 4 s bars,
  rising pentatonic plucks; then "other sound matching my talk": `newyt/clipkit/music_pulse.py`, 100 BPM
  Fmaj7-G-Em7-Am arp + soft kick), volume 0.035 (~21 dB under a -22 LUFS voice; he said "less volume, we went
  through this" at 0.067 with the brighter bed). Previously: about
  20 dB under the voice (volume 0.067 against a -16.4 LUFS voice), sidechain-ducked.
  He asked for it a bit quieter than the first try.

* Music mood per clip: `music_pulse.py <dur> <out> dark` (minor, 92 BPM) when he wants it "less joyful" (newyt clip 2,
  2026-11-07); `bright` is the default. Same volume 0.035.

## 3. Outro (reference: Ali's "axioms" reel, Aug 2026)

Last ~6.8 s: zoom out (1.4 s, smoothstep) from the full frame into the YouTube player on the
REAL watch page of the full video (not live yet? `newyt/clipkit/title_patch.py` repaints the title on the last page capture) (playwright capture, dark mode via cookie `PREF=f6=400`,
ads / sidebar / views / comments hidden with CSS); the clip keeps playing inside the player
with its captions; YouTube logo (rendered from the page's own SVG, wordmark recoloured white)
+ tracked "FULL VIDEO ON YOUTUBE" fade in on his chest (never over the captions); blur and
fade to black only AFTER his last word (2.2 s tail, sound fades out). Captions are burned on
the 16:9 footage BEFORE the zoom so they shrink with it, like the reference.

## 4. Proof before render

Proof frames (crop + grade + captions) at 3 points per clip: text must clear his head.
Font choice: show 5 options as stills; he picks. Then render; check the outro frames.

## Steps and checks (what went wrong once)

1. Candidates (text) -> he picks / adds ("make all 3", "add the exam one", "start with the
   sentence before", "add the no-data part").
2. Cut previews (720p, no captions). 3. Proof frames. 4. Render: `clipkit/caps.py <clip>`
   then `clipkit/render.py <clip>` (~5 min each). 5. Check outro frames + the font in the
   final, then `open` the file and give the full path.
- Logo over the caption = rejected; blur before the last line ended = rejected.
- Music first try too loud ("a bit less loud so they can hear me"): now volume 0.067.

## Publishing

`zeta publish --to tiktok,ig,fb` works for Facebook. TikTok (unaudited app) and Instagram
long Reels (Meta ProcessingFailedError over ~30 s) fail via the API: Ali uploads those by hand.
Post caption: fix his spelling, keep his words.
