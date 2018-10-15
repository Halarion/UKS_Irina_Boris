# Upravljanje Konfiguracijom Softvera - Predmetni Projekat
### Irina Marčeta, Boris Stajić


## 1. UVOD

Originalna ideja je bila da napravimo alat za 3ds max pomoću python-a ali to se pokazalo kao jako teško zbog
neadekvatne dokumentacije, nedostatka tutorijala i foruma, loših alata za testiranje itd.

Zbog toga smo se odlučili da koristimo Blender. Pošto je blender napisan na python-u vrlo je lako napisati dodatne funkcionalnosti,
dokumentacija je odlična, postoji puno tutorijala i objašnjenja online, greške je lako otkriti u konzoli itd.

Add-on koji smo napisali za Blender se zove CreatePlanets, pomoću njega je moguće praviti i animirati sfere po uzoru na zvezdani sistem.

## 2. "CREATE" DUGME

Na vrhu korisničkog interfejsa nalazi se dugme "CREATE". Pritiskom na ovo dugme prvo proveravamo da li su neki objekti na sceni selektovani. 
- Ako ni jedan objekat nije selektovan, ili ako je selektovano više objekata, skripta će napraviti novi "Empty" objekat i "Sferu" u koordinatnom početku sveta. Pošto se objekti u blenderu inače prave na mestu 3D kursora prvo smo učitali poziciju kursora u vektor "cursor", a zatim koristimo te koordinate da transliramo nove objekte u centar scene.
- Ako je selektovan tačno jedan objekat skripta će napraviti novi "Empty" objekat i sferu na poziciji selektovanog objekta.
Nakon toga će "Empty" objekat postati child selektovanog objekta, a sfera će postati child "Empty" objekta.

"Empty" objekat nam je potreban kako bi smo animirali revoluciju sfere oko selektovanog objekta.

## 3. PARAMETRI

U korisničkom interfejsu se nalaze 4 promenljiva parametra. To su: "Size","Orbit","Rotation Speed" i "Orbit Speed".
Sledi objašnjenje parametara.
- "Size" - Veličina sfere.
- "Orbit" - Udaljenost sfere od selekcije, odnosno orbita.
- "Rotation Speed" - Rotacija sfere oko sopstvene z-ose.
- "Orbit Speed" - Brzina kretanja sfere po orbiti.

Svaki od ovih parametra se čita u "main" funkciji programa a zatim se prosleđuje klasi "Planet", prilikom pravljenja objekta "MyPlanet" koja je zadužena da napravi i animira sfere. Nakon što se novi objekat napravi ovim parametrima je nemoguće pristupiti. Omogućiti korisiku da promeni parametre preko korisničkog interfejsa nakon što je objekat napravljen bi bila odlična funkcionalnost, ali njena implementacija je ostavljena za neku narednu verziju skripte.


## 4. ANIMACIJA

Za animaciju rotacije sfere oko svoje ose, upotrebljen je primer sa sledećeg linka: <https://www.youtube.com/watch?v=1rOc1b740Ds>

Definisan je početni i krajnji frejm, transformacija rotacije kao i osa oko koje se okreće sfera. U kodu je to z-osa. 
Zatim je pristupljeno 'GRAPH EDITOR'-u gde su krive promenjene da budu linearne, konkretno fcurves[0].select(True). Fcurves je sastavljen od splajnova koji povezuju keyframe-ove. Na kraju se vraćamo u 3D view, bpy.context.area.type = 'VIEW_3D'.
