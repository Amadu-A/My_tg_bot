from environs import Env
import datetime



env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMIN_ID = env.list('ADMIN_ID')
IP = env.str('IP')
API_KEY = env.str('X-RAPIDAPI-KEY2')
API_KEY_lst = [env.str('X-RAPIDAPI-KEY' + str(x)) for x in range(1, 4)]


headers = {
    'x-rapidapi-host': 'hotels4.p.rapidapi.com',
    'x-rapidapi-key': API_KEY
}
date_today = datetime.datetime.today().strftime('%Y-%m-%d')
date_tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
url_id_city = 'https://hotels4.p.rapidapi.com/locations/v2/search'
url_detail = 'https://hotels4.p.rapidapi.com/properties/list'
url_locale = 'https://hotels4.p.rapidapi.com/get-meta-data'
url_photos = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
