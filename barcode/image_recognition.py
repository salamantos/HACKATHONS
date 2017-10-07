import project_settings
from buildWhiteAndBlack import *
from process import *


def recognize_img(link):
    urllib.urlretrieve(link, project_settings.original_photo_url)
    ToWhiteAndBlack(project_settings.original_photo_url, project_settings.white_black_url)
    recognizeFile(project_settings.white_black_url, project_settings.result_url, 'xml')
    return 0
