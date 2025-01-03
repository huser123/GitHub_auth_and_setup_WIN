# GitHub Auth and Setup for Windows

Ez a repo egy PowerShell és egy Python scriptet tartalmaz, amelyek beállítják a Git-et és a GitHub-ot a Windows rendszereken.

## Fájlok

1. **Python Script (`GitHub_setup_script_WIN.py`)**
   - Ellenőrzi, hogy a Git telepítve van-e a rendszeren.
   - Beállítja a Git globális konfigurációját (felhasználónév és e-mail).
   - Segítséget nyújt a GitHub Personal Access Token (PAT) létrehozásához.
   - Bekéri és érvényesíti a megadott PAT-t.
   - Inicializál egy lokális Git repót, ha még nincs.
   - Létrehoz egy távoli repót a GitHubon és összekapcsolja a lokális repóval.
   - Feltölt egy alap README.md fájlt a `main` ágra.

2. **PowerShell Script (`GitHub_setup_script_WIN.ps1`)**
   - Ugyanezeket a funkciókat valósítja meg, mint a Python script, de PowerShell környezetben futtatható.

## Feltételek

- **Python Script futtatása**: Szükséges egy működő Python környezet, valamint a szükséges modul: `requests`.
- **PowerShell Script futtatása**: Szükséges egy Windows környezet PowerShell támogatással.
- **Előfeltételek**:
  - Git telepítve legyen és elérhető a PATH-ból.
  - A GitHub fiókhoz tartozó Personal Access Token (PAT) létrehozása szükséges a https://github.com/settings/tokens oldalon.
  - A `repo` és `delete_repo` jogosultságokkal rendelkező token szükséges a távoli repó kezeléséhez.
- **Telepítő csomagok**
  - Git: https://git-scm.com/download/win
  - Python: https://www.python.org/downloads/ 

## Használat

1. Futtasd az egyik scriptet a saját környezetedben (Python vagy PowerShell).
2. Kövesd az utasításokat a konfigurációs adatok (GitHub felhasználónév, e-mail, PAT) megadásához.
3. A script automatikusan létrehozza a távoli repót és feltölti az alapfájlokat.

## Figyelmeztetés

- A script automatikusan felülírja a meglévő globális Git konfigurációt, ha van.
- Ha egy megadott nevű távoli repó már létezik, figyelmeztetést ad és lehetőséget nyújt annak újrahasználatára.

Ez a repó kezdőknek és haladóknak egyaránt gyors és egyszerű megoldást ad a Git és GitHub konfigurációjához Windows rendszeren.
