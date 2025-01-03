##### GitHub autentikáció és repó inicializáló script. #####
#                                                          #
## Feltételek:                                             #
# 1. Telepítve van a Git a számítógépen.                   #
# 2. A Git elérhető a PATH környezeti változóban.          #
# 3. PowerShell futtatása engedélyezve van a számítógépen. #
#                                                          #
############################################################

# Indítási üzenet kiírása a felhasználónak. #
Write-Host "Git ellenorzes, varj egy pillanatot..." -ForegroundColor Cyan # Tájékoztató üzenet, hogy a folyamat elindult.

# Globális változó, amely nyomon követi, hogy létezik-e lokális git repó. #
$RepoExists = $false # Alapértelmezett érték, hogy még nincs repó.

# Függvény, amely ellenőrzi, hogy a Git telepítve van-e a rendszerre. #
function Check-GitInstalled {
    try {
        $gitVersion = git --version # A 'git --version' parancs futtatása a Git verzió ellenőrzésére.
        Write-Host "Git telepitve van: $gitVersion" # Ha a Git telepítve van, kiírja a verziószámot.
    } catch {
        Write-Host "A 'git' nincs telepitve, vagy nincs a PATH-ban. Telepitsd a Git-et a https://git-scm.com/ weboldalrol." # Hibaüzenet, ha a Git nincs telepítve.
        exit # A szkript kilép, ha a Git nincs telepítve.
    }
}

# Függvény, amely beállítja a Git globális konfigurációs adatait. #
function Configure-Git {
    $userName = Read-Host "Add meg a GitHub felhasznaloneved" # Bekéri a GitHub felhasználónevet a felhasználótól.
    $userEmail = Read-Host "Add meg a GitHub e-mail cimed" # Bekéri a GitHub e-mail címet.
    git config --global user.name $userName # Beállítja a globális konfigurációs 'user.name' értékét.
    git config --global user.email $userEmail # Beállítja a globális konfigurációs 'user.email' értékét.
    Write-Host "Globalis Git konfiguracio beallitva." # Tájékoztató üzenet a sikeres beállításról.
}

# Függvény, amely megadja a token létrehozási utasításokat. #
function Generate-TokenInstructions {
    Write-Host "Latogass el a kovetkezo oldalra a token letrehozasahoz: https://github.com/settings/tokens" # Kiírja a GitHub token generálási oldal URL-jét.
    Write-Host "Hozz letre egy uj Personal Access Token-t (PAT) a kovetkezo jogosultsagokkal:" # Tájékoztató a szükséges jogosultságokról.
    Write-Host "repo, delete_repo" # Szükséges jogosultságok felsorolása.
}

# Függvény, amely bekéri a GitHub tokent és ellenőrzi annak érvényességét. #
function Get-AndTestToken {
    $token = Read-Host "Add meg a letrehozott tokent" # Token bekérése a felhasználótól.
    $headers = @{ Authorization = "token $token" } # Az API hívás fejlécének beállítása a tokennel.
    $response = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers -Method Get # GitHub API kérés a felhasználói adatok lekérésére.

    if ($response -ne $null) { # Ha a válasz nem üres, a token érvényes.
        Write-Host "Token sikeresen ellenorizve." # Tájékoztató a sikeres ellenőrzésről.
        return $token # Az érvényes token visszaadása.
    } else {
        Write-Host "Hiba: A token nem ervenyes. Ellenorizd, hogy helyesen masoltad-e be." # Hibajelzés, ha a token nem érvényes.
        return Get-AndTestToken # Új token bekérése, rekurzív módon.
    }
}

# Függvény, amely ellenőrzi, hogy van-e lokális repó, vagy inicializálja azt. #
function Check-OrInitializeRepo {
    $currentDir = Get-Location # Az aktuális könyvtár lekérdezése.
    if (Test-Path "$currentDir\.git") { # Ellenőrzi, hogy létezik-e '.git' mappa a könyvtárban.
        Write-Host "Mar letezik egy git repo ebben a mappaban: $currentDir" # Tájékoztató, ha már van repó.
        $Global:RepoExists = $true # Beállítja a globális változót, hogy a repó létezik.
        return # Kilép a függvényből.
    }

    $response = Read-Host "Szeretnel letrehozni egy uj git repot ebben a mappaban? (i/n)" # Felhasználói választás bekérése.
    if ($response -eq "i") { # Ha a felhasználó igen-t választ.
        git init # Új git repó inicializálása.
        Write-Host "Lokalis git repo inicializalva." # Tájékoztató üzenet a sikeres inicializálásról.
    } else {
        Write-Host "A repo letrehozasa kihagyva." # Tájékoztató üzenet, ha a repó létrehozása kihagyva.
        exit # A szkript kilép.
    }
}

# Függvény, amely új távoli repót hoz létre, ha szükséges. #
function Create-RemoteRepo {
    param (
        [string]$Token # Paraméterként a token kerül átadásra.
    )

    if ($Global:RepoExists) { # Ellenőrzi, hogy már létezik-e lokális repó.
        Write-Host "Mar letezik egy git repo ebben a mappaban." # Tájékoztató üzenet, ha már létezik repó.
        Write-Host "A tavoli repo letrehozasa kihagyva." # Tájékoztató üzenet, hogy a távoli repó létrehozása kihagyva.
        Write-Host "Nyomj meg egy gombot a kilepeshez..." # Tájékoztató üzenet a kilépéshez.
        Read-Host # Felhasználói bemenet várása a kilépés előtt.
        exit # A szkript kilép.
    }

    Write-Host "A most létrehozásra kerülő repó PRIVÁT, azaz csak Te férsz hozzá!"
    $repoName = Read-Host "Add meg a tavoli repo nevet (alapertelmezett: 'Iskolai_fajlok')" # A távoli repó neve bekérése.
    if (-not $repoName) { $repoName = "Iskolai_fajlok" } # Alapértelmezett név beállítása, ha nincs megadva.

    $headers = @{ Authorization = "token $Token" } # Az API kérés fejlécének beállítása.
    $body = @{ name = $repoName; private = $true } | ConvertTo-Json -Depth 10 # A POST kérés adatainak előkészítése.
    $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $headers -Method Post -Body $body # POST kérés küldése az API-nak.

    if ($response -ne $null) { # Ha a válasz nem üres, a repó létrejött.
        Write-Host "Tavoli repo sikeresen letrehozva: $repoName" # Tájékoztató a sikeres létrehozásról.
        return $response.clone_url # A repó URL-jének visszaadása.
    } else {
        Write-Host "Hiba tortent a tavoli repo letrehozasakor." # Hibajelzés, ha a repó létrehozása sikertelen.
        exit # A szkript kilép.
    }
}

# Függvény, amely összekapcsolja a lokális és távoli repót. #
function Link-RemoteRepo {
    param (
        [string]$RemoteUrl # Paraméterként a távoli repó URL-je kerül átadásra.
    )

    git remote add origin $RemoteUrl # A távoli repó hozzáadása 'origin' néven.
    git branch -M main # Az alapértelmezett ág átnevezése 'main'-re.
    Set-Content -Path "README.md" -Value "# Uj repo`nEz az elso commit." # Új README.md fájl létrehozása.
    git add README.md # A README.md fájl hozzáadása a stage-hez.
    git commit -m "Elso commit" # Az első commit létrehozása.
    git push -u origin main # Az ág feltöltése a távoli repóra.
    Write-Host "Tavoli repo sikeresen osszekapcsolva es a 'main' ag feltoltve." # Tájékoztató a sikeres feltöltésről.
}

# Fő folyamat indítása. #
Check-GitInstalled # Ellenőrzi, hogy a Git telepítve van-e.
Configure-Git # Beállítja a Git globális konfigurációját.
Generate-TokenInstructions # Token létrehozási utasításokat ad.
$token = Get-AndTestToken # Bekéri és ellenőrzi a tokent.
Check-OrInitializeRepo # Ellenőrzi, hogy van-e lokális repó, vagy inicializálja azt.
$remoteUrl = Create-RemoteRepo -Token $token # Létrehoz egy távoli repót, ha szükséges.
Link-RemoteRepo -RemoteUrl $remoteUrl # Összekapcsolja a lokális és távoli repót.

# Befejezési üzenet. #
Write-Host "Minden kesz! Nyomj meg egy gombot a kilepeshez..." -ForegroundColor Green # Tájékoztató üzenet a sikeres befejezésről.
Read-Host # Felhasználói bemenet várása a kilépés előtt.
