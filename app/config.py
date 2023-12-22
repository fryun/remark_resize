import os
import multiprocessing
import pathlib

CONSTANTA_INT = ["PRESENTASI_RESIZE", "KUALITAS_FOTO", "BANYAK_PROSES","TIPE", "SPLIT_SIZE"]
CONSTANTA_BOOL = ["METEDATA","SPLIT_FOLDER"]
BOOL_TRUE = "true"

CONFIG_SYMBOL = "="

class Config:
    ROOT_DIR = str(pathlib.Path(__file__).parent.parent.absolute())
    IMAGE_SRC_DIR = os.path.join(ROOT_DIR, 'image_src')
    IMAGE_RESULT_DIR = os.path.join(ROOT_DIR, 'image_result')
    RESIZE_RESULT_DIR = os.path.join(IMAGE_RESULT_DIR, 'resize')
    REMARK_RESULT_DIR = os.path.join(IMAGE_RESULT_DIR, 'remark')
    IMAGE_SRC_DONE_DIR = os.path.join(ROOT_DIR, 'image_src_done')
    WATERMARK_DIR = os.path.join(ROOT_DIR, 'watermark')
    FONT_DIR = os.path.join(WATERMARK_DIR, 'font')
    
    TIPE:str
    PRESENTASI_RESIZE:int
    KUALITAS_FOTO:int
    BANYAK_PROSES:int
    KOMPRES_FOTO:str
    PESAN:str
    PESAN_2:str
    WARNA_PESAN:str
    JENIS_REMARK:str
    GAMBAR_REMARK:str
    WARNA_TEXT_REMARK:str
    METEDATA:bool
    SPLIT_FOLDER:bool
    SPLIT_SIZE:int

    def __init__(self) -> None:
        with open("config.txt", "r") as f:
            for line in f.readlines():
                if CONFIG_SYMBOL not in line:
                    continue
                
                text = line.split("=")
                var = text[0]
                value = text[1].replace("\n","")
                
                if var in CONSTANTA_INT:
                    self.__setattr__(var, int(value))
                else:
                    self.__setattr__(var, value)
                
                if var in CONSTANTA_BOOL:
                    if value == BOOL_TRUE:
                        self.__setattr__(var, True)
                    else:
                        self.__setattr__(var, False)


config = Config()