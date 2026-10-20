#!/usr/bin/env python3
"""CYBER PHANTOM X 3.0 — defensive utilities for Termux and Kali Linux."""
import os, socket, hashlib, secrets, string, json, ipaddress
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    RED,GREEN,YELLOW,CYAN,MAGENTA,WHITE = Fore.RED,Fore.GREEN,Fore.YELLOW,Fore.CYAN,Fore.MAGENTA,Fore.WHITE
    RESET=Style.RESET_ALL
except ImportError:
    RED=GREEN=YELLOW=CYAN=MAGENTA=WHITE=RESET=""

try:
    import requests
except ImportError:
    requests=None
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except ImportError:
    phonenumbers=None

os.makedirs("reports", exist_ok=True)
def ask(s): return input(CYAN+s+RESET).strip()
def save(name,data):
    path=f"reports/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(path,"w",encoding="utf-8") as f: json.dump(data,f,indent=2,ensure_ascii=False)
    print(GREEN+"[+] Saved report: "+path+RESET)
def banner():
    os.system("cls" if os.name=="nt" else "clear")
    print(RED+r"""
   ▄████████  ▄██████▄   ▄█     █▄
  ███    ███ ███    ███ ███     ███
  ███    █▀  ███    ███ ███     ███
  ███        ███    ███ ███     ███
  ███        ███    ███ ███     ███
  ███    █▄  ███    ███ ███     ███
  ███    ███ ███    ███ ███     ███
  ████████▀   ▀██████▀   ▀██████▀
      ☠  CYBER PHANTOM X  ☠
""" + RESET)
    print(MAGENTA+"       VERSION 3.0 • MEGA EDITION"+RESET)
    print(YELLOW+" Defensive toolkit | Termux + Kali Linux\nUse only on systems you own or have permission to test.\n"+RESET)
def phone():
    print(YELLOW+"\n[ PHONE NUMBER INTELLIGENCE ]"+RESET)
    num=ask("Number with country code (example +9665XXXXXXXX): ")
    if not phonenumbers:
        print(RED+"Missing dependency. Run installer first."+RESET); return
    try:
        n=phonenumbers.parse(num,None)
        data={"input":num,"possible":phonenumbers.is_possible_number(n),"valid":phonenumbers.is_valid_number(n),
          "international":phonenumbers.format_number(n,phonenumbers.PhoneNumberFormat.INTERNATIONAL),
          "E164":phonenumbers.format_number(n,phonenumbers.PhoneNumberFormat.E164),
          "region":geocoder.description_for_number(n,"en"),"type":str(phonenumbers.number_type(n)),
          "carrier_if_available":carrier.name_for_number(n,"en"),"time_zones":list(timezone.time_zones_for_number(n)),
          "limitation":"No live GPS, owner identity, or home address can be derived from a phone number."}
        for k,v in data.items(): print(f"{GREEN}{k.replace('_',' ').title():24}{RESET}: {v}")
        save("phone",data)
    except Exception as e: print(RED+f"Could not parse number: {e}"+RESET)
def public_ip():
    if not requests: print("Install requirements first."); return
    try:
        r=requests.get("https://ipinfo.io/json",timeout=8); r.raise_for_status(); d=r.json()
        for k in ("ip","city","region","country","loc","org","timezone"):
            if k in d: print(f"{GREEN}{k:12}{RESET}: {d[k]}")
        print(YELLOW+"IP location is approximate, not live GPS."+RESET); save("public_ip",d)
    except Exception as e: print(RED+str(e)+RESET)
def dns():
    domain=ask("Domain name (example.com): ")
    if not domain or "/" in domain or " " in domain: print("Enter only a domain."); return
    try: import dns.resolver
    except ImportError: print("Install requirements first."); return
    data={"domain":domain,"records":{}}
    for typ in ("A","AAAA","MX","NS","TXT"):
        try: data["records"][typ]=[str(x) for x in dns.resolver.resolve(domain,typ,lifetime=4)]
        except Exception: data["records"][typ]=[]
    for k,v in data["records"].items(): print(f"{MAGENTA}{k}{RESET}: "+(", ".join(v) if v else "(none/unavailable)"))
    save("dns",data)
def website():
    url=ask("URL (https://example.com): ")
    if not url.startswith(("https://","http://")): url="https://"+url
    if not requests: print("Install requirements first."); return
    try:
        r=requests.get(url,timeout=8,allow_redirects=True,headers={"User-Agent":"CyberPhantomX/3.0"})
        wanted=("Strict-Transport-Security","Content-Security-Policy","X-Content-Type-Options","X-Frame-Options","Referrer-Policy","Permissions-Policy")
        d={"url":url,"final_url":r.url,"status":r.status_code,"security_headers":{h:r.headers.get(h,"MISSING") for h in wanted}}
        print("HTTP status:",r.status_code," Final URL:",r.url)
        for h,v in d["security_headers"].items(): print(f"{GREEN if v!='MISSING' else RED}{h:32}{RESET} {v}")
        save("website",d)
    except Exception as e: print(RED+str(e)+RESET)
def ports():
    host=ask("Authorized host/IP: ")
    try: ipaddress.ip_address(host)
    except ValueError:
        try: socket.getaddrinfo(host,None)
        except Exception: print("Host not resolved."); return
    raw=ask("Ports (comma-separated, max 30; e.g. 22,80,443): ")
    try:
        ps=sorted(set(int(x.strip()) for x in raw.split(",") if x.strip()))
        if not ps or len(ps)>30 or any(p<1 or p>65535 for p in ps): raise ValueError()
    except ValueError: print("Invalid ports."); return
    out=[]
    for p in ps:
        s=socket.socket(); s.settimeout(.7)
        try: status="open" if s.connect_ex((host,p))==0 else "closed/filtered"
        except Exception: status="error"
        finally: s.close()
        print(f"{GREEN if status=='open' else YELLOW}{p}: {status}{RESET}"); out.append({"port":p,"status":status})
    save("ports",{"host":host,"results":out})
def network():
    try:
        d={"hostname":socket.gethostname(),"local_ip_guess":socket.gethostbyname(socket.gethostname())}
        for k,v in d.items(): print(f"{GREEN}{k}: {v}{RESET}")
        print("For interface details on Linux, run: ip addr"); save("network",d)
    except Exception as e: print(str(e))
def password():
    try: n=int(ask("Password length (12-64): "))
    except ValueError: print("Enter a number."); return
    if not 12<=n<=64: print("Length must be 12-64."); return
    chars=string.ascii_letters+string.digits+"!@#$%^&*()-_=+"
    print(GREEN+"Generated password: "+WHITE+"".join(secrets.choice(chars) for _ in range(n))+RESET)
def file_hash():
    path=ask("Path to file: ")
    if not os.path.isfile(path): print("File not found."); return
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    digest=h.hexdigest(); print(GREEN+"SHA-256: "+digest+RESET)
    expected=ask("Expected SHA-256 (Enter to skip): ").lower()
    if expected: print(GREEN+"MATCH"+RESET if secrets.compare_digest(expected,digest) else RED+"NO MATCH"+RESET)
    save("file_hash",{"file":os.path.basename(path),"sha256":digest})
def lab():
    print("Safe practice: test only your own systems or systems with explicit permission.")
    print("Try website headers on your own site, file hashes, DNS records for a domain you manage, or localhost ports.")
def secret_menu():
    """Optional extra menu for benign/defensive utilities."""
    code = ask("Enter secret access code (or 0 to cancel): ")
    if code == "0":
        return
    # This is a demo access gate, not strong security; users can change it.
    expected = os.environ.get("CPX_SECRET_CODE", "CPX-2025")
    if code != expected:
        print(RED + "Access denied." + RESET)
        return
    while True:
        print(MAGENTA + """
╔══════════════════════════════════════════════╗
║          ☠ PHANTOM SECRET MENU ☠             ║
╠══════════════════════════════════════════════╣
║ [1] Phone number metadata                    ║
║ [2] Public IP metadata                       ║
║ [3] Website security header check            ║
║ [4] DNS record lookup                        ║
║ [5] File SHA-256 integrity check             ║
║ [0] Return to main menu                      ║
╚══════════════════════════════════════════════╝
""" + RESET)
        c = ask("SECRET > ")
        choices = {"1": phone, "2": public_ip, "3": website, "4": dns, "5": file_hash}
        if c == "0":
            return
        fn = choices.get(c)
        if fn:
            try:
                fn()
            except KeyboardInterrupt:
                print(YELLOW + "\\nCancelled." + RESET)
            input("\\nPress Enter to continue...")
        else:
            print(RED + "Invalid choice." + RESET)

def main():
    actions={"1":phone,"2":public_ip,"3":dns,"4":website,"5":ports,"6":network,
             "7":password,"8":file_hash,"9":lab}
    while True:
        banner()
        print(f"""{GREEN}[01]{WHITE} Phone Number Intelligence
{GREEN}[02]{WHITE} Public IP Intelligence
{GREEN}[03]{WHITE} DNS Lookup
{GREEN}[04]{WHITE} Website Security Headers
{GREEN}[05]{WHITE} TCP Port Check (authorized targets only)
{GREEN}[06]{WHITE} Local Network Information
{GREEN}[07]{WHITE} Secure Password Generator
{GREEN}[08]{WHITE} File SHA-256 Checker
{GREEN}[09]{WHITE} System & Security Lab
{GREEN}[10]{WHITE} Extra Tools
{GREEN}[11]{WHITE} Reports Center
{GREEN}[12]{WHITE} Settings / Help
{RED}[99]{WHITE} Secret Menu
{RED}[00]{WHITE} Exit
""")
        c=ask("PHANTOM > ")
        if c in ("0","00","q","exit"):
            print("Phantom signing off."); break
        if c == "99":
            try: secret_menu()
            except KeyboardInterrupt: print("\\nCancelled.")
            input("\\nPress Enter to continue...")
            continue
        if c == "10":
            print(MAGENTA + "\\n[ EXTRA TOOLS ]" + RESET)
            print("1. View Python/platform details")
            print("2. Show report files")
            print("0. Back")
            sub=ask("EXTRA > ")
            if sub=="1":
                import platform
                print("Python:", sys.version.split()[0], "| Platform:", platform.platform())
            elif sub=="2":
                reports = sorted(os.listdir("reports")) if os.path.isdir("reports") else []
                print("\\n".join(reports) if reports else "No reports saved yet.")
            input("\\nPress Enter to continue...")
            continue
        if c == "11":
            reports = sorted(os.listdir("reports")) if os.path.isdir("reports") else []
            print(MAGENTA + "\\n[ REPORTS CENTER ]" + RESET)
            print("\\n".join(reports) if reports else "No reports saved yet.")
            input("\\nPress Enter to continue...")
            continue
        if c == "12":
            print("Change the demo secret code with environment variable CPX_SECRET_CODE.")
            print("Example: CPX_SECRET_CODE='your-own-code' python main.py")
            print("This menu is not encryption or strong authentication.")
            input("\\nPress Enter to continue...")
            continue
        fn=actions.get(c)
        if fn:
            try: fn()
            except KeyboardInterrupt: print("\\nCancelled.")
            input("\\nPress Enter to continue...")
        else:
            input("Invalid choice. Press Enter...")
if __name__=="__main__":
    try: main()
    except KeyboardInterrupt: print("\nExiting.")
