---
name: nettbutikk-seo
description: Use when an online store needs an SEO and AI-visibility review, when asked "why don't we show up on Google", "will ChatGPT find us", "should we start a blog", or for a page-by-page SEO check, technical audit, structured-data check, or a fix list for an online store. Triggers on SEO-sjekk, SEO-gjennomgang, søkjemotoroptimalisering, synleg i Google, AI-synlegheit.
---

# SEO og AI-synlegheit for nettbutikkar

## Kjernen

Ein nettbutikk er usynleg av tre grunnar, og dei krev tre ulike svar: **han blir ikkje crawla**,
**han blir crawla men har ingenting å sitere**, eller **han har innhaldet men serverer det i
JavaScript**. Den tredje er den vanlegaste i Shopify-tema med app-seksjonar, og han er den som
hardast råkar AI-synlegheit, fordi AI-crawlarane ikkje køyrer JavaScript.

Du hentar alltid sidene slik ein crawler gjer: `curl` som Googlebot, utan nettlesar og utan
skjermbilete. Rendering kostar token og skjuler akkurat den feilen du leitar etter.

## Rekkjefølgja er ikkje valfri: plan → rapport → gjennomføring

Dei tre fasane er skilde, og du **stoppar mellom kvar**. Å hoppe rett til fiksar er den vanlegaste
måten å øydeleggje ein butikk som står i ein Merchant Center-gjennomgang eller midt i ein kampanje.

**Fase 1 – plan.** Skriv ein nummerert plan før du hentar éi einaste side: eitt punkt per sidetype,
kva fil kvar rapport skal ligge i, og kva som er **frose** (sjå under). Legg planen i prosjektet og
**vent på ja**.

**Fase 2 – rapport.** Eitt punkt om gongen. Hent, analyser, skriv rapporten til fil, oppsummer kort,
**stopp**. Ikkje fiks noko i denne fasen, uansett kor lite grepet er. Rekkjefølgja som fungerer:
framsida → kolleksjonar → dei viktigaste produktsidene → resten → statiske sider → teknisk →
AI-synlegheit → blogg-avgjerd → samla tiltaksliste.

**Fase 3 – gjennomføring.** Først no blir tiltaka nummererte punkt i planen, sorterte etter
**effekt delt på arbeid**, og gjort eitt om gongen med stopp etter kvart.

## Frosne felt: spør før du rører dei

Finn ut **først** om butikken står i ein Google Merchant Center-gjennomgang, ein Meta-ankesak eller
ein nyleg innsend verifisering. Går ein slik gjennomgang, er desse frosne til svaret kjem:
produkttittel, beskriving, pris, førpris, tilgjengelegheit, retur-/frakt-/personvernsider,
kontaktinfo og leveringslovnader. Ein gjennomgang samanliknar sida slik ho står **no** mot feeden.

Trygt likevel: kontooppsett utanfor sida (Bing, Search Console), språkfeil i grensesnittet, og
kolleksjonstitlar (dei ligg ikkje i feeden).

## Rapportformatet – dette er det som gjer rapporten verdt noko

Kvart funn skal ha fire delar, i denne rekkjefølgja:

1. **Kva eg fann** – bokstavleg, med kjelde (URL, felt, treffteljing).
2. **For** – kva vi vinn, og kor sikkert det er. Skil mellom *dokumentert hos Google*,
   *bransjevane* og *mi vurdering*.
3. **Imot** – kostnad, risiko, og kva som talar for å la det stå. Står det ingenting imot, skriv
   «ingenting imot» – ikkje tomrom.
4. **Tilråding** – eitt av: *gjer no* · *gjer etter gjennomgangen* · *gjer seinare* · ***gjer ikkje*.**

Ein rapport utan **imot**-ledd og utan minst eitt **gjer ikkje** er ikkje ferdig. Halvparten av
SEO-faget er vane, og den som les rapporten treng å vite kva som faktisk betalar seg.
Standard «gjer ikkje»-kandidatar: `llms.txt`, dobbel H1 i Dawn, `ItemList`-markup, meta description
på policysider, GTIN du ikkje har.

## Verktøyet

```bash
python3 scripts/audit.py https://butikk.no --discover \
  --money "mmHg;inch;Buy 1, get 1 FREE;30-day guarantee"
```

`--money` er dei strengane som ber salet. Kolonnene *money_js_only* og *money_absent* er der funnet
som regel ligg: fakta som finst for eit menneske, men ikkje for ein crawler.
`--discover` les `sitemap.xml`. `--json` gir fulle data per URL.

## Sjekklister og fiksar

- **Per sidetype:** `references/checklists.md` – kva du ser etter på framside, kolleksjon, produkt,
  statiske sider og teknisk.
- **Fiksane og fellene:** `references/shopify-fixes.md` – korleis kvart grep faktisk blir gjort på
  Shopify, og dei fellene som kostar ein heil økt om du ikkje veit om dei.
- **AI-synlegheit:** `references/ai-visibility.md` – dei tre kanalane, kva som verkar, og kva
  AI-SEO-bransjen sel som ikkje gjer det.

## Vanlege feil

| Feil | Kva som skjer |
|---|---|
| Hentar sidene i nettlesar | Du ser det JavaScript bygde, og går glipp av hovudfunnet |
| Fiksar medan du analyserer | Rapporten blir upåliteleg, og frosne felt blir rørte |
| Rapport som berre er ei gjeremålsliste | Mottakaren kan ikkje prioritere, og gjer det billegaste først |
| Finn på søkjevolum | Du har ikkje tal. Bruk band, og sei at det er ei vurdering |
| Måler fart ved å gjette | `content-length` manglar på komprimerte svar. Be om ein PageSpeed-køyring i staden |
| Byter variantnamn for søkjeord | Variantnamn heng i feeden, ordrehistorikken og leverandørkoplinga |
| Skriv til det publiserte temaet | Dupliser alltid, og sjekk MAIN-rolla på nytt rett før du skriv |
