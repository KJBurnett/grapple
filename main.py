import re
import subprocess
import sys
import requests


def get_cdn_url(cdn_video_id):
    try:
        print(f"Attempting to download video id {cdn_video_id}...")
        response = requests.get(
            url=f"https://api.flograppling.com/api/right-rail/videos/{cdn_video_id}",
        )
        print(
            "Response HTTP Status Code: {status_code}".format(
                status_code=response.status_code
            )
        )
    except requests.exceptions.RequestException:
        print("HTTP Request failed")

    return response.json()["data"]["source_video"]["playlist"]


# Attempts to parse the video name from the given url.
# Example expected input:
# https://www.flowrestling.org/events/10277271-replay-mat-3-2023-ncwa-national-wrestling-championships-mar-10-9-am/videos?q=Julie&playing=10713225
# Expected Output: 10277271-replay-mat-3-2023-ncwa-national-wrestling-championships-mar-10-9-am
def getVideoNameFromUrl(url) -> str | None:
    match = re.search("/([^/]+)/[^/]+$", url)
    if match:
        return match.group(1)
    else:
        return None


def getVideoIdFromUrl(url: str) -> str:
    return url.split("playing=")[1]


# TODO: Parse the video title from the body of the web page.
# The url title is not accurate.


def getVideoTitleFromWebPage(url) -> str:
    # Beautiful Soup to parse?
    # https://www.flowrestling.org/events/10277271-2023-ncwa-national-wrestling-championships/videos?q=Washington%20State&playing=10713703
    return ""


if __name__ == "__main__":
    url = sys.argv[1]
    videoId = getVideoIdFromUrl(url)
    cdnUrl = get_cdn_url(videoId)
    videoName = getVideoNameFromUrl(url)
    downloadLocation = f"C:\\Users\\burne\\Videos\\Flo\\{videoName}.mp4"

    if (videoName == None) or (videoId == None):
        # Bad!
        print("Error. Could not parse videoId or videoName")
        sys.exit(0)

    command = f"ffmpeg -i {cdnUrl} -bsf:a aac_adtstoasc -c copy {downloadLocation}"
    subprocess.call(command, shell=True)

    print(f"Successfully saved FloGrappling video to {downloadLocation}")
