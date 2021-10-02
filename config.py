from environs import Env


env = Env()
env.read_env()
BOT_TOKEN = env.str('BOT_TOKEN')
ADMIN_ID = env.list('ADMIN_ID')
IP = env.str('IP')
API_KEY = env.str('X-RAPIDAPI-KEY')



