"""EDL v2: the output timeline, and the guards that stop a wrong render."""

from __future__ import annotations

import json

import pytest

from helpers.edl import EDL, EDLError, Overlay, Range


def test_output_time_mapping_across_segments(simple_edl):
    assert simple_edl.offsets() == [0.0, 4.0]
    assert simple_edl.total_duration_s == 8.0
    assert simple_edl.to_output_time("raw01", 2.5) == 0.5
    assert simple_edl.to_output_time("raw01", 10.5) == 4.5
    # A word inside the removed stretch has no place on the output timeline.
    assert simple_edl.to_output_time("raw01", 8.0) is None


def test_source_time_round_trip(simple_edl):
    assert simple_edl.to_source_time(4.5) == ("raw01", 10.5)
    assert simple_edl.to_source_time(99.0) is None


def test_unknown_source_is_rejected():
    e = EDL(sources={"raw01": "/a.mp4"}, ranges=[Range("raw02", 0, 1)])
    with pytest.raises(EDLError, match="not in sources"):
        e.validate()


def test_overlapping_ranges_are_rejected():
    e = EDL(sources={"a": "/a.mp4"}, ranges=[Range("a", 0, 5), Range("a", 4.9, 8)])
    with pytest.raises(EDLError, match="overlap"):
        e.validate()


def test_unverified_overlay_never_ships(simple_edl):
    simple_edl.overlays = [Overlay("s.mp4", 1.0, 2.0, {"url": "https://x", "verified": False})]
    with pytest.raises(EDLError, match="verified"):
        simple_edl.validate()


def test_overlay_without_a_source_url_never_ships(simple_edl):
    simple_edl.overlays = [Overlay("s.mp4", 1.0, 2.0, {"verified": True})]
    with pytest.raises(EDLError, match="url"):
        simple_edl.validate()


def test_overlay_past_the_end_is_rejected(simple_edl):
    simple_edl.overlays = [Overlay("s.mp4", 7.0, 3.0, {"url": "u", "verified": True})]
    with pytest.raises(EDLError, match="past the end"):
        simple_edl.validate()


def test_overlapping_overlays_are_rejected(simple_edl):
    meta = {"url": "u", "verified": True}
    simple_edl.overlays = [Overlay("a.mp4", 0.0, 3.0, meta), Overlay("b.mp4", 2.0, 2.0, meta)]
    with pytest.raises(EDLError, match="overlap"):
        simple_edl.validate()


def test_round_trip_keeps_the_v1_subset_render_py_reads(simple_edl, tmp_path):
    simple_edl.overlays = [Overlay("o.mp4", 1.0, 2.0, {"url": "u", "verified": True})]
    simple_edl.subtitles = "edit/captions/final.ass"
    path = simple_edl.save(tmp_path / "edl.json")
    raw = json.loads(path.read_text())

    assert raw["version"] == 2
    # Exactly what vendored render.py reaches for.
    assert set(raw["sources"]) == {"raw01"}
    assert {"source", "start", "end"} <= set(raw["ranges"][0])
    assert {"file", "start_in_output", "duration"} <= set(raw["overlays"][0])
    assert raw["subtitles"] == "edit/captions/final.ass"
    assert raw["total_duration_s"] == 8.0

    assert EDL.load(path).to_output_time("raw01", 10.5) == 4.5


def test_empty_edl_is_refused():
    with pytest.raises(EDLError, match="no ranges"):
        EDL(sources={"a": "/a.mp4"}).validate()


@pytest.mark.parametrize("fps", [30, 25, 24, 30000 / 1001, 60])
def test_ranges_render_to_exactly_the_planned_length(fps):
    """render.py cuts with `-t f"{end - start:.3f}"` (from the saved, rounded
    values) and keeps every frame before that time. Unsnapped, IMG_7560 came out
    0.43 s longer than its plan and the captions ran ahead of the voice."""
    import random

    from helpers.edl import snap_to_frames
    rng = random.Random(7)
    raw = [Range("a", s, s + rng.uniform(0.2, 20)) for s in (rng.uniform(0, 600) for _ in range(2000))]
    drift = 0.0
    for before, r in zip(raw, snap_to_frames(raw, fps)):
        d = Range.from_dict(r.to_dict()).duration          # what render.py reads back
        frames = 0
        while frames / fps < float(f"{d:.3f}") - 1e-9:        # what render.py keeps
            frames += 1
        assert -1e-9 <= frames / fps - d < 0.001               # rendered == planned, < 1 ms
        assert r.end >= before.end - 0.001                     # only ever extended: no word cut
        assert r.end - before.end < 1 / fps + 0.001
        drift += frames / fps - d
    assert drift / len(raw) < 0.001
