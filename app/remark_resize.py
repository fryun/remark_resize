

import os
import shutil

from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS, GPSTAGS

from app.config import config
from app.logger import get_logger
from app import utility as ut

TIPE = config.TIPE
SPLIT_FOLDER_RESULT = config.SPLIT_FOLDER
SPLIT_SIZE_RESULT = config.SPLIT_SIZE

RESIZE_RESULT_DIR = config.RESIZE_RESULT_DIR
REMARK_RESULT_DIR = config.REMARK_RESULT_DIR
IMAGE_RESULT_DIR = config.IMAGE_RESULT_DIR
PRESENTASI_RESIZE = config.PRESENTASI_RESIZE / 100
KUALITAS_FOTO = config.KUALITAS_FOTO

JENIS_REMARK = config.JENIS_REMARK
REMARK_GAMBAR = "gambar"
REMARK_TEXT = "teks"
WATERMARK_DIR = config.WATERMARK_DIR
FONT_DIR = config.FONT_DIR
GAMBAR_REMARK_DIR = os.path.join(WATERMARK_DIR, "remark.jpg")
WARNA_TEXT_REMARK = config.WARNA_TEXT_REMARK
WARNA_PESAN_REMARK = config.WARNA_PESAN
METEDATA = config.METEDATA
FONT_FILE = os.path.join(FONT_DIR, "font.otf")
WATERMARK_FONT_SIZE = 60
PESAN_FONT_SIZE = 30
WATERMARK_FONT = ImageFont.truetype(FONT_FILE, WATERMARK_FONT_SIZE)
PESAN_FONT = ImageFont.truetype(FONT_FILE, PESAN_FONT_SIZE)
PESAN = config.PESAN
PESAN_2 = config.PESAN_2

WATERMARK_X = 2
WATERMARK_Y = 1.8

PESAN_X = 2
PESAN_Y = 1.60

PESAN_2_X = 2
PESAN_2_Y = 1.52

DATETIME_X = 1
DATETIME_Y = 0.1

TIPE_1 = 1 # hanya resize
TIPE_2 = 2 # resize dan remark
TIPE_3 = 3 # menyimpan hasil resize dan remark

logger = get_logger(__name__)


def main_remark_resize(params):
    
    list_foto, src_done_dir = params
    
    for foto in list_foto:
        image_name = ut.get_image_name(foto)
        foto_done = os.path.join(src_done_dir, image_name)
        logger.info(f"start proses {image_name}")
        resize_result = resize(foto)
        
        if TIPE == TIPE_1:
            continue # tidak melakukan remark
        else:
            remark_result = remark(resize_result)
            
        if TIPE == TIPE_2:
            os.remove(resize_result)
        
        shutil.move(foto, foto_done)


def resize(image):
    
    image_name = ut.get_image_name(image)
    image_src = Image.open(image)
    resize_result = os.path.join(RESIZE_RESULT_DIR, image_name)

    #* Cek image, jika image ter rotasi maka akan di rotasi kembali ke posisi awalnya
    exif = image_src._getexif()
    orientation = 0
    if exif:
        orientation = exif.get(0x0112)
    if orientation == 3:
        image_src = image_src.rotate(180, expand=True)
    elif orientation == 6:
        image_src = image_src.rotate(270, expand=True)
    elif orientation == 8:
        image_src = image_src.rotate(90, expand=True)
        
    #* menentukan size file yang di kompres dari original image
    width, height = image_src.size
    new_width     = int(width * PRESENTASI_RESIZE)
    new_height    = int(height * PRESENTASI_RESIZE)
    new_size      = (new_width, new_height)
    logger.info(f"new size: {new_size} || quality: {KUALITAS_FOTO}")
    
    #* Proses resize
    resized_image = image_src.resize(new_size)
        
    #* Simpan hasil resize
    resized_image.save(resize_result, optimize=True, quality=KUALITAS_FOTO)
    resized_image.close()
    image_src.close()
    
    logger.info(f"Resize sukses : '{image_name}' [size {new_width}x{new_height}]")
    
    # if SPLIT_FOLDER_RESULT:
    #     ut.split_folder_result(resize_result)
        
    return resize_result


def remark(image):
    image_name = ut.get_image_name(image)
    remark_result = os.path.join(REMARK_RESULT_DIR, image_name)
    shutil.copy(image, remark_result)
    
    if JENIS_REMARK == REMARK_TEXT:
        set_watermark_font(remark_result)
    if JENIS_REMARK == REMARK_GAMBAR:
        set_watermark_image
    
    logger.info(f"Remark sukses : '{image_name}'")


def set_watermark_font(image:str):
    
    image_name = ut.get_image_name(image)
    image_src = Image.open(image)
    datetime_image = None
    
    #* Cek image, jika image ter rotasi maka akan di rotasi kembali ke posisi awalnya
    exif = image_src.getexif()
    orientation = 0
    if exif:
        orientation = exif.get(0x0112)
        
        for tag, value in exif.items():
            tag_name = TAGS.get(tag, tag)
            logger.info(f"{tag_name} : {value}")
            if tag_name == "DateTime":
                datetime_image = str(value)
                logger.info(f"image datetime found: {datetime_image}")
    # else:
    #     logger.info("exif tidak ditemukan!!!!!!!!!!!!!!!!")

    if orientation == 3:
        image_src = image_src.rotate(180, expand=True)
    elif orientation == 6:
        image_src = image_src.rotate(270, expand=True)
    elif orientation == 8:
        image_src = image_src.rotate(90, expand=True)
    
    width, height = image_src.size

    # if exif:
    #     for tag, value in exif.items():
    #         tag_name = TAGS.get(tag, tag)
    #         logger.info(f"{tag_name} : {value}")
    #         if tag_name == "DateTime":
    #             datetime_image = str(value)
    #             logger.info(f"image datetime found: {datetime_image}")

    # Buat objek ImageDraw
    draw = ImageDraw.Draw(image_src)
    
    # Ukuran teks
    text_length = WATERMARK_FONT.getlength(image_name)
    pesan_length = PESAN_FONT.getlength(PESAN)
    pesan_2_length = PESAN_FONT.getlength(PESAN_2)
    
    
    # Koordinat tengah gambar
    text_x = (width - text_length) // WATERMARK_X
    pesan_x = (width - pesan_length) // PESAN_X
    pesan_2_x = (width - pesan_2_length) // PESAN_2_X
    
    text_y = height // WATERMARK_Y
    pesan_y = height // PESAN_Y
    pesan_2_y = height // PESAN_2_Y
    datetime_y = height // DATETIME_Y
    
    font_position = (text_x, text_y)
    pesan_position = (pesan_x, pesan_y)
    pesan_2_position = (pesan_2_x, pesan_2_y)
    
    #* Gambar teks watermark pada gambar
    draw.text(font_position, image_name, fill=WARNA_TEXT_REMARK, font=WATERMARK_FONT)
    draw.text(pesan_position, PESAN, fill=WARNA_PESAN_REMARK, font=PESAN_FONT)
    draw.text(pesan_2_position, PESAN_2, fill=WARNA_PESAN_REMARK, font=PESAN_FONT)

    if datetime_image:
        datetime_length = PESAN_FONT.getlength(datetime_image)
        datetime_x = (width - datetime_length) // DATETIME_X
        datetime_position = (datetime_x, datetime_y)
        draw.text(datetime_position, datetime_image, fill=WARNA_PESAN_REMARK, font=PESAN_FONT)

    image_src.save(image, optimize=True, quality=KUALITAS_FOTO)
    image_src.close()


def set_watermark_image():
    pass


