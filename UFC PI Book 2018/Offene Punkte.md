---
title: "Offene Punkte"
imported: 2026-07-25
tags:
  - ufc-pi
  - todo
---

# Offene Punkte

Was ohne das Original-PDF fehlt. Diese Liste ist die Arbeitsgrundlage für den
Moment, in dem die Datei vorliegt.

> [!todo] Vereinbarter Stand (25.07.2026)
> Der aktuelle Inhalt ist ausdrücklich ein **Zwischenstand**. Die genaue
> Ausarbeitung ist auf später vertagt und braucht als Voraussetzung das
> Original-PDF — ohne die Datei ändert sich an den Lücken unten nichts, egal
> wie oft nachrecherchiert wird.
>
> Voraussetzung erfüllen durch **eine** der beiden Optionen:
> 1. `UFCPI_Book_2018.pdf` beschaffen und ins Repo-Root legen
> 2. `media.ufc.tv` auf die Egress-Allowlist der Umgebung setzen

## Ganz fehlende Kapitel

- [ ] [[03 Optimierung des Trainingsprozesses]] — komplett offen
- [ ] [[04 Steuerung des Trainingsprozesses]] — komplett offen
- [ ] [[07 Das UFC Performance Paradigm]] — komplett offen

## Lückenhafte Abschnitte

- [ ] **Benchmarks pro Gewichtsklasse** — der Report enthält Tabellen über alle
      Divisionen; belegt sind nur Extremwerte (LHW Sprungkraft, FW relative
      Kraft) → [[05 Physische Leistungs-Benchmarks]]
- [ ] **Judging-Metriken** — als Inhalt bestätigt, Zahlen fehlen →
      [[01 Winning in Todays UFC]]
- [ ] **Siegmethoden für die übrigen Divisionen** — belegt sind nur Middleweight,
      Heavyweight, Men's Flyweight → [[01 Winning in Todays UFC]]
- [ ] **Vollständige Rangliste der 167 Kampf-Metriken** — bekannt sind nur die
      Top-Indikatoren und Rang 19 für Takedowns
- [ ] **Zuordnung der Gewichtmach-Werte** zum 2018er Band statt zum 2021er
      Nachfolger → [[06 Performance Nutrition und Gewichtsmanagement]]
- [ ] **Acknowledgements / Autorenschaft** — wer den Report verfasst hat

## Zu verifizieren

- [ ] Ob die **10-%-Fight-Week-Aussage** bereits im 2018er Band steht oder erst
      2021 dazukam
- [ ] Ob die **Aktigraphie-Schlafstudie** im Report referenziert wird oder rein
      parallel publiziert wurde

## Wenn das PDF da ist

```bash
python3 -m venv .venv && .venv/bin/pip install pypdf
.venv/bin/python _scripts/pdf_to_obsidian.py UFCPI_Book_2018.pdf \
    --out "UFC PI Book 2018 (Volltext)" --title "UFC PI Book 2018 Volltext"
```

Bewusst in einen **separaten Ordner**, damit der Volltext-Import diese
recherchierten Notizen nicht überschreibt — danach zusammenführen und die
Frontmatter-Felder `source_type` / `primary_source_retrieved` aktualisieren.

---

Zurück zu [[UFC PI Book 2018]]
