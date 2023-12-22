import os
import pathlib
import sys
import time

from art import text2art

from app.config import config
from app.logger import get_logger


IMAGE_SRC_DIR = config.IMAGE_SRC_DIR
BANYAK_PROSES = config.BANYAK_PROSES
IMAGE_SRC_DONE_DIR = config.IMAGE_SRC_DONE_DIR
FOLDER_DONE = "_done"
FOTO_FOLDER = "FOTO"

logger = get_logger(__name__)


def starting_text():
    text = "Created By: ArdiYP"
    Art=text2art("Remark Resize","big")
    print(Art)
    print_with_delay(text,0.1)
    print()
    print()
    
    
def print_with_delay(text, delay):
    for char in text:
        print(char, end="")
        time.sleep(delay)
        sys.stdout.flush()
    time.sleep(0.3)


def convert_seconds_to_time(seconds:int):
  """
  Mengubah format detik menjadi jam dengan format hh:mm:ss

  Args:
    seconds: Jumlah detik

  Returns:
    String yang berisi waktu dengan format hh:mm:ss
  """

  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60

  time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

  return time_str


def get_images(image_dir=IMAGE_SRC_DIR):
    
    image_folder = pathlib.Path(image_dir)    
    semua_foto = list(image_folder.rglob("*.JPG"))
    if not semua_foto:
        raise Exception (f"Tidak ada foto di {IMAGE_SRC_DIR}")
    
    semua_foto_str = [str(path) for path in semua_foto]
    return semua_foto_str


def split_images(list_foto:list)->list:
    # Menghitung banyak daftar
    list_length = len(list_foto)
    # Menghitung jumlah elemen dalam setiap sublist
    chunk_size = round(list_length / BANYAK_PROSES)
    logger.info(f"banyak foto: {list_length}")
    logger.info(f"foto dibagi: {chunk_size}")
    # Membagi nilai dalam daftar menjadi sublist
    sublists = []

    for i in range(0, list_length, chunk_size):
        sublist = list_foto[i:i+chunk_size]
        sublists.append(sublist)
    
    return sublists


def get_image_name(image):
    return str(image).split("\\")[-1]


def folder_done(folder_number:int=0):
    folder_path = os.path.join(IMAGE_SRC_DONE_DIR, FOTO_FOLDER + "_" + str(folder_number))
    
    if os.path.exists(folder_path) or os.path.exists(folder_path + FOLDER_DONE):
        folder_path = folder_done(folder_number=folder_number + 1)
    else:
        os.mkdir(folder_path)
        
    return folder_path


def split_folder_result():
    pass
