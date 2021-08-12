import subprocess

# Get the latest Database URL (which heroku cycles periodically) from the Heroku CLI
DATABASE_URL = subprocess.Popen("heroku config:get DATABASE_URL -a jocampo-alten-app-challenge",
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).communicate()[0].decode("utf-8").strip()

# Fix an issue with the now deprecated postgres dialect that Heroku gives back
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
