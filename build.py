import subprocess
from datetime import datetime as dt

REGEXR_VERSION="3.6.1"
BASE_IMAGE_NAME = "winkelchri/regexr-base"
IMAGE_NAME = "winkelchri/regexr"

DATE_FORMAT = r"%Y-%m-%dT%H:%M:%SZ"
BUILD_DATE = dt.now().strftime(DATE_FORMAT)
print(BUILD_DATE)
# BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ'

def main():
    print("BUILD BASE IMAGE ...")
    build_base_image_command =(
        "docker build -t {image_name}:{regexr_version} --file base.dockerfile "
        "--build-arg REGEXR_VERSION={regexr_version} "
        "--build-arg BUILD_DATE={build_date} "
        "."
    ).format(
        image_name=BASE_IMAGE_NAME,
        regexr_version=REGEXR_VERSION,
        build_date=BUILD_DATE
    )
    print(build_base_image_command)
    subprocess.run(build_base_image_command, shell=True)

    print("BUILD FINAL CONTAINER ...")
    build_final_container_command = (
        "docker build -t {image_name}:{version} --file Dockerfile "
        "--build-arg VERSION={version} "
        "--build-arg BUILD_DATE={build_date} "
        "."
    ).format(
        image_name=IMAGE_NAME,
        version=REGEXR_VERSION,
        build_date=BUILD_DATE
    )
    
    print(build_final_container_command)
    subprocess.run(build_final_container_command)

    subprocess.run("docker tag {image_name}:{version} {image_name}:{latest}".format(
        image_name=BASE_IMAGE_NAME,
        version=REGEXR_VERSION
    ))

    subprocess.run("docker tag {image_name}:{version} {image_name}:{latest}".format(
        image_name=IMAGE_NAME,
        version=REGEXR_VERSION
    ))


if __name__  == "__main__":
    main()