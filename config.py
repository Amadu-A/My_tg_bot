from environs import Env
import datetime


env = Env()
env.read_env()
BOT_TOKEN = env.str('BOT_TOKEN')
ADMIN_ID = env.list('ADMIN_ID')
IP = env.str('IP')
API_KEY = env.str('X-RAPIDAPI-KEY')


headers = {
        'x-rapidapi-host': 'hotels4.p.rapidapi.com',
        'x-rapidapi-key': API_KEY
    }
date_today = datetime.datetime.today().strftime('%Y-%m-%d')
date_tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
url_id_city = 'https://hotels4.p.rapidapi.com/locations/search'
url_detail = 'https://hotels4.p.rapidapi.com/properties/list'
url_locale = 'https://hotels4.p.rapidapi.com/get-meta-data'