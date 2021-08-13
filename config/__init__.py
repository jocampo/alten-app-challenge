import subprocess

from utils.heroku import HerokuUtils

# Get the latest Database URL (which heroku cycles periodically) from the Heroku CLI
DATABASE_URL = subprocess.Popen("heroku config:get DATABASE_URL -a jocampo-alten-app-challenge",
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).communicate()[0].decode("utf-8").strip()

DATABASE_URL = HerokuUtils.parse_postgres_dialect(DATABASE_URL)
