from pathlib import Path

from osdagbridge.core.reports.chap3 import ch3_loads
from osdagbridge.core.reports.charts import write_quantity_charts, write_utilization_chart
from osdagbridge.core.reports.styles import repeat_longtable_headers
from osdagbridge.core.utils.common import (
    KEY_LL_IRC_CLASS_A, KEY_LL_IRC_70R_TRACKED, KEY_SPAN,
)


def test_legacy_longtable_repeats_heading_without_repeating_caption():
    source = (r"\begin{longtable}{|c|}" + "\n"
              + r"\caption{Checks}" + "\n"
              + r"\hline" + "\n" + r"\textbf{Member} \\" + "\n"
              + r"\hline" + "\n" + r"G1 \\" + "\n"
              + r"\end{longtable}")
    result = repeat_longtable_headers(source)
    assert result.count(r"\caption{Checks}") == 1
    assert result.count(r"\textbf{Member}") == 2
    assert result.count(r"\endfirsthead") == 1
    assert result.count(r"\endhead") == 1


def test_live_loads_follow_vehicle_selection_and_separate_footway():
    tex = ch3_loads({KEY_SPAN: 24, KEY_LL_IRC_CLASS_A: True,
                     KEY_LL_IRC_70R_TRACKED: False})
    assert "Vehicle Live Loads" in tex
    assert "Footway Live Load" in tex
    assert "Class A" in tex
    assert "Class 70R (Tracked)" not in tex


def test_charts_keep_unavailable_quantities_explicit(tmp_path: Path):
    assert write_utilization_chart({}, tmp_path) == ""
    tex = write_quantity_charts({"steel_girders_wt_total": "42.5"}, tmp_path)
    assert "steel_quantities.png" in tex
    assert (tmp_path / "steel_quantities.png").exists()
    assert "deck_quantities.png" not in tex
