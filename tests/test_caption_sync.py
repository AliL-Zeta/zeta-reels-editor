from helpers.captions import sync_starts

F = 0.01


def _mask(spans, total=5.0):
    m = [False] * int(total / F)
    for a, b in spans:
        for i in range(int(a / F), int(b / F)):
            m[i] = True
    return m


def test_cue_in_silence_waits_for_the_voice():
    voiced = _mask([(0.0, 1.0), (1.6, 3.0)])
    words = [(0.0, 1.0), (1.6, 3.0)]
    # interpolated start 1.2 s lands in the pause: caption would appear before he speaks
    assert abs(sync_starts([0.0, 1.2], words, voiced)[1] - 1.57) < 0.02


def test_late_cue_moves_back_to_where_he_resumed():
    voiced = _mask([(0.0, 1.0), (1.6, 3.0)])
    words = [(0.0, 1.0), (1.6, 2.2), (2.3, 3.0)]
    # interpolated start 2.3 s is on the second word after the pause: caption is late
    assert abs(sync_starts([0.0, 2.3], words, voiced)[1] - 1.57) < 0.02


def test_no_audio_snaps_to_word_starts_and_keeps_order():
    words = [(0.0, 0.5), (0.9, 1.4), (1.5, 2.0)]
    out = sync_starts([0.0, 1.0, 1.45], words, None)
    assert out == sorted(out) and abs(out[1] - 0.9) < 1e-6
