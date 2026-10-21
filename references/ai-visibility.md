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
