
import requests

# Замените 'YOUR_API_TOKEN' на ваш реальный токен бота
API_TOKEN = '6711370288:AAH-K7ww2IiHJGvpxxk4saz713UrSdobO8I'
API_URL = f'https://api.telegram.org/bot{API_TOKEN}/'

def send_message(chat_id, text):
    url = f'{API_URL}sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

def get_updates(offset=None):
    url = f'{API_URL}getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def handle_message(message):
    chat_id = message['chat']['id']
    text = message.get('text', '')

    if text.startswith('/start'):
        send_message(chat_id, 'Hi! I am glad that you decided to use me!')
    elif text.startswith('/info'):
        info_text = (
            "I am a simple Telegram bot.\n"
            "I can echo messages back to you and provide basic help information.\n"
            "Use /help to see the list of available commands."
        )
        send_message(chat_id, info_text)
    elif text.startswith('/help'):
        help_text = (
            "/start - Start the bot\n"
            "/help - Get help information\n"
            "/echo <message> - Echo back the message you send\n"
            "/info - Get information about the bot"
        )
        send_message(chat_id, help_text)
    elif text.startswith('/echo'):
        args = text.split()[1:]
        if args:
            echo_text = ' '.join(args)
            send_message(chat_id, echo_text)
        else:
            send_message(chat_id, "Please provide a message to echo. Usage: /echo <message>")
    else:
        send_message(chat_id, "I don't understand that command. Use /help to see available commands.")

def main():
    print("Bot is running...")
    offset = None

    while True:
        updates = get_updates(offset)
        if 'result' in updates:
            for update in updates['result']:
                offset = update['update_id'] + 1
                if 'message' in update:
                    handle_message(update['message'])

if __name__ == "__main__":
    main()