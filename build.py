import subprocess
IMAGE_NAME = "winkelchri/regexr"

subprocess.run("docker build -t {} .".format(IMAGE_NAME))
