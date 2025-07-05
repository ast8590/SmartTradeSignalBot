import time, random
from datetime import datetime
from telegram import Bot

TELEGRAM_BOT_TOKEN = "7663433863:AAFT0hUi6WsIQG5nlmoVIZi4IRXU1hyEFC8"
CHAT_ID = None
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def generate_fake_signal():
    pairs = ["XAUUSD", "EURUSD", "GBPUSD"]
    pair = random.choice(pairs)
    side = random.choice(["BUY", "SELL"])
    entry = round(random.uniform(1.07, 1.10), 5) if pair != "XAUUSD" else round(random.uniform(2350, 2370), 2)
    sl = entry + 0.0035 if side == "BUY" else entry - 0.0035
    tp1 = entry + 0.005 if side == "BUY" else entry - 0.005
    tp2 = entry + 0.01 if side == "BUY" else entry - 0.01
    reasons = ["Order Block", "Break of Structure", "Liquidity Sweep", "FVG + SMC", "Mitigation Zone"]

    signal = f"""📊 {pair} {side} SIGNAL

Entry: {entry}
Stop Loss: {round(sl,5)}
Take Profit 1: {round(tp1,5)}
Take Profit 2: {round(tp2,5)}
Reason: {random.choice(reasons)}
Time: {datetime.now().strftime('%Y‑%m‑%d %H:%M:%S')}"""
    return signal

def send_trade_signal(signal):
    global CHAT_ID
    if CHAT_ID:
        bot.send_message(chat_id=CHAT_ID, text=signal)
    else:
        print("⚠️ No chat ID yet — send /start to register.")

def listen_for_start_command():
    updates = bot.get_updates()
    for u in updates:
        if u.message and u.message.text == "/start":
            global CHAT_ID
            CHAT_ID = u.message.chat.id
            bot.send_message(chat_id=CHAT_ID, text="✅ Bot activated. You'll receive trade signals now.")
            print(f"Registered chat ID: {CHAT_ID}")

print("Bot started. Waiting for /start…")
while not CHAT_ID:
    listen_for_start_command()
    time.sleep(3)

while True:
    now = datetime.now()
    if now.minute % 15 == 0 and random.randint(0,10) > 8:
        sig = generate_fake_signal()
        send_trade_signal(sig)
    time.sleep(60)
