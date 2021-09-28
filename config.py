from environs import Env


env = Env()
env.read_env()
bot_token = env.str('bot_token')
admin_id = env.list('admin_id')
ip = env.str('ip')



