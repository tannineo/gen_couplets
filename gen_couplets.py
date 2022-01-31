# -*- coding: utf-8 -*-

import os
import freetype
import numpy as np
from PIL import Image

FONT_FILE = r'FZZJ-BQXSJF.ttf'
BG_FILE = r'dragon_n_phoenix.png'


def text2image(word, font_file, size=128, color=(0, 0, 0)):
    """使用指定字体 将单个汉字转为图像

    word        - 单个汉字字符串
    font_file   - 矢量字库文件名
    size        - 字号 默认128
    color       - 颜色 默认黑色
    """

    face = freetype.Face(font_file)
    face.set_char_size(size * size)

    face.load_char(word)
    btm_obj = face.glyph.bitmap
    w, h = btm_obj.width, btm_obj.rows
    pixels = np.array(btm_obj.buffer, dtype=np.uint8).reshape(h, w)

    dx = int(face.glyph.metrics.horiBearingX / 64)
    if dx > 0:
        patch = np.zeros((pixels.shape[0], dx), dtype=np.uint8)
        pixels = np.hstack((patch, pixels))

    r = np.ones(pixels.shape) * color[0] * 255
    g = np.ones(pixels.shape) * color[1] * 255
    b = np.ones(pixels.shape) * color[2] * 255

    im = np.dstack((r, g, b, pixels)).astype(np.uint8)

    return Image.fromarray(im)


def write_couplets(text,
                   horv='V',
                   quality='L',
                   out_file=None,
                   bg=BG_FILE,
                   bg_color='#ee2121ff'):
    """写春联

    text        - 春联字符串
    bg          - 背景图路径
    horv        - v-竖排 H-横排
    quality     - 单字分辨率 H-640像素 L-320像素
    out_file    - 输出文件名
    bg_color    - 背景颜色 带透明 默认大红
    """

    size, tsize = (320, 128) if quality == 'L' else (640, 180)
    ow, oh = (size, size * len(text)) if horv == 'V' else (size * len(text),
                                                           size)
    im_out = Image.new('RGBA', (ow, oh), bg_color)
    im_bg = Image.open(BG_FILE)

    im_bg = im_bg.resize((size, size))

    for i, w in enumerate(text):
        im_w = text2image(w, FONT_FILE, size=tsize, color=(0, 0, 0))
        w, h = im_w.size
        dw, dh = (size - w) // 2, (size - h) // 2

        if horv == 'V':
            im_out.paste(im_bg, (0, i * size), mask=im_bg)
            im_out.paste(im_w, (dw, i * size + dh), mask=im_w)
        else:
            im_out.paste(im_bg, (i * size, 0), mask=im_bg)
            im_out.paste(im_w, (i * size + dw, dh), mask=im_w)

    im_out.save('%s.png' % text)
    os.system("open " + '%s.png' % text)


if __name__ == '__main__':
    write_couplets('欧了', horv='H', quality='H')
    write_couplets('纠缠单抽出金', horv='V', quality='H')
    write_couplets('定轨十连五黄', horv='V', quality='H')
