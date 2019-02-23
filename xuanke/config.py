import getpass
import os
import platform

from selenium import webdriver

from local_config import LocalConfig

cur_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(cur_dir, "data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

platform_name = platform.system()

if platform_name == "Windows":
    driver_name = 'chromedriver_win.exe'
elif platform_name == "Linux":
    driver_name = 'phantomjs_linux'
else:
    driver_name = 'chromedriver_mac'

driver_path = os.path.join(cur_dir, 'utils', driver_name)


def get_driver():
    if platform_name == "Linux":
        driver = webdriver.PhantomJS(driver_path)
    else:
        driver = webdriver.Chrome(driver_path)
    return driver


tesseract_config_str = ''
if platform.system() == "Windows":
    if getpass.getuser() == "wsg":  # 我的电脑
        # "https://raw.githubusercontent.com/tesseract-ocr/tessdata/master/eng.traineddata"
        tesseract_config_str = ' --tessdata-dir "D:/Program/tesseract-Win64/tessdata"'
    else:
        raise ("请设置eng.traineddata所在目录")


class Config(LocalConfig):
    pass
