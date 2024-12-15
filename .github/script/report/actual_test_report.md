---
draft: true
---
## Rapport 1 - Processtappen
*Doel: achterhalen welke processtappen nog helemaal niet zijn geïmplementeerd*

- ✅ Er bestaat een bestand met deze taxonomiecode op dit niveau 
- ⛔️ Er is geen enkel bestand met deze taxonomiecode op dit niveau 
- 🏳️ De taxonomiecode wordt niet aangeboden op dit niveau (X in de Dataset) 

| TC1 | Proces | Processtap | Niveau 1 | Niveau 2 | Niveau 3 |
| --- | --- | --- | --- | --- | --- |
| bg-24 | Beheerproces | Gebruiken beheersysteem | 🏳️ | ✅ | ✅ |
| ib-19 | Implentatieproces | Bouwen softwaresysteem | 🏳️ | ✅ | ✅ |


## Rapport 2 - Onderwerpen Catalogus
*Doel: Lijst met onderwerpen + gekoppelde taxonomie code voor inzicht in aangeboden onderwerpen.*
Bij kolom *TC2*, *Leertaken*, *Ondersteunende informatie*, *Procedurele informatie* en *Deeltaken* zijn drie tekens aanwezig om de drie HBO-i niveaus weer te geven

- ✅ Het onderwerp met taxonomie code wordt aangeboden op het aangegeven niveau 
- ⛔️ Het onderwerp met taxonomie code wordt **niet** aangeboden op het aangegeven niveau 
- 🏳️ Het onderwerp hoeft met deze taxonomie code niet aangeboden te worden op het aangegeven niveau 

| TC3 | TC1 | TC2 | Leertaken | Ondersteunende-informatie | Procedurele-informatie | Deeltaken |
| --- | --- | --- | --- | --- | --- | --- |
| Geen-Niveau | bg-24 | 🏳️ 🏳️ 🏳️ | 🏳️ 🏳️ 🏳️ | 🏳️ 🏳️ 🏳️ | 🏳️ 🏳️ 🏳️ | 🏳️ 🏳️ 🏳️ |
| Alleen-Niveau-Twee | bg-24 | 🏳️ ✅ 🏳️ | 🏳️ ⛔️ 🏳️ | 🏳️ ✅ 🏳️ | 🏳️ ✅ 🏳️ | 🏳️ ✅ 🏳️ |
| Niveau-Twee-En-Drie | bg-24 | 🏳️ ✅ ✅ | 🏳️ ✅ ✅ | 🏳️ ⛔️ ⛔️ | 🏳️ ✅ ✅ | 🏳️ ⛔️ ⛔️ |
| Ander-Eerste-Onderdeel | ib-19 | 🏳️ ✅ ✅ | 🏳️ ⛔️ ⛔️ | 🏳️ ⛔️ ⛔️ | 🏳️ ✅ ✅ | 🏳️ ⛔️ ⛔️ |


## Work-in-progress bestanden
Doel: De onderstaande bestanden hebben nog todo items in de markdown staan.
Deze todo items moeten nog worden afgehandeld.

| Status | File | Path | Taxonomie | Tags | Errors |
| --- | --- | --- | --- | --- | --- |
| 🔨 | 26. work-in-progress test | 3. Procedurele-informatie\26. work-in-progress test.md | N/A | N/A | No taxonomie found in file.<br>To-Do item(s) found in the file:<br>-=ENUM=- |


## Gefaalde bestanden
*Doel: De onderstaande bestanden zijn niet succesvol verwerkt.*

❌ Dit bestand bevat nog geen taxonomie code
⚠️ Dit bestand bevat een foute taxonomie code. Zie de *Errors* kolom om te weten wat er mis is
🟠 Dit bestand bevat een taxonomie code die niet toegevoegd hoeft te zijn

| Status | File | Path | Taxonomie | Tags |
| --- | --- | --- | --- | --- |
| ⚠️ | 10. Taxonomie code zonder onderwerp (tc-3) | 2. Ondersteunende-informatie\10. Taxonomie code zonder onderwerp (tc-3).md | bg-24.2.OI | N/A | Invalid taxonomie: bg-24.2.OI |
| ⚠️ | 11. Taxonomie code zonder niveau (tc-2) | 2. Ondersteunende-informatie\11. Taxonomie code zonder niveau (tc-2).md | bg-24.Alleen-Niveau-Twee.OI | N/A | Invalid taxonomie: bg-24.Alleen-Niveau-Twee.OI |
| ⚠️ | 12. Taxonomie code zonder tc-1 | 2. Ondersteunende-informatie\12. Taxonomie code zonder tc-1.md | 2.Alleen-Niveau-Twee.OI | N/A | Invalid taxonomie: 2.Alleen-Niveau-Twee.OI |
| ⚠️ | 13. Taxonomie code met 0 in tc-1 | 2. Ondersteunende-informatie\13. Taxonomie code met 0 in tc-1.md | bg-0.2.Alleen-Niveau-Twee.OI | N/A | Taxonomie not found in dataset: bg-0.2.Alleen-Niveau-Twee.OI |
| ⚠️ | 14. Taxonomie code met spaties in tc-3 | 2. Ondersteunende-informatie\14. Taxonomie code met spaties in tc-3.md | bg-24.2.Alleen Niveau Twee.OI | N/A | Invalid taxonomie: bg-24.2.Alleen Niveau Twee.OI |
| ⚠️ | 15. Taxonomie code tussen tc-1 en tc-2 | 2. Ondersteunende-informatie\15. Taxonomie code tussen tc-1 en tc-2.md | bg-24. 2.Alleen-Niveau-Twee.OI | N/A | Invalid taxonomie: bg-24. 2.Alleen-Niveau-Twee.OI |
| ⚠️ | 16. Taxonomie code tussen tc-2 en tc-3 | 2. Ondersteunende-informatie\16. Taxonomie code tussen tc-2 en tc-3.md | bg-24.2. Alleen-Niveau-Twee.OI | N/A | Invalid taxonomie: bg-24.2. Alleen-Niveau-Twee.OI |
| ⚠️ | 17. Taxonomie code tussen tc-3 en tc-4 | 2. Ondersteunende-informatie\17. Taxonomie code tussen tc-3 en tc-4.md | bg-24.2.Alleen-Niveau-Twee. OI | N/A | Invalid taxonomie: bg-24.2.Alleen-Niveau-Twee. OI |
| 🟠 | 18. Taxonomie code die niet behandeld hoeft te worden | 2. Ondersteunende-informatie\18. Taxonomie code die niet behandeld hoeft te worden.md | bg-24.2.Geen-Niveau.OI<br>bg-24.3.Alleen-Niveau-Twee.OI | HBO-i/niveau-2<br>Beheerproces<br>Gebruiken beheersysteem<br>Geen-Niveau<br>HBO-i/niveau-3<br>Alleen-Niveau-Twee<br>bg-24.2.Geen-Niveau.OI<br>bg-24.3.Alleen-Niveau-Twee.OI | Taxonomie code used when not needed: bg-24.2.Geen-Niveau.OI<br>Taxonomie code used when not needed: bg-24.3.Alleen-Niveau-Twee.OI |
| ⚠️ | 2. Taxonomie code op negatief niveau | 2. Ondersteunende-informatie\2. Taxonomie code op negatief niveau.md | bg-24.-2.Alleen-Niveau-Twee.OI | N/A | Invalid taxonomie: bg-24.-2.Alleen-Niveau-Twee.OI |
| ❌ | 21. Fouten in dynamisch link opgelost | 4. Deeltaken\21. Fouten in dynamisch link opgelost.md | N/A | N/A | Invalid dynamic link: `[[foutieveLinkEen]]`<br>Invalid dynamic link: `[[foutieveLinkTwee]]`<br>No taxonomie found in file. |
| ⚠️ | 22. Twee taxonomie codes met fouten | 2. Ondersteunende-informatie\22. Twee taxonomie codes met fouten.md | bg-0.2.Alleen-Niveau-Twee.OI<br>bg-24.2.Alleen-Niveau-Twee.JH | N/A | Taxonomie not found in dataset: bg-0.2.Alleen-Niveau-Twee.OI<br>Invalid taxonomie: bg-24.2.Alleen-Niveau-Twee.JH |
| ❌ | 25. 2 van de 5 images gebruikt | 4. Deeltaken\25. 2 van de 5 images gebruikt.md | N/A | N/A | No taxonomie found in file. |
| ⚠️ | 27. Taxonomie code in verkeerde 4CID onderdeel | 1. Leertaken\27. Taxonomie code in verkeerde 4CID onderdeel.md | bg-24.2.Alleen-Niveau-Twee.LT<br>bg-24.2.Alleen-Niveau-Twee.OI | HBO-i/niveau-2<br>Beheerproces<br>Gebruiken beheersysteem<br>Alleen-Niveau-Twee<br>bg-24.2.Alleen-Niveau-Twee.LT<br>bg-24.2.Alleen-Niveau-Twee.OI | 4C/ID component from taxonomie not matching with 4C/ID folder: bg-24.2.Alleen-Niveau-Twee.LT<br>4C/ID component from taxonomie not matching with 4C/ID folder: bg-24.2.Alleen-Niveau-Twee.OI |
| ⚠️ | 3. Taxonomie code op niveau 0 | 2. Ondersteunende-informatie\3. Taxonomie code op niveau 0.md | bg-24.0.Alleen-Niveau-Twee.OI | N/A | Invalid taxonomie: bg-24.0.Alleen-Niveau-Twee.OI |
| ⚠️ | 4. Taxonomie code op niveau 4 | 2. Ondersteunende-informatie\4. Taxonomie code op niveau 4.md | bg-24.4.Alleen-Niveau-Twee.OI | N/A | Invalid taxonomie: bg-24.4.Alleen-Niveau-Twee.OI |
| ⚠️ | 5. Taxonomie code met negatieve tc-1 | 2. Ondersteunende-informatie\5. Taxonomie code met negatieve tc-1.md | bg--24.2.Alleen-Niveau-Twee.OI | N/A | Invalid taxonomie: bg--24.2.Alleen-Niveau-Twee.OI |
| ⚠️ | 6. Taxonomie code met verkeerd tc-1 nummer | 2. Ondersteunende-informatie\6. Taxonomie code met verkeerd tc-1 nummer.md | bg-19.2.Alleen-Niveau-Twee.OI | N/A | Taxonomie not found in dataset: bg-19.2.Alleen-Niveau-Twee.OI |
| ⚠️ | 7. Taxonomie code met niet bestaand onderwerp | 2. Ondersteunende-informatie\7. Taxonomie code met niet bestaand onderwerp.md | bg-24.2.Dit-Onderwerp-Bestaat-Niet.OI | N/A | Taxonomie not found in dataset: bg-24.2.Dit-Onderwerp-Bestaat-Niet.OI |
| ⚠️ | 8. Taxonomie code met een niet bestaand 4CID component | 1. Leertaken\8. Taxonomie code met een niet bestaand 4CID component.md | bg-24.2.Alleen-Niveau-Twee.JH | N/A | Invalid taxonomie: bg-24.2.Alleen-Niveau-Twee.JH |
| ⚠️ | 9. Taxonomie code zonder 4CID component (tc-4) | 1. Leertaken\9. Taxonomie code zonder 4CID component (tc-4).md | bg-24.2.Alleen-Niveau-Twee | N/A | Invalid taxonomie: bg-24.2.Alleen-Niveau-Twee |


## Gefaalde images
*Doel: De onderstaande images missen een 4C/ID component.*

Als een image de error heeft over het niet gebruikt worden, betekent dit dat de image niet in build staat, maar nog wel in content.

| Status | Image | Path | Error |
| --- | --- | --- | --- |
| 🏳️ | OI_test_image_2 | 4. Deeltaken\src\OI_test_image_2.png | Image not used in any file |
| 🏳️ | PI_test_image_4 | 4. Deeltaken\src\PI_test_image_4.png | Image not used in any file |
| 🏳️ | test_image_1 | 4. Deeltaken\src\test_image_1.png | Image not used in any file |
| ❌ | test_image_3 | 4. Deeltaken\src\test_image_3.png | Image does not include 4C/ID component |


## Geslaagde bestanden
De onderstaande bestanden zijn succesvol verwerkt.

| Status | File | Path | Taxonomie | Tags |
| --- | --- | --- | --- | --- |
| ✅ | 1. Correct taxonomie codes | 3. Procedurele-informatie\1. Correct taxonomie codes.md | bg-24.2.Alleen-Niveau-Twee.PI<br>bg-24.2.Niveau-Twee-En-Drie.PI<br>bg-24.3.Niveau-Twee-En-Drie.PI<br>ib-19.2.Ander-Eerste-Onderdeel.PI<br>ib-19.3.Ander-Eerste-Onderdeel.PI | HBO-i/niveau-2<br>Beheerproces<br>Gebruiken beheersysteem<br>Alleen-Niveau-Twee<br>Niveau-Twee-En-Drie<br>HBO-i/niveau-3<br>Implentatieproces<br>Bouwen softwaresysteem<br>Ander-Eerste-Onderdeel<br>bg-24.2.Alleen-Niveau-Twee.PI<br>bg-24.2.Niveau-Twee-En-Drie.PI<br>bg-24.3.Niveau-Twee-En-Drie.PI<br>ib-19.2.Ander-Eerste-Onderdeel.PI<br>ib-19.3.Ander-Eerste-Onderdeel.PI | N/A |
| ✅ | 19. Dezelfde taxonomie code twee keer | 4. Deeltaken\19. Dezelfde taxonomie code twee keer.md | bg-24.2.Alleen-Niveau-Twee.DT<br>bg-24.2.Alleen-Niveau-Twee.DT | HBO-i/niveau-2<br>Beheerproces<br>Gebruiken beheersysteem<br>Alleen-Niveau-Twee<br>bg-24.2.Alleen-Niveau-Twee.DT | N/A |
| ✅ | 20. Dezelfde taxonomie code twee keer, maar ander niveau | 1. Leertaken\20. Dezelfde taxonomie code twee keer, maar ander niveau.md | bg-24.3.Niveau-Twee-En-Drie.LT<br>bg-24.2.Niveau-Twee-En-Drie.LT | HBO-i/niveau-3<br>Beheerproces<br>Gebruiken beheersysteem<br>Niveau-Twee-En-Drie<br>HBO-i/niveau-2<br>bg-24.2.Niveau-Twee-En-Drie.LT<br>bg-24.3.Niveau-Twee-En-Drie.LT | N/A |
| ✅ | 23. Taxonomie code met al bestaande tag | 3. Procedurele-informatie\23. Taxonomie code met al bestaande tag.md | bg-24.2.Alleen-Niveau-Twee.PI | DezeTagMoetBlijvenBestaan<br>HBO-i/niveau-2<br>Beheerproces<br>Gebruiken beheersysteem<br>Alleen-Niveau-Twee<br>bg-24.2.Alleen-Niveau-Twee.PI | N/A |
| ✅ | 24. Taxonomie code met al bestaande tag gelijk aan het onderwerp | 2. Ondersteunende-informatie\24. Taxonomie code met al bestaande tag gelijk aan het onderwerp.md | bg-24.2.Alleen-Niveau-Twee.OI | Alleen-Niveau-Twee<br>HBO-i/niveau-2<br>Beheerproces<br>Gebruiken beheersysteem<br>bg-24.2.Alleen-Niveau-Twee.OI | N/A |


