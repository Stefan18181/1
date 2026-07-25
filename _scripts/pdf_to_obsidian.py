#!/usr/bin/env python3
"""Konvertiert ein PDF in verlinkte Obsidian-Notizen.

Nutzung:
    python _scripts/pdf_to_obsidian.py <pdf> [--out ORDNER] [--title TITEL]

Erzeugt im Zielordner eine Notiz pro erkanntem Abschnitt, eine Index-Notiz
(MOC) mit Wikilinks auf alle Abschnitte und eine Rohtext-Notiz pro Seite.
"""

import argparse
import datetime
import pathlib
import re
import sys

from pypdf import PdfReader

# Zeichen, die Obsidian in Dateinamen nicht erlaubt bzw. als Syntax deutet.
ILLEGAL = re.compile(r'[\\/:*?"<>|#^\[\]]')


def slugify(text, fallback="Abschnitt"):
    """Macht aus einer Überschrift einen Obsidian-tauglichen Dateinamen."""
    cleaned = ILLEGAL.sub(" ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .-")
    return cleaned[:80] or fallback


def is_heading(line):
    """Heuristik für Überschriften in Report-PDFs.

    Überschriften sind kurz, enden nicht auf Satzzeichen und sind entweder
    durchgehend groß geschrieben oder im Title Case gesetzt.
    """
    line = line.strip()
    if not (3 <= len(line) <= 80):
        return False
    if line[-1] in ".,;:":
        return False
    if re.fullmatch(r"[\d\s.\-–—|]+", line):  # reine Seitenzahlen/Trenner
        return False

    letters = [c for c in line if c.isalpha()]
    if len(letters) < 3:
        return False

    upper_ratio = sum(c.isupper() for c in letters) / len(letters)
    if upper_ratio > 0.85:
        return True

    words = [w for w in line.split() if w[:1].isalpha()]
    if len(words) >= 2 and all(w[:1].isupper() for w in words):
        return True
    return False


def extract_pages(pdf_path):
    reader = PdfReader(str(pdf_path))
    if reader.is_encrypted:
        reader.decrypt("")  # leeres Passwort deckt Read-Protection ab
    return [(i, (page.extract_text() or "").strip())
            for i, page in enumerate(reader.pages, start=1)]


def split_sections(pages):
    """Gruppiert die Zeilen aller Seiten unter den erkannten Überschriften."""
    sections = []
    current = {"title": "Einleitung", "start_page": 1, "end_page": 1, "lines": []}

    for page_no, text in pages:
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            if is_heading(line):
                if current["lines"]:
                    sections.append(current)
                current = {"title": line, "start_page": page_no,
                           "end_page": page_no, "lines": []}
            else:
                current["lines"].append(line)
                current["end_page"] = page_no

    if current["lines"]:
        sections.append(current)
    return sections


def frontmatter(title, source, pages, tags):
    tag_block = "".join(f"\n  - {t}" for t in tags)
    return (
        "---\n"
        f'title: "{title}"\n'
        f'source: "{source}"\n'
        f"pages: {pages}\n"
        f"imported: {datetime.date.today().isoformat()}\n"
        f"tags:{tag_block}\n"
        "---\n\n"
    )


def write_notes(sections, pages, out_dir, doc_title, source):
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = out_dir / "Rohtext"
    raw_dir.mkdir(exist_ok=True)

    used = set()
    links = []

    for section in sections:
        name = slugify(section["title"])
        candidate, n = name, 2
        while candidate.lower() in used:
            candidate, n = f"{name} ({n})", n + 1
        used.add(candidate.lower())

        page_range = (f"{section['start_page']}"
                      if section["start_page"] == section["end_page"]
                      else f"{section['start_page']}-{section['end_page']}")

        body = frontmatter(section["title"], source, page_range,
                           ["ufc-pi", "import"])
        body += f"# {section['title']}\n\n"
        body += "\n\n".join(section["lines"])
        body += f"\n\n---\n\nZurück zu [[{doc_title}]]\n"

        (out_dir / f"{candidate}.md").write_text(body, encoding="utf-8")
        links.append((candidate, section["title"], page_range))

    for page_no, text in pages:
        note = frontmatter(f"Seite {page_no}", source, page_no,
                           ["ufc-pi", "rohtext"])
        note += f"# Seite {page_no}\n\n{text}\n"
        (raw_dir / f"Seite {page_no:03d}.md").write_text(note, encoding="utf-8")

    index = frontmatter(doc_title, source, len(pages), ["ufc-pi", "moc"])
    index += f"# {doc_title}\n\n"
    index += f"Quelle: `{source}`\n\n"
    index += f"{len(pages)} Seiten, {len(links)} Abschnitte.\n\n## Abschnitte\n\n"
    for candidate, title, page_range in links:
        link = candidate if candidate == title else f"{candidate}|{title}"
        index += f"- [[{link}]] — S. {page_range}\n"
    index += "\n## Rohtext\n\nSeitenweise Volltext im Ordner `Rohtext/`.\n"
    (out_dir / f"{doc_title}.md").write_text(index, encoding="utf-8")

    return len(links)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=pathlib.Path)
    parser.add_argument("--out", type=pathlib.Path, default=None,
                        help="Zielordner (Standard: Titel des Dokuments)")
    parser.add_argument("--title", default=None,
                        help="Titel der Index-Notiz (Standard: PDF-Dateiname)")
    args = parser.parse_args()

    if not args.pdf.exists():
        sys.exit(f"PDF nicht gefunden: {args.pdf}")

    doc_title = args.title or slugify(args.pdf.stem, "Dokument")
    out_dir = args.out or pathlib.Path(doc_title)

    pages = extract_pages(args.pdf)
    if not any(text for _, text in pages):
        sys.exit("Kein Text extrahierbar — das PDF ist vermutlich gescannt "
                 "und braucht vorher OCR (z. B. ocrmypdf).")

    sections = split_sections(pages)
    count = write_notes(sections, pages, out_dir, doc_title, args.pdf.name)
    print(f"{count} Abschnittsnotizen + {len(pages)} Rohtextseiten "
          f"geschrieben nach {out_dir}/")


if __name__ == "__main__":
    main()
