from pathlib import Path
import sys
import tempfile
import markdown
import win32com.client


CSS = """
<style>
  body {
    font-family: Calibri, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.4;
    color: #111827;
  }
  h1 {
    font-size: 22pt;
    color: #073763;
    border-bottom: 2px solid #073763;
    padding-bottom: 6pt;
  }
  h2 {
    font-size: 15pt;
    color: #073763;
    border-bottom: 1px solid #d1d5db;
    padding-bottom: 4pt;
    margin-top: 18pt;
  }
  h3 {
    font-size: 12.5pt;
    color: #1f4e79;
    margin-top: 14pt;
  }
  h4 {
    font-size: 11pt;
    color: #374151;
  }
  code {
    font-family: Consolas, monospace;
    font-size: 10pt;
    background: #f3f4f6;
    padding: 1px 3px;
  }
  pre {
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    padding: 8pt;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 8pt 0 12pt 0;
  }
  th, td {
    border: 1px solid #d1d5db;
    padding: 5pt 6pt;
    vertical-align: top;
  }
  th {
    background: #eaf2f8;
    color: #073763;
    font-weight: bold;
  }
  blockquote {
    border-left: 4px solid #9ca3af;
    padding: 4pt 10pt;
    color: #374151;
    background: #f9fafb;
  }
</style>
"""


def md_to_pdf(md_file: str):
    md_path = Path(md_file).resolve()

    if not md_path.exists():
        raise FileNotFoundError(md_path)

    pdf_path = md_path.with_suffix(".pdf")

    print(f"Reading {md_path.name}")
    md_text = md_path.read_text(encoding="utf-8")

    print("Converting Markdown...")
    html_body = markdown.markdown(
        md_text,
        extensions=[
            "tables",
            "fenced_code",
            "sane_lists",
            "md_in_html",
        ],
    )

    full_html = (
        "<!DOCTYPE html>"
        "<html><head><meta charset='utf-8'>"
        f"{CSS}"
        "</head><body>"
        f"{html_body}"
        "</body></html>"
    )

    # Temp HTML file - created, used, then deleted
    tmp_html = Path(
        tempfile.NamedTemporaryFile(
            suffix=".html",
            delete=False,
        ).name
    )
    tmp_html.write_text(full_html, encoding="utf-8")

    print("Launching Word...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    try:
        doc = word.Documents.Open(str(tmp_html))

        print("Saving PDF...")
        doc.SaveAs2(
            str(pdf_path),
            FileFormat=17,  # wdFormatPDF
        )

        doc.Close(False)
        print(f"PDF created: {pdf_path}")

    finally:
        word.Quit()
        tmp_html.unlink(missing_ok=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_pdf.py <markdown-file>")
        sys.exit(1)

    arg = Path(sys.argv[1])
    project_root = Path(__file__).resolve().parent.parent

    candidates = [
        arg,
        Path.cwd() / arg,
        project_root / arg,
    ]

    if not arg.is_absolute() and len(arg.parts) == 1:
        reports_dir = project_root / "reports"
        if reports_dir.exists():
            candidates.extend(reports_dir.rglob(arg.name))

    md_path = next((p for p in candidates if p.exists()), None)

    if md_path is None:
        print("Could not find the markdown file. Tried:")
        for c in candidates:
            print(f"  - {c}")
        sys.exit(1)

    print(f"Resolved: {md_path}")
    md_to_pdf(str(md_path))
