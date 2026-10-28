"""Tests for Universal Optical Grain Inspection (Bowls, Heaps, Separated Grains, Varieties)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from PIL import Image
import pytest
from vision import analyse
from app import detect_rice_type

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "samples")


def test_good_long_grain():
    path = os.path.join(SAMPLES_DIR, "good_long.png")
    res = analyse(Image.open(path))
    assert res is not None
    assert res["score"] >= 85
    assert res["grade"] == "A"
    assert res["quality_level"] == "high"
    assert res["verdict"] == "safe"
    top, conf, reasons, _ = detect_rice_type(res)
    assert top is not None
    assert "global_consumers" in top
    assert "global_producers" in top


def test_brown_rice_in_bowl():
    path = os.path.join(SAMPLES_DIR, "brown_bowl.png")
    res = analyse(Image.open(path))
    assert res is not None
    assert res["colour"] == "brown"
    assert res["grade"] == "A"
    assert res["verdict"] == "safe"
    top, conf, reasons, _ = detect_rice_type(res)
    assert "Brown" in top["name"]
    assert "1.2+ Billion" in top["global_consumers"]
    assert "38 Million" in top["global_producers"]


def test_red_rice_heap():
    path = os.path.join(SAMPLES_DIR, "red_heap.png")
    res = analyse(Image.open(path))
    assert res is not None
    assert res["colour"] == "red"
    assert res["grade"] == "A"
    assert res["verdict"] == "safe"
    top, conf, reasons, _ = detect_rice_type(res)
    assert "Matta" in top["name"] or "Red" in top["name"]
    assert "global_consumers" in top


def test_broken_mix():
    path = os.path.join(SAMPLES_DIR, "broken_mix.png")
    res = analyse(Image.open(path))
    assert res is not None
    assert res["broken_pct"] > 40
    assert res["quality_level"] == "low"
    assert res["grade"] == "Reject"
    top, conf, reasons, _ = detect_rice_type(res)
    assert "Broken" in top["name"]


def test_mouldy_rejection():
    path = os.path.join(SAMPLES_DIR, "mouldy.png")
    res = analyse(Image.open(path))
    assert res is not None
    assert res["verdict"] == "unsafe"
    assert res["quality_level"] == "low"
    assert res["green_pct"] > 1.0


def test_never_returns_none_on_blank():
    # Even on plain empty canvas, analyse() guarantees returning a result dict
    blank = Image.new("RGB", (200, 200), (240, 240, 240))
    res = analyse(blank)
    assert res is not None
    assert "score" in res
    assert "grade" in res
    assert "verdict" in res
