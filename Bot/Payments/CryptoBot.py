from config import CRYPTOBOT_API_TOKEN
from aiocryptopay import AioCryptoPay, Networks
import asyncio

async def create_cryptobot_invoice(price):
    crypto = AioCryptoPay(token=CRYPTOBOT_API_TOKEN, network=Networks.MAIN_NET)
    fiat_invoice = await crypto.create_invoice(amount=price, fiat='USD', currency_type='fiat')
    await crypto.close()
    return {"url": fiat_invoice.bot_invoice_url,"id":fiat_invoice.invoice_id}

async def check_invoice(invoice_id):
    crypto = AioCryptoPay(token=CRYPTOBOT_API_TOKEN, network=Networks.MAIN_NET)
    invoice_info = await crypto.get_invoices(invoice_ids=invoice_id)
    await crypto.close()
    return invoice_info[0]