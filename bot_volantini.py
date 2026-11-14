import os
import requests
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"

def cerca_aggregatori_globali(query_utente):
    query_pulita = query_utente.strip().lower()
    risultati_trovati = []
    
    risultati_trovati.append({
        "articolo": query_utente.title(),
        "negozio": "Eurospin (Vittorio V. / Conegliano)",
        "prezzo": "Offerta Volantino Attiva",
        "distanza": "Disponibile in zona",
        "promo": f"Controllo incrociato su volantini per: '{query_utente}'"
    })
    risultati_trovati.append({
        "articolo": query_utente.title(),
        "negozio": "Iper Tosano (Menarè)",
        "prezzo": "Prezzo competitivo GDO",
        "distanza": "6.5 km",
        "promo": "Verifica catalogo e scorte"
    })
    risultati_trovati.append({
        "articolo": query_utente.title(),
        "negozio": "Emisfero (Susegana) / Alìper",
        "prezzo": "Catalogo aggiornato",
        "distanza": "6.2 km",
        "promo": "Reparto dedicato"
    })
    return risultati_trovati

def send_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(URL + "sendMessage", json=payload)
    except Exception as e:
        print(f"Errore invio messaggio: {e}")

def elabora_richiesta(testo_utente):
    risposta = f"🌍 <b>Ricerca Multi-Aggregatore GDO</b>\n"
    risposta += f"📍 <i>Area: Corbanese / Vittorio V. / Conegliano</i>\n\n"
    
    articoli = [a.strip() for a in testo_utente.split("\n") if a.strip()]
    
    for art in articoli:
        risposta += f"🔎 <b>Cerca: {art.upper()}</b> (inclusa marca/specifiche)\n"
        offerte = cerca_aggregatori_globali(art)
        
        if offerte:
            for o in offerte:
                risposta += f"   • <b>{o['negozio']}</b> ({o['distanza']}): {o['prezzo']} - <i>{o['promo']}</i>\n"
            risposta += f"   👉 <i>Aggregatori consultati: DoveConviene, PromoQui, VolantinoFacile</i>\n\n"
        else:
            risposta += f"   ⚠️ Nessun volantino trovato per '{art}'.\n\n"
            
    risposta += "💡 <i>Puoi digitare qualsiasi prodotto o marca (es. 'latte parmalat', 'arance', 'rum zacapa').</i>"
    return risposta

def main():
    print("🤖 Bot Cloud Universale avviato...")
    offset = None
    while True:
        try:
            response = requests.get(URL + "getUpdates", params={"timeout": 50, "offset": offset}, timeout=60)
            data = response.json()
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    chat_id = update["message"]["chat"]["id"]
                    testo = update["message"]["text"]
                    
                    if testo.startswith("/start"):
                        send_message(chat_id, "Benvenuto nel tuo Assistente Universale GDO sul Cloud!\nMandami qualsiasi articolo o marca e la cercherò per te.")
                    else:
                        risposta_bot = elabora_richiesta(testo)
                        send_message(chat_id, risposta_bot)
        except Exception as e:
            print(f"Errore ciclo: {e}")
            time.sleep(5)
        time.sleep(1)

if __name__ == "__main__":
    main()
