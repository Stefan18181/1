# UFC PI Book 2018 — Obsidian-Import

Obsidian-Vault für den Import des *UFC Performance Institute Book 2018*.

## Status: aus Sekundärquellen recherchiert, PDF weiterhin nicht abrufbar

Die Datei `https://media.ufc.tv/ufcpi/UFCPI_Book_2018.pdf` konnte in dieser
Session **nicht geladen werden**. Der Egress-Proxy hat die Verbindung mit `403`
abgelehnt (Policy-Denial, kein Fehler der Gegenstelle):

```
connect_rejected — gateway answered 403 to CONNECT — host: media.ufc.tv:443
```

Das betrifft das gesamte offene Internet dieser Session, nicht nur diese Domain
(`example.com` und `en.wikipedia.org` werden identisch geblockt, auch über
WebFetch). Erlaubt sind GitHub und die Paket-Registries.

Funktioniert hat einzig die **serverseitige Websuche**. Der Ordner
`UFC PI Book 2018/` enthält daher 11 Notizen, die aus **öffentlicher
Berichterstattung über den Report** recherchiert sind — Inhaltsverzeichnis,
Datenbasis und die dokumentierten Kernbefunde, jede Zahl mit Quelle belegt.

**Nichts davon ist aus dem PDF extrahiert und nichts aus dem Gedächtnis ergänzt.**
Kapitel 3, 4 und 7 sind bewusst leer, weil sich zu ihnen keine belastbaren Daten
finden ließen. `UFC PI Book 2018/Offene Punkte.md` listet alle Lücken.

## So wird der Volltext-Import abgeschlossen

Sobald das PDF lokal vorliegt (Download außerhalb dieser Umgebung, oder
`media.ufc.tv` auf die Allowlist der Umgebung setzen):

```bash
python3 -m venv .venv && .venv/bin/pip install pypdf
.venv/bin/python _scripts/pdf_to_obsidian.py UFCPI_Book_2018.pdf \
    --out "UFC PI Book 2018 (Volltext)" --title "UFC PI Book 2018 Volltext"
```

Das erzeugt:

- `<Ordner>/UFC PI Book 2018 Volltext.md` — Index-Notiz (MOC) mit Wikilinks auf
  alle erkannten Abschnitte
- `<Ordner>/<Abschnitt>.md` — eine Notiz pro Kapitel, mit YAML-Frontmatter
  (`title`, `source`, `pages`, `imported`, `tags`) und Rücklink auf den Index
- `<Ordner>/Rohtext/Seite NNN.md` — seitenweiser Volltext als Fallback

Der separate Zielordner verhindert, dass der Import die recherchierten Notizen
überschreibt. Danach zusammenführen und in der Frontmatter `source_type: primär`
sowie `primary_source_retrieved: true` setzen.

Danach den Repo-Ordner in Obsidian als Vault öffnen.

## Hinweise

- Ist das PDF gescannt statt digital gesetzt, bricht das Skript mit einem Hinweis
  ab — dann vorher OCR laufen lassen (z. B. `ocrmypdf ein.pdf aus.pdf`).
- Die Abschnittserkennung ist eine Heuristik (kurze Zeilen in Versalien oder
  Title Case). Bei ungewohntem Layout liefert der `Rohtext/`-Ordner immer den
  vollständigen Text.
