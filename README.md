# UFC PI Book 2018 — Obsidian-Import

Obsidian-Vault für den Import des *UFC Performance Institute Book 2018*.

## Status: Quelle nicht erreichbar

Die angefragte Datei `https://media.ufc.tv/ufcpi/UFCPI_Book_2018.pdf` konnte in
dieser Session **nicht geladen werden**. Der Egress-Proxy dieser Umgebung hat die
Verbindung mit `403` abgelehnt (Policy-Denial, nicht ein Fehler der Gegenstelle):

```
connect_rejected — gateway answered 403 to CONNECT — host: media.ufc.tv:443
```

Das betrifft das gesamte offene Internet in dieser Session, nicht nur diese Domain
(`example.com` und `www.ufc.com` werden identisch geblockt). Erlaubt sind nur
GitHub sowie die Paket-Registries.

Der Inhalt des PDFs ist daher **nicht** in diesem Vault enthalten — es wurde nichts
aus dem Gedächtnis rekonstruiert.

## So wird der Import abgeschlossen

Sobald das PDF lokal vorliegt (Download außerhalb dieser Umgebung, oder
`media.ufc.tv` auf die Allowlist der Umgebung setzen):

```bash
python3 -m venv .venv && .venv/bin/pip install pypdf
.venv/bin/python _scripts/pdf_to_obsidian.py UFCPI_Book_2018.pdf \
    --title "UFC PI Book 2018"
```

Das erzeugt:

- `UFC PI Book 2018/UFC PI Book 2018.md` — Index-Notiz (MOC) mit Wikilinks auf
  alle erkannten Abschnitte
- `UFC PI Book 2018/<Abschnitt>.md` — eine Notiz pro Kapitel, mit YAML-Frontmatter
  (`title`, `source`, `pages`, `imported`, `tags`) und Rücklink auf den Index
- `UFC PI Book 2018/Rohtext/Seite NNN.md` — seitenweiser Volltext als Fallback

Danach den Repo-Ordner in Obsidian als Vault öffnen.

## Hinweise

- Ist das PDF gescannt statt digital gesetzt, bricht das Skript mit einem Hinweis
  ab — dann vorher OCR laufen lassen (z. B. `ocrmypdf ein.pdf aus.pdf`).
- Die Abschnittserkennung ist eine Heuristik (kurze Zeilen in Versalien oder
  Title Case). Bei ungewohntem Layout liefert der `Rohtext/`-Ordner immer den
  vollständigen Text.
