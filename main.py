import requests, telebot, time

# Bot Token
token = "7768940127:AAGx69BeXWrp3eAUvnHYAAJg1-zN5s1NNYM"  # Replace with your bot token
bot = telebot.TeleBot(token)

loading_frames = [
    "[■□□□□□□□□□]",
    "[■■□□□□□□□□]",
    "[■■■□□□□□□□]",
    "[■■■■□□□□□□]",
    "[■■■■■□□□□□]",
    "[■■■■■■□□□□]",
    "[■■■■■■■□□□]",
    "[■■■■■■■■□□]",
    "[■■■■■■■■■□]",
    "[■■■■■■■■■■]"
]

def check_captcha(url):
    try:
        response = requests.get(url).text
        if 'https://www.google.com/recaptcha/api' in response or 'captcha' in response or 'verifyRecaptchaToken' in response or 'grecaptcha' in response or 'www.google.com/recaptcha' in response:
            return "❌ Captcha Detected"
        else:
            return "✅ No Captcha"
    except:
        return "❓ Error Checking Captcha"

def check_credit_card_payment(url):
    try:
        response = requests.get(url)
        if 'stripe' in response.text:
            return '💳 Stripe'
        elif 'Cybersource' in response.text:
            return '💳 Cybersource'
        elif 'paypal' in response.text:
            return '💳 PayPal'
        elif 'authorize.net' in response.text:
            return '💳 Authorize'
        elif 'Bluepay' in response.text:
            return '💳 Bluepay'
        elif 'Magento' in response.text:
            return '💳 Magento'
        elif 'woo' in response.text:
            return '💳 WooCommerce'
        elif 'Shopify' in response.text:
            return '💳 Shopify'
        elif 'adyan' in response.text or 'Adyen' in response.text:
            return '💳 Adyen'
        elif 'braintree' in response.text:
            return '💳 Braintree'
        elif 'square' in response.text:
            return '💳 Square'
        elif 'payflow' in response.text:
            return '💳 Payflow'
        elif 'payment by' in response.text or "credit card" in response.text:
            return '💳 Generic Payment'
        else:
            return '❌ No Payment Gateway Detected'
    except:
        return "❓ Error Checking Payment Gateway"

def check_cloud_in_website(url):
    try:
        response = requests.get(url)
        if 'cloud' in response.text.lower():
            return "🌥️ Cloud Detected"
        else:
            return "☁️ No Cloud Detected"
    except:
        return "❓ Error Checking Cloud"

@bot.message_handler(commands=['start'])
def start(message):
    # Display loading animation
    loading_msg = bot.send_message(message.chat.id, "Initializing...")
    for frame in loading_frames:
        time.sleep(0.5)
        bot.edit_message_text(frame, chat_id=message.chat.id, message_id=loading_msg.message_id)

    # Send welcome message
    bot.send_message(
        message.chat.id,
        (
            "<strong>Welcome to the Multi-Check Bot!</strong> 🤖\n\n"
            "This bot allows you to check:\n"
            "- Captcha presence 🔐\n"
            "- Payment gateway details 💳\n"
            "- Cloud technology usage ☁️\n\n"
            "Send a list of URLs separated by spaces or newlines to start checking.\n\n"
            "Example:\n"
            "https://example.com\n"
            "https://shopify.com\n\n"
            "Developed by: Team Zyrex 🇮🇳"
        ),
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda m: True)
def mass_check(message):
    urls = message.text.split()  # Split input into a list of URLs

    # Show processing animation
    processing_msg = bot.send_message(message.chat.id, "🔄 Processing URLs...")
    for frame in loading_frames:
        time.sleep(0.3)
        bot.edit_message_text(frame, chat_id=message.chat.id, message_id=processing_msg.message_id)

    # Generate results
    results = []
    for url in urls:
        try:
            captcha = check_captcha(url)
            cloud = check_cloud_in_website(url)
            payment = check_credit_card_payment(url)
            results.append(
                f"<strong>🌐 URL:</strong> {url}\n"
                f"<strong>🔐 Captcha:</strong> {captcha}\n"
                f"<strong>☁️ Cloud:</strong> {cloud}\n"
                f"<strong>💳 Payment System:</strong> {payment}\n\n"
            )
        except Exception as e:
            results.append(f"<strong>🌐 URL:</strong> {url}\n❓ Error: {e}\n\n")

    # Send results
    bot.send_message(
        message.chat.id,
        "".join(results),
        parse_mode="HTML"
    )

bot.polling(True)
