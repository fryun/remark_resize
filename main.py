

from concurrent.futures import ProcessPoolExecutor
import os
import shutil
import time
from app import utility as ut
from app.logger import get_logger
from app.remark_resize import main_remark_resize
from app.config import config

logger = get_logger(__name__)

TIPE_RR = config.TIPE
MAX_PROCESS = config.BANYAK_PROSES

RESIZE_RESULT_DIR = config.RESIZE_RESULT_DIR
REMARK_RESULT_DIR = config.REMARK_RESULT_DIR
IMAGE_RESULT_DIR = config.IMAGE_RESULT_DIR
IMAGE_SRC_DONE = config.IMAGE_SRC_DONE_DIR

def main():
    
    start_time = time.perf_counter()
    ut.starting_text()
    list_foto = ut.get_images()
    split_foto = ut.split_images(list_foto)
    image_src_done_folder = ut.folder_done()
    time.sleep(1)
    
    #* Hapus foto sebelumnya
    shutil.rmtree(IMAGE_RESULT_DIR)
    os.mkdir(IMAGE_RESULT_DIR)
    os.mkdir(RESIZE_RESULT_DIR)
    os.mkdir(REMARK_RESULT_DIR)
    
    print()
    logger.info("======================= Start Remark Resize =======================")
    #* Test satu list foto
    # params = (split_foto[0], image_src_done_folder)
    # main_remark_resize(params)
    
    params = []
    for split in split_foto:
        params.append([split, image_src_done_folder])

    with ProcessPoolExecutor(max_workers=MAX_PROCESS) as executor:
        results = executor.map(main_remark_resize, params)

    end_time = time.perf_counter()    
    total_time = int(end_time - start_time)
    total_time = ut.convert_seconds_to_time(total_time)
    
    print()
    logger.info("====================== Remark Resize Selesai ======================")
    logger.info(f"Tipe Remark Resize: {TIPE_RR}")
    logger.info(f"Total Foto: {len(list_foto)}")
    logger.info(f"Total Waktu: {total_time}")
    logger.info("===================================================================")


if __name__ == "__main__":
    main()