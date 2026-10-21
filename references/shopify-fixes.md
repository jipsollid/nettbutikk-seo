# Fiksar på Shopify – korleis dei faktisk blir gjorde, og fellene

Samla frå ein full SEO-oppbygging av ein nettbutikk: grunnarbeidet, utvidinga og
revisjonen etterpå. Kvar felle her har kosta minst ei økt.

## Grunnarbeidet – rekkjefølgje som verkar

1. **Framsidetittel og meta description.** Dette er **shop**-innstillingar (Online Store →
   Preferences), ikkje tema-innstillingar, og **det finst ingen Admin API-mutasjon for dei**. Dei må
   tastast i admin. Nettlesaren automatiserer sida fint, men biletopplastinga for delingsbiletet
   lagar `input[type=file]` først ved klikk og opnar ein nativ filveljar – den må eigaren gjere sjølv.
2. **Produkt-SEO.** `seo.title` og `seo.description` per produkt via `productUpdate`. Hugs at
   plattforma legg på « – Butikknamn» når tittelen manglar merkenamnet; rekn det med i 60 teikn.
   Står `seo.description` tom, viser Google dei første ~320 teikna av brødteksten.
3. **Handles.** Importerte produkt gir ofte søkjeordspam-slugar («…-amazon-mens-and-womens-socks»). Byt dei
   med **`redirectNewHandle: true`** på `ProductInput` – då lagar plattforma 301-en sjølv.
   `collectionUpdate` har **ikkje** det feltet: der må du lage omdirigeringa med `urlRedirectCreate`.
4. **Kolleksjonar:** brødtekst + SEO-tittel + SEO-meta på alle. Ei setning i brødteksten, ikkje meir
   – sjå felle under.
5. **Alt-tekst i bulk.** Hent `media` **og** `variants { media }` per produkt, så kvart
   variantkopla bilete får den verkelege farge- eller mønsternemninga si; berre dei ukopla får ein
   generisk produktlinje. Skriv med `fileUpdate`. Over hundre bilete på éi økt er overkomeleg.
6. **Botnmeny.** About-sida er nesten alltid lenkja frå ingenting. Bygg menyen med `menuUpdate` –
   men sjekk at `footer-group.json` faktisk har ei `link_list`-blokk. Manglar blokka, renderer ingen
   meny uansett kor rett menyen er.
7. **Search Console.** Er Google & YouTube-kanalen kopla til, er eigarskapet alt verifisert med
   HTML-tagg – ingen DNS-post trengst. Send inn `sitemap.xml`; «Couldn't fetch» rett etterpå er
   normalt. Manuelle indekseringsførespurnader er rate-limiterte og endrar ikkje prioritet, så
   send inn eitt døme, ikkje heile katalogen.
8. **Bing Webmaster Tools.** Importknapp frå Search Console, under fem minutt, ingen ny
   verifisering. ChatGPT-søk køyrer på Bing-indeksen. Dette blir gløymt kvar gong.

## Fellene

**Temaet du skriv til er kanskje live.** Sjekk MAIN-rolla rett før **kvar** skriving – eigarar
publiserer midt i ei økt. Dupliser og arbeid i kopien.

**Forhandsvising med `curl` lyg.** `?preview_theme_id=<id>` serverer stille det **publiserte**
temaet. Bruk ein cookie-jar: hent preview-URL-en éin gong med `-c cj.txt -b cj.txt`, så hent sida
på nytt med same jar.

**Kolleksjonsskildringa lekk til framsida.** `featured-collection` har ofte
`show_description: true` og renderer **kolleksjonen** si skildring, ikkje seksjonen si. Ein lengre
kolleksjonstekst byter då stille ut linja på framsida. Vil du ha meir tekst på kolleksjonssida, legg
han i ein eigen seksjon under rutenettet.

**Å døype om ein kolleksjon bryt ikkje seksjonsinnstillingar.** Plattforma løyser innstillinga til
objektet, ikkje til den bokstavlege handla, så `templates/index.json` treng ikkje redigerast.

**App-seksjonar renderer i JavaScript.** Alt som blir sett inn med `innerHTML` – storleiksguidar,
tilbodsmerke, garantiboksar, omtalewidgetar – finst ikkje for ein AI-crawler, og tel lite når det i
tillegg startar `hidden`. Fiksen er å skrive ut innhaldet i mal-språket. Det er ein større jobb enn
det høyrest ut som, fordi dataa må flyttast frå ein JS-variabel til noko malen kan lese.

**Ikkje døyp om variantar for søkjeord.** Variantnamn heng saman med feeden, ordrehistorikken og
leverandørkoplinga. Vil du ha måltal inn der crawlarar og handleagentar ser dei, legg dei i
**produktteksten**.

**Dobbel H1 i Dawn-baserte tema.** Logoen i headeren ligg i `<h1>` på framsida. Google har sagt
fleire gonger at fleire H1-ar ikkje påverkar rangering, og fiksen krev omskriving av ei stor
kjernefil. **Gjer ikkje.** Det verkelege H1-problemet er nesten alltid at hero-overskrifta er eit
slagord utan emneord – det er ei tekstavgjerd, ikkje ei markup-avgjerd.

**Kunngjeringsbaren peikar ofte på `/collections/all`** – ei side utan tittel, utan meta og med alt
som er publisert, gåve- og testprodukt inkludert. Det er den sterkaste interne lenkja i butikken,
og ho peikar på den svakaste sida.

**Ei omdirigering taper mot eit levande produkt.** Set du opp 301 frå eit produkt du vil skjule,
verkar ho ikkje før produktet er avpublisert frå nettbutikken. Og før du avpubliserer: sjekk at
ingen temafunksjon (gåveveljarar, bundlar) treng varianten.

**Utkast-produkt lagar 404 bak 301.** Kvar gong eit produkt blir sett til utkast, peikar dei gamle
omdirigeringane rett i ein 404.

**Nokre mutasjonar blir blokkerte** av MCP-/tilgangslag – `themePublish`, `publishableUnpublish`,
statusendringar i bulk. Lag ei liste eigaren kan gjere i admin i staden for å prøve på nytt.

## Det som skal fiksast i ei bestemt rekkjefølgje

1. Kontooppsett utanfor sida (Search Console, Bing) – trygt når som helst.
2. Reine feil: feil språk i grensesnittet, tomme felt, 404 bak 301.
3. Innhald som gjer fakta synlege for crawlarar (den store jobben).
4. Metadata i bulk (titlar, meta descriptions).
5. Strukturerte data og entitetsmarkup – **etter** at adressa og namnet er endeleg avklara mot
   eventuelle plattformverifiseringar.
6. Rydding (foreldrelause kolleksjonar, tomme sider, omdirigeringar).
