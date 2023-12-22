
# Remark n Resize

This project is a tool for manipulating images. It can resize images and add watermarks. To use, simply add images to the `image_src` folder and then run the project. Simple settings can be changed in the config.txt file.

This project uses multiprocessing to speed up the processing of thousands of photos. Photos that have been successfully processed will be moved to the `image_src_done` folder, so that if there are failed processes, the successfully processed photos will not be mixed with photos that have not yet been processed. The results of the process will be saved in the `image_result` folder.
## Authors

- [@ArdiYp](https://www.github.com/fryun)

## Run Locally

Clone the project

```bash
  git clone https://github.com/fryun/remark_resize.git
```

Go to the project directory

```bash
  cd remark_resize
```

Install dependencies

```bash
  pip install -r requirements.py
```

Setting the config

```bash
  edit config.txt
```

Start the program

```bash
  double clik run.bat
```

