"""Render a clearly labeled illustrative report from a selected source checkout.

Usage: PYTHONPATH=src python tools/generate_report_sample.py OUTPUT_DIR STEM
The script intentionally does not run a structural design or assert that the
example values represent a real bridge.
"""

import inspect
import re
import sys
from pathlib import Path

from osdagbridge.core.reports.report_generator import (
    ReportDataBridge, ReportFigures, ReportMetadata, ReportOptions,
    ReportPayload, preamble, title_page, toc_section,
)
from osdagbridge.core.reports.chap1 import ch1_project_info
from osdagbridge.core.reports.chap2 import ch2_input_parameters
from osdagbridge.core.reports.chap3 import ch3_loads
from osdagbridge.core.reports.chap4 import ch4_analysis
from osdagbridge.core.reports.chap5 import ch5_design_checks
from osdagbridge.core.reports.chap6 import ch6_drawings
from osdagbridge.core.reports.chap7 import ch7_quantities
from osdagbridge.core.reports.chap8 import ch8_design_log
from osdagbridge.core.reports.chap9 import references
from osdagbridge.core.utils.common import (
    KEY_DD_M_ULS_SAG, KEY_DD_MU_BOT, KEY_LL_FOOTPATH_PRESSURE_MODE,
    KEY_LL_IRC_70R_WHEELED, KEY_LL_IRC_CLASS_A, KEY_SPAN,
    KEY_TS_NO_OF_FOOTPATHS, KEY_TS_NO_OF_GIRDERS, KEY_WC_LD_LANE_TABLE_COUNT,
)


def main(output_dir, stem):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    assets = output / "assets"
    assets.mkdir(exist_ok=True)
    metadata = ReportMetadata("Illustrative Bridge", "Mumbai", "Sample Designer",
                              "Sample Client", "FOSSEE", job_number="SAMPLE-001",
                              report_date="2026-11-19", subtitle="Illustrative fixture")
    inputs = {
        KEY_SPAN: "24", KEY_TS_NO_OF_GIRDERS: "4",
        KEY_TS_NO_OF_FOOTPATHS: "2", KEY_LL_IRC_CLASS_A: True,
        KEY_LL_IRC_70R_WHEELED: True,
        KEY_LL_FOOTPATH_PRESSURE_MODE: "As per IRC 6",
        KEY_WC_LD_LANE_TABLE_COUNT: "2",
        "steel_girders_wt_total": "42.5",
        "bracing_top_wt_total": "1.2", "bracing_bot_wt_total": "1.3",
        "bracing_diag_wt_total": "2.4",
        "concrete_deck_vol_total": "57.6", "rebar_deck_wt_total": "6.91",
    }
    for i in range(1, 5):
        inputs[f"member_properties.girder_details.select_girder.G{i}"] = f"G{i}"
        inputs[f"member_properties.girder_details.member_id.G{i}.M1"] = f"G{i}M1"
    outputs = {
        "design_results": {"per_girder": {
            "G1": {"checks": [
                {"check_id": 1, "dcr": 0.82, "demand": 820, "capacity": 1000,
                 "demand_unit": "kNm", "capacity_unit": "kNm"},
                {"check_id": 2, "dcr": 0.74, "demand": 296, "capacity": 400,
                 "demand_unit": "kN", "capacity_unit": "kN"},
            ]}
        }},
        "deck_report_values": {KEY_DD_M_ULS_SAG: 75, KEY_DD_MU_BOT: 100},
    }
    payload = ReportPayload(metadata, ReportOptions([], True, True, True), inputs,
                            {}, [], ReportFigures(), output_dict=outputs)
    bridge = ReportDataBridge(outputs, inputs, payload)
    is_new = "asset_dir" in inspect.signature(ch5_design_checks).parameters
    parts = [preamble(metadata.project_name, metadata.job_number,
                      metadata.report_date, metadata.subtitle),
             title_page(metadata, None, None), toc_section(),
             r"\chapter*{Illustrative fixture}",
             r"The values in this report are sample inputs for checking report layout. "
             r"They are not the output of a structural analysis or design.",
             ch1_project_info(metadata), ch2_input_parameters(metadata, inputs, outputs),
             ch3_loads(inputs), ch4_analysis({}, {}, bridge, 24),
             ch5_design_checks([], bridge, assets) if is_new else ch5_design_checks([], bridge),
             ch6_drawings({}),
             ch7_quantities(inputs, assets) if is_new else ch7_quantities(inputs),
             ch8_design_log([], inputs), references(), r"\end{document}"]
    tex = "\n".join(parts)
    if is_new:
        from osdagbridge.core.reports.styles import repeat_longtable_headers
        tex = repeat_longtable_headers(tex)
    else:
        # The upstream templates omit a required row terminator after some
        # longtable captions. Repair only that syntax so the baseline can render.
        def baseline_caption_fix(match):
            table = match.group(0)
            first = table.find(r"\hline")
            if first >= 0 and r"\caption" in table[:first] and not table[:first].rstrip().endswith(r"\\"):
                table = table[:first].rstrip() + r"\\" + "\n" + table[first:]
            return table
        tex = re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}",
                     baseline_caption_fix, tex, flags=re.S)
    tex = "\n".join(line.rstrip() for line in tex.splitlines()) + "\n"
    (output / f"{stem}.tex").write_text(tex)
    print(output / f"{stem}.tex")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
