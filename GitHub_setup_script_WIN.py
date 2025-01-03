### GitHub autentikáció és repó inicializáló script. ###
#                                                      #
## Feltételek a működéséhez:                           #
# Git: https://git-scm.com/download/win                #
# Python: https://www.python.org/downloads/            #
#                                                      # 
########################################################

import os  # Az 'os' modul importálása, amely fájlrendszerrel kapcsolatos műveleteket tesz lehetővé.
import subprocess  # Az 'subprocess' modul importálása, amely külső parancsok és folyamatok futtatását segíti.
import sys  # A 'sys' modul importálása, amely hozzáférést biztosít a Python fordítóval kapcsolatos alacsony szintű funkciókhoz.

# Ellenőrizzük, hogy a `requests` modul telepítve van-e, ha nem, akkor telepítjük
try:
    import requests  # A 'requests' modul importálása, amely HTTP kéréseket tesz lehetővé.
except ImportError:  # Ha az importálás sikertelen, mert a modul nincs telepítve.
    print("A 'requests' modul nincs telepítve, telepítés folyamatban...")  # Tájékoztató üzenet a felhasználónak.
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])  # A 'requests' modul telepítése a pip használatával.
    print("'requests' modul sikeresen telepítve!")  # Telepítés sikerességének visszajelzése.
    import requests  # A 'requests' modul újraimportálása, hogy biztosan használható legyen.

vanmarrepo = False # A repó létezésének ellenőrzésére szolgáló változó.

def check_git_installed():  # Függvény, amely ellenőrzi, hogy a Git telepítve van-e.
    try:
        result = subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # A 'git --version' parancs futtatása és annak kimenetének mentése.
        print("Git telepítve van:", result.stdout.decode().strip())  # A Git verziószámának kiírása.
    except FileNotFoundError:  # Ha a 'git' nincs telepítve, vagy nem elérhető a PATH-ban.
        print("A 'git' nincs telepítve, vagy nincs a PATH-ban. Telepítsd a Git-et a https://git-scm.com/ weboldalról.")
        # Felhasználói tájékoztató üzenet.
    except subprocess.CalledProcessError as e:  # Ha a 'git' futtatása hibát eredményez.
        print("Hiba történt a 'git' futtatása során:", e.stderr.decode().strip())  # A hibaüzenet kiírása.

def configure_git():  # Függvény, amely a Git globális konfigurációját állítja be.
    user_name = input("Add meg a GitHub felhasználóneved: ")  # A felhasználónév bekérése.
    user_email = input("Add meg a GitHub e-mail címed: ")  # Az e-mail cím bekérése.
    subprocess.run(["git", "config", "--global", "user.name", user_name], check=True)  # A globális 'user.name' beállítása.
    subprocess.run(["git", "config", "--global", "user.email", user_email], check=True)  # A globális 'user.email' beállítása.
    print("Globális Git konfiguráció beállítva.")  # Visszajelzés a sikeres beállításról.

def generate_token_instructions():  # Függvény, amely token generálási utasításokat ad.
    print("Látogass el a következő oldalra a token létrehozásához: https://github.com/settings/tokens")
    # Tájékoztatás a token létrehozási folyamatról.
    print("Hozz létre egy új Personal Access Token-t (PAT) a következő jogosultságokkal:")  # Jogosultságok felsorolása.
    print("repo, delete_repo")  # Szükséges jogosultságok.

def get_and_test_token():  # Függvény, amely bekéri és ellenőrzi a GitHub token érvényességét.
    token = input("Add meg a létrehozott tokent: ")  # A token bekérése a felhasználótól.
    headers = {"Authorization": f"token {token}"}  # Az API kérés fejlécének beállítása a tokennel.
    response = requests.get("https://api.github.com/user", headers=headers)
    # HTTP GET kérés küldése az API-nak a token ellenőrzésére.

    if response.status_code == 200:  # Ha a válaszkód 200, a token érvényes.
        print("Token sikeresen ellenőrizve.")  # Sikeres ellenőrzés visszajelzése.
        return token  # Az érvényes token visszaadása.
    else:  # Ha a válaszkód nem 200.
        print("Hiba: A token nem érvényes. Ellenőrizd, hogy helyesen másoltad-e be.")  # Hibajelzés a felhasználónak.
        return get_and_test_token()  # Újabb token bekérése rekurzívan.

def check_or_initialize_repo():  # Függvény, amely ellenőrzi, hogy van-e git repó, vagy inicializálja azt.
    current_dir = os.getcwd()  # Az aktuális munkakönyvtár elérése.
    if os.path.exists(os.path.join(current_dir, ".git")):
        # Ellenőrzi, hogy a '.git' mappa létezik-e az aktuális könyvtárban.
        print(f"Már létezik egy git repó ebben a mappában: {current_dir}")  # Visszajelzés, ha már van repó.
        global vanmarrepo  # A globális változó használata.
        vanmarrepo = True # A repó létezésének változója igazra állítása.
        return  # Kilépés a függvényből.

    response = input("Szeretnél létrehozni egy új git repót ebben a mappában? (i/n): ")
    # Bekérés, hogy akar-e új repót.
    if response.lower() == "i":  # Ha az input 'i' (igen).
        subprocess.run(["git", "init"], check=True)  # Új git repó inicializálása.
        print("Lokális git repó inicializálva.")  # Visszajelzés a sikeres inicializálásról.
    else:  # Ha az input nem 'i'.
        print("A repó létrehozása kihagyva.")  # Tájékoztatás a repó kihagyásáról.
        exit()  # A program befejezése.

def create_remote_repo(token):  # Függvény, amely új távoli repót hoz létre a GitHub-on.
    global vanmarrepo  # A globális változó használata.
    if vanmarrepo == True:
        print("Már van egy git repó ebben a mappában.")  # Visszajelzés, ha már van repó.
        print("A távoli repó létrehozása kihagyva.")  # Tájékoztatás a távoli repó kihagyásáról.
        print("Az autentikáció és a lokális repó inicializálása sikeres volt.")  # Visszajelzés az eddigi lépésekről.
        print("A program befejezéséhez nyomj meg egy billentyűt.")  # Kilépési utasítás.
        input()  # Várakozás a kilépésre.
        exit() # Ha már van repó, akkor kilép a program.
    else: # Ha nincs repó.
        print("A most létrehozásra kerülő repó PRIVÁT, azaz csak Te férsz hozzá!")
        repo_name = input("Add meg a távoli repó nevét (alapértelmezett: 'Iskolai_fajlok'): ") or "Iskolai_fajlok"
        # Bekérés a repó nevéhez, vagy alapértelmezés beállítása.
        headers = {"Authorization": f"token {token}"}  # Fejléc beállítása a tokennel.
        data = {  # Az API kérés adatai.
            "name": repo_name,
            "private": True  # A repó privát lesz.
        }
        response = requests.post("https://api.github.com/user/repos", json=data, headers=headers)
        # POST kérés küldése az új repó létrehozásához.

        if response.status_code == 201:  # Ha a válaszkód 201, a repó sikeresen létrejött.
            print(f"Távoli repó sikeresen létrehozva: {repo_name}")  # Visszajelzés a sikeres repó létrehozásról.
            return response.json()["clone_url"]  # A repó klónozási URL-jének visszaadása.
        elif response.status_code == 422:  # Ha a válaszkód 422, már létezik ilyen nevű repó.
            print("Hiba: Már létezik egy ilyen nevű távoli repó.")  # Hibajelzés a felhasználónak.
            choice = input("Szeretnéd összekapcsolni a meglévő repóval? (i/n): ")  # Bekérés, hogy kapcsolódjon-e.
            if choice.lower() == "i":  # Ha az input 'i'.
                return f"https://github.com/USERNAME/{repo_name}.git"  # A meglévő repó URL-jének visszaadása.
            else:  # Ha az input nem 'i'.
                exit()  # A program befejezése.
        else:  # Ha más hiba történt.
            print("Hiba történt a távoli repó létrehozásakor.")  # Általános hibajelzés.
            print(response.json())  # A teljes hibaüzenet kiírása.
            exit()  # A program befejezése.

def link_remote_repo(remote_url):  # Függvény, amely összekapcsolja a lokális és távoli repót.
    subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
    # Távoli repó hozzáadása 'origin' néven.
    subprocess.run(["git", "branch", "-M", "main"], check=True)  # A fő ág átnevezése 'main'-re.
    with open("README.md", "w") as readme:  # Új 'README.md' fájl létrehozása és megnyitása írásra.
        readme.write("# Uj repo\nEz az elso commit.")  # Tartalom írása a README fájlba.
    subprocess.run(["git", "add", "README.md"], check=True)  # A README fájl hozzáadása a stage-hez.
    subprocess.run(["git", "commit", "-m", "Első commit"], check=True)  # Első commit létrehozása.
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
    # A fő ág feltöltése a távoli repóra.
    print("Távoli repó sikeresen összekapcsolva és a 'main' ág feltöltve.")  # Visszajelzés a sikeres összekapcsolásról.

def main():  # A fő program futtatása.
    check_git_installed()  # Ellenőrzi, hogy a Git telepítve van-e.
    configure_git()  # Beállítja a Git globális konfigurációját.
    generate_token_instructions()  # Utasításokat ad a token generálásához.
    token = get_and_test_token()  # Bekéri és ellenőrzi a GitHub tokent.
    check_or_initialize_repo()  # Ellenőrzi, hogy van-e git repó, vagy inicializálja azt.
    remote_url = create_remote_repo(token)  # Létrehoz egy új távoli repót, vagy csatlakozik egy meglévőhöz.
    link_remote_repo(remote_url)  # Összekapcsolja a lokális és távoli repót.

if __name__ == "__main__":  # Ellenőrzi, hogy a fájlt közvetlenül futtatják-e.
    main()  # A fő függvény meghívása.
