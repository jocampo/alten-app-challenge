import os
import subprocess

# Get the latest Database URL (which heroku cycles periodically) from the Heroku CLI
# in environments that can't invoke the .envrc file contents
DATABASE_URL = subprocess.Popen("heroku config:get DATABASE_URL -a jocampo-alten-app-challenge",
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).communicate()[0]

os.environ["DATABASE_URL"] = DATABASE_URL.decode("utf-8")
