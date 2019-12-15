import subprocess
from datetime import datetime as dt

REGEXR_VERSION="3.6.1"
IMAGE_NAME = "winkelchri/regexr"

DATE_FORMAT = r"%Y-%m-%dT%H:%M:%SZ"
BUILD_DATE = dt.now().strftime(DATE_FORMAT)
# BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ'


def run(command):
    subprocess.run(command, shell=True)


def main():
    latest_git_tag = subprocess.run(
        'git describe --tags',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Set the REGEXR_VERSION if there is a git tag available
    # Otherwise use the default value
    REGEXR_VERSION if latest_git_tag.stdout != b'' else REGEXR_VERSION

    # Command for building the docker container
    build_image_command =(
        "docker build -t {image_name}:{regexr_version} --file Dockerfile "
        "--build-arg REGEXR_VERSION={regexr_version} "
        "--build-arg BUILD_DATE={build_date} "
        "."
    ).format(
        image_name=IMAGE_NAME,
        regexr_version=REGEXR_VERSION,
        build_date=BUILD_DATE
    )

    # Command for tagging the container with latest
    tag_image_command = "docker tag {image_name}:{version} {image_name}:latest".format(
        image_name=IMAGE_NAME,
        version=REGEXR_VERSION
    )

    run(build_image_command)
    run(tag_image_command)


if __name__  == "__main__":
    main()