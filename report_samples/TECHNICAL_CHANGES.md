# OsdagBridge report generator changes

## Scope

The report generator in `src/osdagbridge/core/reports` emits LaTeX strings. The
implementation keeps that architecture and centralizes presentation in
`styles.py`. It does not add a PyLaTeX dependency or convert every chapter to
PyLaTeX objects, since doing so would replace the existing report templates.

## Changes

- `styles.py` owns page geometry, footer spacing, palette, table padding, row
  spacing, section gaps, and the report preamble. Its longtable pass supplies
  `\endfirsthead` and `\endhead` for legacy tables and fills an existing empty
  continuation heading. Explicit multirow continuation headings are retained.
- `report_generator.py` applies the longtable pass to the assembled report and
  writes chart assets to the temporary report directory. It uses Tectonic when
  no `pdflatex` executable is available.
- `chap3.py` lists only the vehicle classes selected in the loading inputs. It
  places vehicle loads and footway loads in separate tables with unit columns.
  Centrifugal force reads an explicit input if present and otherwise says
  “Not specified,” since no computed centrifugal value exists in the current
  report payload.
- `core/utils/codes/irc6_2017.py` initializes the braking-force components and
  converts Newton-valued wheel loads to tonnes-force before the report formats
  the result in kN. This resolves an N/A value for valid lane counts.
- `chap5.py` includes a governing utilization chart in the overall design
  summary. The bars come from the same rows as Table 5.22. Missing member
  results are marked N/A; the chart does not invent an end diaphragm UR.
- `chap7.py` includes structural steel and deck material charts. The concrete
  volume and reinforcement mass use separate axes. The current quantity
  calculator does not return end diaphragm tonnage, so that bar is N/A.
- `charts.py` draws plots with Matplotlib and embeds them as LaTeX figures.
- Chapter files now consume spacing and padding macros from `styles.py`.
  `chap5.py` also gives two formerly unheaded tables explicit column headings.

## Verification and report samples

`Report_Before.pdf` and `Report_After.pdf` use the same **illustrative fixture**
created by `tools/generate_report_sample.py`. They demonstrate layout changes;
their values are not the result of a bridge analysis. The baseline uses the
upstream `dev` checkout at commit `d74f56d`. The enhanced sample uses this
working tree. The baseline fixture receives only a missing LaTeX caption row
terminator so it can compile; its original table layout is retained. Both PDF
sources are included for inspection.

The GUI design sequence requires the full OsdagBridge environment and a design
run. That sequence was not available on this machine. Reproduce it in the
documented Conda environment to compare actual engineering results.
