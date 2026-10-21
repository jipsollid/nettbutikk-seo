# nettbutikk-seo

Ein Claude Code-skill for SEO- og AI-synlegheitsgjennomgang av nettbutikkar
(bygd for Shopify, men det meste gjeld alle nettbutikkar).

Han tvingar fram ei bestemt rekkjefølgje – **plan → rapport → gjennomføring**, med stopp mellom kvar
fase – og krev at kvart funn blir skrive som **kva eg fann → for → imot → tilråding**.
Ein rapport utan motargument og utan minst eitt «gjer ikkje» er ikkje ferdig.

## Installer

```bash
git clone git@github.com:<brukar>/nettbutikk-seo.git ~/.claude/skills/nettbutikk-seo
```

Start Claude Code på nytt. Kall han med `/nettbutikk-seo`, eller berre be om ein SEO-sjekk –
han blir funnen av seg sjølv.

Brukar du Claude i nettlesaren eller skrivebordsappen: last opp mappa som zip under
Innstillingar → Capabilities → Skills.

## Innhald

| fil | kva |
|---|---|
| `SKILL.md` | dei tre fasane, regelen om frosne felt, rapportformatet |
| `scripts/audit.py` | hentar sider som Googlebot, utan JavaScript. Berre standardbiblioteket |
| `references/checklists.md` | kva du ser etter per sidetype |
| `references/shopify-fixes.md` | korleis kvar fiks faktisk blir gjord, og fellene |
| `references/ai-visibility.md` | dei tre AI-kanalane, og kva som ikkje verkar |
| `references/plan-template.md` | ferdig plan til fase 1 |

## Skriptet åleine

Det fungerer utan Claude:

```bash
python3 scripts/audit.py https://butikk.no --discover \
  --money "mmHg;inch;Buy 1, get 1 FREE;30-day guarantee"
```

`--money` er dei strengane som ber salet. Kolonnene *berre i JavaScript* og *finst ikkje* er der
funnet som regel ligg: fakta som finst for eit menneske, men ikkje for ein crawler.

Køyr han berre mot butikkar du sjølv har ansvar for.
