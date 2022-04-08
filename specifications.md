# Zadání společné seminární práce KI/(K)APR2 2022

## základní zadání

Program pro hráče hry česká dáma, poskytující náhled na stav hry, jednoduchou interakci (provedení tahu) a také elementární umělou inteligenci (náhodná volba tahu bez podpory složitější strategie)

Pravidla české dámy viz [[Pravidla české dámy ČFD]](http://damweb.cz/pravidla/cdfull.html). Program by měl zohledňovat všechna pravidla ve článku 2, 3 a 4 (samozřejmě vyjma pravidel týkajících se fyzické interakce s figurami)

## povinná funkčnost

* načtení počáteční pozice z textového souboru ve formátu CSV (konkrétní formát viz níže)
* udržování stavu hry (pozice všech figur)
* nalezení všech možných tahů pro všechny figury na desce (včetně všech braní) a filtrování přípustných tahů (pravidlo o přednosti braní, přednost braní dámou)
* provedení tahu (aktualizace stavu hry)
* zobrazení (vizualizace) stavu hry
* náhodný výběr tahu (ze všech přípustných tahů v dané stavu)
* detekce výhry (všechny figury protivníka blokovány nebo protivník ztratil poslední figuru)

Program by měl podporovat hru dvou hráčů (každý z nich vybírá z přípustných tahů, poté co zvolí kámen jímž bude hrát) nebo jednoho hráče (místo druhého hráče se provede náhodný tvar). Po každém tahu se aktualizuje zobrazení stavu hry (resp. se zobrazí nové). Hra (partie) může být zahájena z libovolné možné pozice figura (dané obsahem CSV souboru). Pokud některý z hráčů dosáhne vítězství partie končí.

## formát CSV souboru

* na každém řádku je pozice jedné figury
* řádek má dvě pole oddělené čárkou, první určuje pozici v notaci české dámy (=šachová notace), druhý barvu a typ figury:
  * b = černý kámen
  * bb = černá dáma
  * w = bílý kámen
  * ww = bílá dáma

V souboru jsou přípustné prázdné řádky (= řádky tvořené jen mezerovými znaky)

Čtení musí skončit s výjimkou, pokud:

* neodpovídá výše uvedenému formátu
* figura je na nepřípustné pozici (bílé pole, aut)
* na herním poli je více než jedna figura

## Možná rozšíření (jsou zohledněny v rámci zkoušky)

Následující rozšíření jsou pouze návrhem, fantazii se samozřejmě meze nekladou.

### elementární rozšíření

* při náhodném tahu se preferují tahy s určitou taktickou výhodu, tj. například braní maximálního počtu soupeřových figur,  maximální postup kamene (tj. maximální přiblížení se k poslednímu řádku)
* přehlednější zobrazení v konzolovém výstupu (barvy,  vhodné Unicode znaky)
* záznam partie

### komplexnější rozšíření

* GUI/WEB rozhraní
* podpora hraní na síti

## Povinné implementační detaily

* figury musí být representovány objekty vlastních tříd s využitím dědičnosti (ze třídy Figura odvozené třídy Dáma a Kámen)
* pro representaci herního stavu je použito dvojrozměrné pole (např. seznam seznamů)
* možné tahy jsou representovány jako spojové stromy (obdoba binárních stromů s možností až čtyř dětských uzlů)

Jiří Fišer, 20.3. 2022
