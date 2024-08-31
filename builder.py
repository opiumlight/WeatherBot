import logging
import weatherapi
import redis

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

r = redis.Redis(decode_responses=True)

configuration = weatherapi.Configuration()
configuration.api_key['key'] = config('API_KEY')
weather_api = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=RedisStorage.from_url('redis://localhost:6379/0'))
