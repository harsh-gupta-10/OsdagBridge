"""Report layout, palette, table rules, and chart presentation."""
import re
from osdagbridge.core.reports.report_utils import _tex

ACCENT_HEX = "91B014"
PAGE_MARGIN_MM = 18
PAGE_BOTTOM_MM = 30
FOOT_SKIP_MM = 17
ROW_PADDING_PT = 4
TABLE_COLUMN_PADDING_PT = 3
CHART_PASS_COLOR = "#91B014"
CHART_FAIL_COLOR = "#C43C32"
CHART_NEUTRAL_COLOR = "#477A9C"

def preamble(project_name, job_number, report_date, report_version='Rev 0'):
    pn = _tex(project_name)
    jn = _tex(job_number)
    rd = _tex(report_date)
    rv = _tex(report_version)
    tex = r"""
\documentclass[12pt,a4paper]{report}

% Packages
\usepackage[a4paper, left=18mm, right=18mm, top=24mm, bottom=30mm, headheight=18pt, headsep=8mm, footskip=17mm]{geometry}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{float}
\usepackage{fancyhdr}
\usepackage[hidelinks]{hyperref}
\usepackage{xcolor}
\usepackage{setspace}
\usepackage{enumitem}
\usepackage{caption}

\captionsetup{
    labelfont=bf,
    justification=raggedright,
    singlelinecheck=false,
    format=plain
}
\usepackage{subcaption}
\usepackage{multirow}
\usepackage{colortbl}
\usepackage{longtable}
\setlength{\LTleft}{\fill}
\setlength{\LTright}{\fill}
\usepackage{titlesec}
\usepackage{titletoc}
\usepackage{lastpage}
\usepackage{makecell}
\usepackage{etoolbox}
\usepackage{needspace}

\numberwithin{table}{chapter}
\numberwithin{figure}{chapter}
% Table layout and spacing: consistent padding, row height, and longtable pre/post skips
\newcommand{\reportrowpad}{4pt}
\newcommand{\reportsectiongap}{0.75em}
\newcommand{\reportsmallgap}{0.4em}
\newcommand{\reportmediumgap}{0.6em}
\newcommand{\reportlargegap}{2.2em}
\newcommand{\reportchaptergap}{0.4cm}
\newcommand{\reportbigchaptergap}{0.8cm}
\newcommand{\reportcaptiongap}{4pt}
\newcommand{\reporttabcolsep}{4pt}
\newcommand{\reportcompactcolsep}{2.5pt}
\newcommand{\reporttallrowstretch}{1.25}
\setlength{\tabcolsep}{\reporttabcolsep}
\renewcommand{\arraystretch}{1.10}
\setlength{\LTpre}{0pt}
\setlength{\LTpost}{6pt}
% Table rules (outline thickness) and small extra row height for clarity
\setlength{\arrayrulewidth}{0.5pt}
\setlength{\extrarowheight}{0.8pt}

% Prevent tables from overflowing past the page bottom:
% if fewer than 5 baseline-skips remain, break to the next page first.
\BeforeBeginEnvironment{table}{\needspace{5\baselineskip}}
\BeforeBeginEnvironment{longtable}{\needspace{5\baselineskip}}

\definecolor{osdagGreen}{HTML}{91B014}

\fancypagestyle{main}{
  \fancyhf{}
  \fancyhead[L]{""" + pn + r""" $|$ """ + jn + r"""}
  \fancyhead[R]{""" + rd + r""" $|$ """ + rv + r"""}
  \fancyfoot[L]{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}
  \fancyfoot[R]{Page \thepage\ of \pageref{LastPage}}
  \renewcommand{\headrule}{\color{osdagGreen}\hrule width\headwidth height 1pt \vspace{2pt}}
  \renewcommand{\footrule}{%
    \ifbool{hasSDonPage}{%
      \vspace{0pt}%
      \hbox to \headwidth{\textcolor{black}{\footnotesize\textit{* Software default value}}\hfil}%
      \vspace{4pt}%
    }{%
      \vspace{0pt}%
    }%
    \color{osdagGreen}\hrule width\headwidth height 1pt \vspace{6pt}%
  }
}
\fancypagestyle{plain}{
  \fancyhf{}
  \fancyhead[L]{""" + pn + r""" $|$ """ + jn + r"""}
  \fancyhead[R]{""" + rd + r""" $|$ """ + rv + r"""}
  \fancyfoot[L]{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}
  \fancyfoot[R]{Page \thepage\ of \pageref{LastPage}}
  \renewcommand{\headrule}{\color{osdagGreen}\hrule width\headwidth height 1pt \vspace{2pt}}
  \renewcommand{\footrule}{%
    \ifbool{hasSDonPage}{%
      \vspace{0pt}%
      \hbox to \headwidth{\textcolor{black}{\footnotesize\textit{* Software default value}}\hfil}%
      \vspace{4pt}%
    }{%
      \vspace{0pt}%
    }%
    \color{osdagGreen}\hrule width\headwidth height 1pt \vspace{6pt}%
  }
}
\fancypagestyle{firstpage}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \fancyfoot[L]{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}
  \fancyfoot[R]{Page \thepage\ of \pageref{LastPage}}
  \renewcommand{\footrule}{\color{osdagGreen}\hrule width\headwidth height 1pt \vspace{6pt}}
}
\pagestyle{main}
\setstretch{1.15}

% Custom Commands
\newcommand{\placeholder}[1]{\textit{\textless #1\textgreater}}
\newcommand{\todo}[1]{\colorbox{yellow}{TODO: #1}}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}

% Software-default asterisk
\newcommand{\sdstar}{\textsuperscript{*}}
\newbool{hasSDonPage}
\boolfalse{hasSDonPage}
\newcommand{\markSD}{\global\booltrue{hasSDonPage}}
\renewcommand{\sdstar}{\textsuperscript{*}\markSD{}}
\AddToHook{shipout/before}{\global\boolfalse{hasSDonPage}}

\title{\Large\textbf{OsdagBridge} \\ \normalsize Open Source Software for Steel Girder Bridge Design \\ \vspace{2cm} \large Design Report}
\author{}
\date{}

\begin{document}
"""
    return (tex.replace("left=18mm, right=18mm", f"left={PAGE_MARGIN_MM}mm, right={PAGE_MARGIN_MM}mm")
               .replace("bottom=30mm", f"bottom={PAGE_BOTTOM_MM}mm")
               .replace("footskip=17mm", f"footskip={FOOT_SKIP_MM}mm")
               .replace(r"\newcommand{\reportrowpad}{4pt}",
                        rf"\newcommand{{\reportrowpad}}{{{ROW_PADDING_PT}pt}}")
               .replace(r"\newcommand{\reporttabcolsep}{4pt}",
                        rf"\newcommand{{\reporttabcolsep}}{{{TABLE_COLUMN_PADDING_PT}pt}}")
               .replace("{HTML}{91B014}", f"{{HTML}}{{{ACCENT_HEX}}}"))




def repeat_longtable_headers(document):
    """Repeat the first heading row on each page for legacy longtables.

    Explicitly authored first/continuation headings are preserved. Captions remain
    in the first head only, so they are not duplicated on continuation pages.
    """
    pattern = re.compile(r"(\\begin\{longtable\}(?:\[[^]]*\])?\{[^\n]*\})(.*?)(\\end\{longtable\})", re.S)

    def update(match):
        begin, body, end = match.groups()
        first = body.find(r"\hline")
        if first >= 0 and r"\caption" in body[:first] and not body[:first].rstrip().endswith(r"\\"):
            # longtable captions are table rows and need a row terminator.
            body = body[:first].rstrip() + r"\\" + "\n" + body[first:]
            first = body.find(r"\hline")
        second = body.find(r"\hline", first + 6) if first >= 0 else -1
        if second < 0:
            return match.group(0)
        heading = body[first:second + len(r"\hline")]
        if r"\textbf" not in heading:
            return match.group(0)
        if r"\endfirsthead" in body:
            firsthead = body.index(r"\endfirsthead")
            endhead = body.find(r"\endhead", firsthead)
            if endhead >= 0 and not body[firsthead + len(r"\endfirsthead"):endhead].strip():
                body = body[:firsthead + len(r"\endfirsthead")] + "\n" + heading + "\n" + body[endhead:]
            return begin + body + end
        continuation = "\n" + r"\endfirsthead" + "\n" + heading + "\n" + r"\endhead"
        return begin + body[:second + len(r"\hline")] + continuation + body[second + len(r"\hline"):] + end

    return pattern.sub(update, document)
