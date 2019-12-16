import sys
import subprocess
from datetime import datetime as dt

REGEXR_VERSION="3.6.1"
IMAGE_NAME = "winkelchri/regexr"


def run(command):
    subprocess.run(command, shell=True)


def get_latest_tag(default=REGEXR_VERSION):
    ''' Returns the latest git tag of the regexr repository. '''

    latest_git_tag = subprocess.run(
        'git describe --tags',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if latest_git_tag.stdout != b'':
        return latest_git_tag.stdout

    return default


def build_image(image_name, version_tag):
    ''' Builds the container using with the given image_name and specified version_tag. '''

    # BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    date_format = r"%Y-%m-%dT%H:%M:%SZ"
    build_date = dt.now().strftime(date_format)

    # Command for building the docker container
    build_image_command =(
        "docker build -t {image_name}:{version_tag} --file Dockerfile "
        "--build-arg REGEXR_VERSION={version_tag} "
        "--build-arg BUILD_DATE={build_date} "
        "."
    ).format(
        image_name=image_name,
        version_tag=version_tag,
        build_date=build_date
    )

    run(build_image_command)


def tag_image_latest(image_name, version_tag):
    ''' Tags the given image_name and version_tag with :latest '''

    # Command for tagging the container with latest
    tag_image_command = "docker tag {image_name}:{version_tag} {image_name}:latest".format(
        image_name=image_name,
        version_tag=version_tag
    )

    run(tag_image_command)


def main():
    image_name = IMAGE_NAME
    version_tag = get_latest_tag()

    if sys.argv[1] == '--skip-build':
        skip_build = True
    else:
        skip_build = False

    if not skip_build:
        build_image(image_name, version_tag)
        tag_image_latest(image_name, version_tag)

    sys.stdout.write(version_tag)

if __name__  == "__main__":
    main()