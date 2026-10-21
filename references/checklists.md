# Sjekklister per sidetype

Alt blir henta med `curl` som Googlebot. Køyr `scripts/audit.py` først – han tek det mekaniske –
og bruk listene under til det som krev auge.

## Felles for alle sider

- `<title>`: under 60 teikn **inkludert** det butikknamnet plattforma legg på automatisk.
- meta description: finst han i det heile? Er han skriven, eller er det dei første 320 teikna av
  brødteksten? Ein auto-snutt startar nesten alltid med problem-agitasjon og null produktfakta.
- canonical: sjølvpeikande og absolutt.
- `lang`-attributtet mot språket i teksten – og mot etikettane plattforma genererer.
- H1: éin med meining. Tel òg dei tomme (ein logo pakka i `<h1>` tel med).
- alt-tekst: tal bilete, tal utan alt.
- JSON-LD: typar, og om alle blokkene parserer.
- **Språkbrot:** søk etter ord frå eigarens morsmål i HTML-en. Filteretikettar, knappar og
  app-tekstar arvar ofte feil språk, og det er synleg for kunden.

## Framsida

- Står søkjeordet i H1, eller er H1 eit slagord utan emne?
- Ordtal i ekte brødtekst – ikkje produktkort.
- Kor mange produkt og kolleksjonar er faktisk lenkja?
- `sameAs` i Organization: tomme strengar er standard i mange tema, og dei er alltid tomme.
- Finst `BreadcrumbList`, `WebSite`/`SearchAction`?
- Dei konkrete tala (mål, spesifikasjonar, storleikar): står dei i teksten, eller berre i eit skript?

## Kolleksjonssider

- Har kvar kolleksjon **eigen** tekst, eller les dei som duplikat av kvarandre?
- Facett- og sorterings-URL-ar i HTML-en (`?filter.`, `?sort_by=`): kvar av dei er ein crawl-felle.
  Null er bra og vanlegare enn folk trur – sjekk før du «fiksar» noko.
- Paginering, `rel=next/prev`, canonical på side 2+.
- Dekkjer kolleksjonane alle produkta? Crawl-stien til produktsidene går som regel herifrå.
- Tel kolleksjonane mot talet på produkt. Åtte kolleksjonar over ti produkt betyr at kvart produkt
  ligg i fire nesten like rutenett, og at plattforma vel kva for ei som rankar.
- **Foreldrelause kolleksjonar:** sider som er tekne ut av menyen men framleis ligg i sitemapet.
  Å skjule noko i menyen er ikkje å avindeksere det.
- Ein kolleksjon med eitt produkt er ikkje ein kolleksjon – han er eit duplikat av produktsida.

## Produktsider

- `Product`/`ProductGroup`-markup: pris, valuta, `availability`, `sku`, bilete per variant.
- **`aggregateRating`: kvar kjem tala frå?** Importerte leverandøromtalar som blir sende ut som
  strukturerte stjerner er eit juridisk problem i USA (16 CFR Part 465, i kraft frå okt. 2024) og
  ein kjend utløysar for Merchant Center-flagg. Sjå etter mønsteret: blanke 5,0, ingen under 4,
  nokre sider med markup og andre utan.
- GTIN/MPN: har butikken dei i det heile? Har han dei ikkje, er svaret `identifier_exists: no` i
  **feeden**, ikkje oppdikta tal på sida.
- Ordtal og kva spørsmål teksten faktisk svarar på.
- **Helsepåstandar og liknande regulert språk** i produktteksten. Dette ligg i feeden.
- Storleiks-/spesifikasjonstabellar: server-rendra HTML, eller bygde i JavaScript og gøymde bak eit
  klikk? Dette er hovudfunnet i dei fleste revisjonar.

## Statiske sider (About, Contact, FAQ, vilkår)

Spørsmålet er ikkje rangering, men om butikken ser ut som ein verkeleg aktør.

- Finst ei ekte adresse, og står ho **identisk** alle stader?
- Finst det eit namngitt menneske?
- Same e-post overalt? Same leveringstid overalt, og stemmer ho med det leverandøren faktisk gjer?
- Står noko ope og ubehageleg (t.d. kvar omtalane kjem frå)? Det er eit pluss, ikkje eit minus.
- Er alt dette **berre brødtekst**? Nesten alltid ja – og då veit ingen maskin om det.
- Søkjeresultatsider: er `/search?q=` indekserbar?
- Tomme app-sider i sitemapet.

## Teknisk

- `robots.txt`: er crawl-fellene stengde, og er **AI-crawlarane ved eit uhell blokkerte**?
- Sitemap-indeks og alle barna. Ligg det tomme eller framandspråklege sider der?
- Omdirigeringar: test måla. Ein 301 inn i ein 404 er verre enn ingen 301, og det skjer kvar gong
  nokon set eit produkt til utkast.
- JSON-LD-validitet over alle sidene samla.
- Fart: **mål, ikkje gjett.** `content-length` manglar på komprimerte svar, og PSI-API-et har
  dagskvote. Be eigaren køyre `pagespeed.web.dev` og sende talet.
- Search Console og Bing Webmaster Tools: oppsett, indekseringstal, og
  «Crawled – currently not indexed», som skil crawl-problem frå kvalitetsproblem.
