# AI-synlegheit

## Det finst ikkje éin kanal – det finst tre

| kanal | korleis han les butikken | kva som avgjer |
|---|---|---|
| **Direkte crawl** – GPTBot, PerplexityBot, ClaudeBot, CCBot | rå HTML, **køyrer ikkje JavaScript** | står fakta i kjeldekoden? |
| **Bing-indeksen** – ChatGPT-søk, Copilot | Bing sin indeks | er butikken i Bing i det heile? |
| **Agentlaget** – handleagentar | strukturert katalogdata frå plattforma | har produktdataa det agenten treng å matche på? |

Ein revisjon som berre ser på det første, er halvferdig.

## Test kvar kanal, ikkje anta

**Crawl:** hent sida utan JavaScript og søk etter dei strengane som ber salet
(`scripts/audit.py --money`). Fakta som berre finst i eit `<script>` finst ikkje for denne kanalen.

**Bing:** er Webmaster Tools sett opp? Importknapp frå Search Console. Gratis, fem minutt, og det er
heile døra til ChatGPT-søk.

**Agentlaget:** Shopify eksponerer `/agents.md`, `/.well-known/ucp` og `/api/ucp/mcp`. Lista
verktøya med eit `tools/list`-kall:

```bash
curl -s -X POST https://butikk.no/api/ucp/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Sjekk så kva katalogen faktisk serverer – `https://butikk.no/products/<handle>.js` viser same
felta: tittel, type, tags, varianttitlar og beskriving. Spør: **kan ein agent matche det kunden
faktisk spør om?** Ein agent som blir bedt om «socks for a 22 inch calf» ser varianten «Black / 5XL»
og har ingen måte å vite at 5XL er 26–29 tommar – med mindre tala står i produktteksten.

## Det som verkar

1. **Få måltala inn i tekst som følgjer produktet.** Same grep løyser crawl-kanalen og agentkanalen.
   Ei spesifikasjonsside server-rendra som ekte HTML, pluss éi setning med tal i kvar produkttekst.
2. **Bing.**
3. **Entitetskopling:** lenkjer frå butikken til dei sosiale profilane, og `sameAs` i
   Organization-markupen, slik at kjeldene peikar på kvarandre. Lenk aldri til ein tom profil –
   publiser innhaldet der først.
4. **Konsistens:** same namn, adresse, e-post og leveringstid på nettstaden, i profilane og i
   handelskontoane. Modellar byggjer tillit av at kjeldene seier det same.

## Den fjerde kanalen: blir butikken *tilrådd*?

Dei tre kanalane over handlar om å bli **funnen**. Det finst eit fjerde spørsmål, og det er det
ein eigar faktisk stiller: *spør eg ChatGPT om butikken min, kva svarar ho?*

Svaret er ofte ein variant av **«eg fann ikkje nok uavhengig dokumentasjon til å seie at dette er
ein trygg butikk»**. Det er ikkje eit SEO-problem, og ingen av grepa i denne skillen flyttar det.
Modellen leiter **utanfor domenet**, og alt du gjer på di eiga side er per definisjon partisk.

**Test det på same måten som alt anna – spør, og noter svaret ordrett.** Det er målinga. Gjenta
etter tiltaka, og sjå om formuleringa endrar seg.

### Sjekklista modellen går gjennom

| Signal | Korleis du sjekkar det |
|---|---|
| Uavhengige omtalar (Trustpilot, Sitejabber, BBB) | finst profilen i det heile? |
| Utgåande lenkjer til eigne sosiale profilar | `grep` etter `href="http` og trekk frå eige domene |
| `sameAs` i Organization-markup | ofte **tomme strengar**, ikkje manglande felt – sjå under |
| Postadresse og telefon i markup | `address`, `telephone` |
| Namngitt menneske eller firma nokon stad | om-sida, kontaktsida, botnteksten |
| Land | ofte berre antyda av opningstider i ei tidssone |
| Domenealder | `whois \| grep -i 'creation date'` |
| Omtalane på sida | er dei importerte frå leverandøren? Då tel dei ikkje |

**Fella med `sameAs`:** eit Shopify-tema fyller `sameAs` frå dei sosiale lenkjefelta i
temainnstillingane. Står dei tomme, får du ikkje eit manglande felt – du får **ein tabell med tomme
strengar**, som ser ut som markup og ikkje er det. Sjekk verdiane, ikkje berre at nøkkelen finst.

### Kva som faktisk flyttar det, i rekkjefølgje

1. **Ein tredjepartsprofil som finst.** Gratis, kort tid. Sjølv utan omtalar er det ein
   verifiserbar stad å slå opp, og det er det modellen leiter etter.
2. **Eit namngitt menneske eller firma, med land.** Det billegaste tillitssignalet som finst – men
   **spør eigaren først**, både om namnet og om adressa. Mange butikkar er registrerte på ein
   privatadresse, og det er eigaren si avgjerd å publisere henne, ikkje di.
3. **Ekte omtalar frå ekte kjøp.** Alt anna er kosmetikk, og ein ny butikk har som regel ingen.
4. **Tid.** Eit fire månader gammalt domene ser ut som eit fire månader gammalt domene.

### Det du ikkje gjer

Dikt aldri opp omtalar, kundar, namn eller tal for å tette hòlet. I USA er det forbode etter
**16 CFR Part 465** (i kraft oktober 2024), med bøter per brot. Og reint praktisk: ein modell som
finn oppdikta omtalar skriv noko verre om butikken enn at ho ikkje fann nok dokumentasjon.

**Sei det rett ut til eigaren:** når butikken er ny og utan ordrar, *finst* det ikkje noko
uavhengig å vise til. Svaret frå modellen er riktig. Det som endrar det, er dei første verkelege
kundane – ikkje meir arbeid på sida.

## Det som ikkje verkar, uansett kva nokon sel deg

**`llms.txt`.** På Shopify blir han allereie servert, identisk med `/agents.md`, og stien kan ikkje
overstyrast frå temaet. Konvensjonen er dessutan ikkje vedteken av OpenAI, Anthropic eller Google –
det finst ingen dokumentasjon på at han blir lesen. Ein fil som listar fakta som ikkje står på
sidene, hjelper ingen uansett.

**Å sikte mot «best X»-spørsmål.** Svarmotorane siterer nesten alltid tredjepartar på
produktanbefalingar – forumtrådar, samanlikningssider, redaksjonelle lister – og nesten aldri
butikken som sel varen. Ingen mengde arbeid på eiga side endrar det. Det krev omtale andre stader,
og det er ein annan jobb enn SEO.

**Å blokkere AI-crawlarane.** Argumentet mot dei gjeld nettstader som lever av annonsevisningar. Ein
butikk lever av å selje: ein modell som fortel nokon at butikken har rett storleik, gjer deg ei
teneste. Sjekk at `robots.txt` ikkje blokkerer dei ved eit uhell, og la dei vere i fred.

## Det ein butikk realistisk kan vinne

Dei konkrete, målbare spørsmåla der det finst eitt rett svar og butikken er den som har det:
mål, passform, spesifikasjonar, kompatibilitet, kva storleik som svarar til kva. Smalare mål enn
«best X», men eit ekte eit – og det krev at tala står som tekst.
