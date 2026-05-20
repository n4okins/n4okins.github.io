#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Air sender generator - standalone edition.

このファイルは、元の main.py を単一ファイル化し、Python 実行時の外部依存を
できるだけなくした版です。

実行時依存:
  - Python 標準ライブラリのみ

内蔵しているもの:
  - qrcode 8.2 のQRエンコードに必要な純Python部分
    （PIL/Pillow、pypng、SVG image factory は使わず、matrix からSVGを直接生成）
  - Fernet互換トークン生成に必要な最小AES-128-CBC暗号化処理
    （PBKDF2-HMAC-SHA256とHMAC-SHA256は標準ライブラリを使用）

互換性:
  - 生成されるデータ形式は既存の index.html と互換です。
  - 暗号化ありの場合も、既存の index.html の復号処理で読めるように
    salt + raw Fernet token の形式を維持します。

注意:
  - 内蔵AESは「このツールのFernet互換暗号化生成」に用途を絞った最小実装です。
  - index.html 側はFernet HMAC検証をしていませんが、この sender 側では正しいHMACを生成します。
"""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import hmac
import html
import os
import struct
import sys
import time
import types
from pathlib import Path

MAX_CHUNKS = 65_535
DEFAULT_CHUNK_SIZE = 256
DEFAULT_DELAY_MS = 75
PBKDF2_ITERATIONS = 100_000
FEC_MAGIC = b"QA"
FEC_VERSION = 2
FEC_HEADER_SIZE = 22

# ---------------------------------------------------------------------------
# Vendored qrcode 8.2 license
# ---------------------------------------------------------------------------
_QRCODE_LICENSE = 'Copyright (c) 2011, Lincoln Loop\nAll rights reserved.\n\nRedistribution and use in source and binary forms, with or without\nmodification, are permitted provided that the following conditions are met:\n\n    * Redistributions of source code must retain the above copyright notice,\n      this list of conditions and the following disclaimer.\n    * Redistributions in binary form must reproduce the above copyright notice,\n      this list of conditions and the following disclaimer in the documentation\n      and/or other materials provided with the distribution.\n    * Neither the package name nor the names of its contributors may be\n      used to endorse or promote products derived from this software without\n      specific prior written permission.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\nANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\nWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE \nDISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR\nANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\nLOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON\nANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\nSOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n\n\n-------------------------------------------------------------------------------\n\n\nOriginal text and license from the pyqrnative package where this was forked\nfrom (http://code.google.com/p/pyqrnative):\n\n#Ported from the Javascript library by Sam Curren\n#\n#QRCode for Javascript\n#http://d-project.googlecode.com/svn/trunk/misc/qrcode/js/qrcode.js\n#\n#Copyright (c) 2009 Kazuhiko Arase\n#\n#URL: http://www.d-project.com/\n#\n#Licensed under the MIT license:\n#   http://www.opensource.org/licenses/mit-license.php\n#\n# The word "QR Code" is registered trademark of\n# DENSO WAVE INCORPORATED\n#   http://www.denso-wave.com/qrcode/faqpatent-e.html\n'

# QRエンコードに必要な qrcode 8.2 の純Python部分だけを、メモリ上のモジュールとして読み込む。
# これにより `import qrcode` や Pillow/PIL は不要になる。
_QRCODE_MODULE_SOURCES = {
    "qrcode.constants": "# QR error correct levels\nERROR_CORRECT_L = 1\nERROR_CORRECT_M = 0\nERROR_CORRECT_Q = 3\nERROR_CORRECT_H = 2\n",
    "qrcode.exceptions": "class DataOverflowError(Exception):\n    pass\n",
    "qrcode.LUT": "# Store all kinds of lookup table.\n\n\n# # generate rsPoly lookup table.\n\n# from qrcode import base\n\n# def create_bytes(rs_blocks):\n#     for r in range(len(rs_blocks)):\n#         dcCount = rs_blocks[r].data_count\n#         ecCount = rs_blocks[r].total_count - dcCount\n#         rsPoly = base.Polynomial([1], 0)\n#         for i in range(ecCount):\n#             rsPoly = rsPoly * base.Polynomial([1, base.gexp(i)], 0)\n#         return ecCount, rsPoly\n\n# rsPoly_LUT = {}\n# for version in range(1,41):\n#     for error_correction in range(4):\n#         rs_blocks_list = base.rs_blocks(version, error_correction)\n#         ecCount, rsPoly = create_bytes(rs_blocks_list)\n#         rsPoly_LUT[ecCount]=rsPoly.num\n# print(rsPoly_LUT)\n\n# Result. Usage: input: ecCount, output: Polynomial.num\n# e.g. rsPoly = base.Polynomial(LUT.rsPoly_LUT[ecCount], 0)\nrsPoly_LUT = {\n    7: [1, 127, 122, 154, 164, 11, 68, 117],\n    10: [1, 216, 194, 159, 111, 199, 94, 95, 113, 157, 193],\n    13: [1, 137, 73, 227, 17, 177, 17, 52, 13, 46, 43, 83, 132, 120],\n    15: [1, 29, 196, 111, 163, 112, 74, 10, 105, 105, 139, 132, 151, 32, 134, 26],\n    16: [1, 59, 13, 104, 189, 68, 209, 30, 8, 163, 65, 41, 229, 98, 50, 36, 59],\n    17: [1, 119, 66, 83, 120, 119, 22, 197, 83, 249, 41, 143, 134, 85, 53, 125, 99, 79],\n    18: [\n        1,\n        239,\n        251,\n        183,\n        113,\n        149,\n        175,\n        199,\n        215,\n        240,\n        220,\n        73,\n        82,\n        173,\n        75,\n        32,\n        67,\n        217,\n        146,\n    ],\n    20: [\n        1,\n        152,\n        185,\n        240,\n        5,\n        111,\n        99,\n        6,\n        220,\n        112,\n        150,\n        69,\n        36,\n        187,\n        22,\n        228,\n        198,\n        121,\n        121,\n        165,\n        174,\n    ],\n    22: [\n        1,\n        89,\n        179,\n        131,\n        176,\n        182,\n        244,\n        19,\n        189,\n        69,\n        40,\n        28,\n        137,\n        29,\n        123,\n        67,\n        253,\n        86,\n        218,\n        230,\n        26,\n        145,\n        245,\n    ],\n    24: [\n        1,\n        122,\n        118,\n        169,\n        70,\n        178,\n        237,\n        216,\n        102,\n        115,\n        150,\n        229,\n        73,\n        130,\n        72,\n        61,\n        43,\n        206,\n        1,\n        237,\n        247,\n        127,\n        217,\n        144,\n        117,\n    ],\n    26: [\n        1,\n        246,\n        51,\n        183,\n        4,\n        136,\n        98,\n        199,\n        152,\n        77,\n        56,\n        206,\n        24,\n        145,\n        40,\n        209,\n        117,\n        233,\n        42,\n        135,\n        68,\n        70,\n        144,\n        146,\n        77,\n        43,\n        94,\n    ],\n    28: [\n        1,\n        252,\n        9,\n        28,\n        13,\n        18,\n        251,\n        208,\n        150,\n        103,\n        174,\n        100,\n        41,\n        167,\n        12,\n        247,\n        56,\n        117,\n        119,\n        233,\n        127,\n        181,\n        100,\n        121,\n        147,\n        176,\n        74,\n        58,\n        197,\n    ],\n    30: [\n        1,\n        212,\n        246,\n        77,\n        73,\n        195,\n        192,\n        75,\n        98,\n        5,\n        70,\n        103,\n        177,\n        22,\n        217,\n        138,\n        51,\n        181,\n        246,\n        72,\n        25,\n        18,\n        46,\n        228,\n        74,\n        216,\n        195,\n        11,\n        106,\n        130,\n        150,\n    ],\n}\n",
    "qrcode.base": 'from typing import NamedTuple\nfrom qrcode import constants\n\nEXP_TABLE = list(range(256))\n\nLOG_TABLE = list(range(256))\n\nfor i in range(8):\n    EXP_TABLE[i] = 1 << i\n\nfor i in range(8, 256):\n    EXP_TABLE[i] = (\n        EXP_TABLE[i - 4] ^ EXP_TABLE[i - 5] ^ EXP_TABLE[i - 6] ^ EXP_TABLE[i - 8]\n    )\n\nfor i in range(255):\n    LOG_TABLE[EXP_TABLE[i]] = i\n\nRS_BLOCK_OFFSET = {\n    constants.ERROR_CORRECT_L: 0,\n    constants.ERROR_CORRECT_M: 1,\n    constants.ERROR_CORRECT_Q: 2,\n    constants.ERROR_CORRECT_H: 3,\n}\n\nRS_BLOCK_TABLE = (\n    # L\n    # M\n    # Q\n    # H\n    # 1\n    (1, 26, 19),\n    (1, 26, 16),\n    (1, 26, 13),\n    (1, 26, 9),\n    # 2\n    (1, 44, 34),\n    (1, 44, 28),\n    (1, 44, 22),\n    (1, 44, 16),\n    # 3\n    (1, 70, 55),\n    (1, 70, 44),\n    (2, 35, 17),\n    (2, 35, 13),\n    # 4\n    (1, 100, 80),\n    (2, 50, 32),\n    (2, 50, 24),\n    (4, 25, 9),\n    # 5\n    (1, 134, 108),\n    (2, 67, 43),\n    (2, 33, 15, 2, 34, 16),\n    (2, 33, 11, 2, 34, 12),\n    # 6\n    (2, 86, 68),\n    (4, 43, 27),\n    (4, 43, 19),\n    (4, 43, 15),\n    # 7\n    (2, 98, 78),\n    (4, 49, 31),\n    (2, 32, 14, 4, 33, 15),\n    (4, 39, 13, 1, 40, 14),\n    # 8\n    (2, 121, 97),\n    (2, 60, 38, 2, 61, 39),\n    (4, 40, 18, 2, 41, 19),\n    (4, 40, 14, 2, 41, 15),\n    # 9\n    (2, 146, 116),\n    (3, 58, 36, 2, 59, 37),\n    (4, 36, 16, 4, 37, 17),\n    (4, 36, 12, 4, 37, 13),\n    # 10\n    (2, 86, 68, 2, 87, 69),\n    (4, 69, 43, 1, 70, 44),\n    (6, 43, 19, 2, 44, 20),\n    (6, 43, 15, 2, 44, 16),\n    # 11\n    (4, 101, 81),\n    (1, 80, 50, 4, 81, 51),\n    (4, 50, 22, 4, 51, 23),\n    (3, 36, 12, 8, 37, 13),\n    # 12\n    (2, 116, 92, 2, 117, 93),\n    (6, 58, 36, 2, 59, 37),\n    (4, 46, 20, 6, 47, 21),\n    (7, 42, 14, 4, 43, 15),\n    # 13\n    (4, 133, 107),\n    (8, 59, 37, 1, 60, 38),\n    (8, 44, 20, 4, 45, 21),\n    (12, 33, 11, 4, 34, 12),\n    # 14\n    (3, 145, 115, 1, 146, 116),\n    (4, 64, 40, 5, 65, 41),\n    (11, 36, 16, 5, 37, 17),\n    (11, 36, 12, 5, 37, 13),\n    # 15\n    (5, 109, 87, 1, 110, 88),\n    (5, 65, 41, 5, 66, 42),\n    (5, 54, 24, 7, 55, 25),\n    (11, 36, 12, 7, 37, 13),\n    # 16\n    (5, 122, 98, 1, 123, 99),\n    (7, 73, 45, 3, 74, 46),\n    (15, 43, 19, 2, 44, 20),\n    (3, 45, 15, 13, 46, 16),\n    # 17\n    (1, 135, 107, 5, 136, 108),\n    (10, 74, 46, 1, 75, 47),\n    (1, 50, 22, 15, 51, 23),\n    (2, 42, 14, 17, 43, 15),\n    # 18\n    (5, 150, 120, 1, 151, 121),\n    (9, 69, 43, 4, 70, 44),\n    (17, 50, 22, 1, 51, 23),\n    (2, 42, 14, 19, 43, 15),\n    # 19\n    (3, 141, 113, 4, 142, 114),\n    (3, 70, 44, 11, 71, 45),\n    (17, 47, 21, 4, 48, 22),\n    (9, 39, 13, 16, 40, 14),\n    # 20\n    (3, 135, 107, 5, 136, 108),\n    (3, 67, 41, 13, 68, 42),\n    (15, 54, 24, 5, 55, 25),\n    (15, 43, 15, 10, 44, 16),\n    # 21\n    (4, 144, 116, 4, 145, 117),\n    (17, 68, 42),\n    (17, 50, 22, 6, 51, 23),\n    (19, 46, 16, 6, 47, 17),\n    # 22\n    (2, 139, 111, 7, 140, 112),\n    (17, 74, 46),\n    (7, 54, 24, 16, 55, 25),\n    (34, 37, 13),\n    # 23\n    (4, 151, 121, 5, 152, 122),\n    (4, 75, 47, 14, 76, 48),\n    (11, 54, 24, 14, 55, 25),\n    (16, 45, 15, 14, 46, 16),\n    # 24\n    (6, 147, 117, 4, 148, 118),\n    (6, 73, 45, 14, 74, 46),\n    (11, 54, 24, 16, 55, 25),\n    (30, 46, 16, 2, 47, 17),\n    # 25\n    (8, 132, 106, 4, 133, 107),\n    (8, 75, 47, 13, 76, 48),\n    (7, 54, 24, 22, 55, 25),\n    (22, 45, 15, 13, 46, 16),\n    # 26\n    (10, 142, 114, 2, 143, 115),\n    (19, 74, 46, 4, 75, 47),\n    (28, 50, 22, 6, 51, 23),\n    (33, 46, 16, 4, 47, 17),\n    # 27\n    (8, 152, 122, 4, 153, 123),\n    (22, 73, 45, 3, 74, 46),\n    (8, 53, 23, 26, 54, 24),\n    (12, 45, 15, 28, 46, 16),\n    # 28\n    (3, 147, 117, 10, 148, 118),\n    (3, 73, 45, 23, 74, 46),\n    (4, 54, 24, 31, 55, 25),\n    (11, 45, 15, 31, 46, 16),\n    # 29\n    (7, 146, 116, 7, 147, 117),\n    (21, 73, 45, 7, 74, 46),\n    (1, 53, 23, 37, 54, 24),\n    (19, 45, 15, 26, 46, 16),\n    # 30\n    (5, 145, 115, 10, 146, 116),\n    (19, 75, 47, 10, 76, 48),\n    (15, 54, 24, 25, 55, 25),\n    (23, 45, 15, 25, 46, 16),\n    # 31\n    (13, 145, 115, 3, 146, 116),\n    (2, 74, 46, 29, 75, 47),\n    (42, 54, 24, 1, 55, 25),\n    (23, 45, 15, 28, 46, 16),\n    # 32\n    (17, 145, 115),\n    (10, 74, 46, 23, 75, 47),\n    (10, 54, 24, 35, 55, 25),\n    (19, 45, 15, 35, 46, 16),\n    # 33\n    (17, 145, 115, 1, 146, 116),\n    (14, 74, 46, 21, 75, 47),\n    (29, 54, 24, 19, 55, 25),\n    (11, 45, 15, 46, 46, 16),\n    # 34\n    (13, 145, 115, 6, 146, 116),\n    (14, 74, 46, 23, 75, 47),\n    (44, 54, 24, 7, 55, 25),\n    (59, 46, 16, 1, 47, 17),\n    # 35\n    (12, 151, 121, 7, 152, 122),\n    (12, 75, 47, 26, 76, 48),\n    (39, 54, 24, 14, 55, 25),\n    (22, 45, 15, 41, 46, 16),\n    # 36\n    (6, 151, 121, 14, 152, 122),\n    (6, 75, 47, 34, 76, 48),\n    (46, 54, 24, 10, 55, 25),\n    (2, 45, 15, 64, 46, 16),\n    # 37\n    (17, 152, 122, 4, 153, 123),\n    (29, 74, 46, 14, 75, 47),\n    (49, 54, 24, 10, 55, 25),\n    (24, 45, 15, 46, 46, 16),\n    # 38\n    (4, 152, 122, 18, 153, 123),\n    (13, 74, 46, 32, 75, 47),\n    (48, 54, 24, 14, 55, 25),\n    (42, 45, 15, 32, 46, 16),\n    # 39\n    (20, 147, 117, 4, 148, 118),\n    (40, 75, 47, 7, 76, 48),\n    (43, 54, 24, 22, 55, 25),\n    (10, 45, 15, 67, 46, 16),\n    # 40\n    (19, 148, 118, 6, 149, 119),\n    (18, 75, 47, 31, 76, 48),\n    (34, 54, 24, 34, 55, 25),\n    (20, 45, 15, 61, 46, 16),\n)\n\n\ndef glog(n):\n    if n < 1:  # pragma: no cover\n        raise ValueError(f"glog({n})")\n    return LOG_TABLE[n]\n\n\ndef gexp(n):\n    return EXP_TABLE[n % 255]\n\n\nclass Polynomial:\n    def __init__(self, num, shift):\n        if not num:  # pragma: no cover\n            raise Exception(f"{len(num)}/{shift}")\n\n        offset = 0\n        for offset in range(len(num)):\n            if num[offset] != 0:\n                break\n        else:\n            # qrcode 8.2 leaves an all-zero polynomial as many zero coefficients.\n            # That can later call glog(0) when a Reed-Solomon block is entirely zero,\n            # which happens often with large fixed-size binary/FEC shards padded by 0x00.\n            self.num = [0]\n            return\n\n        self.num = num[offset:] + [0] * shift\n\n    def __getitem__(self, index):\n        return self.num[index]\n\n    def __iter__(self):\n        return iter(self.num)\n\n    def __len__(self):\n        return len(self.num)\n\n    def __mul__(self, other):\n        num = [0] * (len(self) + len(other) - 1)\n\n        for i, item in enumerate(self):\n            for j, other_item in enumerate(other):\n                num[i + j] ^= gexp(glog(item) + glog(other_item))\n\n        return Polynomial(num, 0)\n\n    def __mod__(self, other):\n        difference = len(self) - len(other)\n        if difference < 0:\n            return self\n\n        ratio = glog(self[0]) - glog(other[0])\n\n        num = [\n            item ^ gexp(glog(other_item) + ratio)\n            for item, other_item in zip(self, other)\n        ]\n        if difference:\n            num.extend(self[-difference:])\n\n        # recursive call\n        return Polynomial(num, 0) % other\n\n\nclass RSBlock(NamedTuple):\n    total_count: int\n    data_count: int\n\n\ndef rs_blocks(version, error_correction):\n    if error_correction not in RS_BLOCK_OFFSET:  # pragma: no cover\n        raise Exception(\n            "bad rs block @ version: %s / error_correction: %s"\n            % (version, error_correction)\n        )\n    offset = RS_BLOCK_OFFSET[error_correction]\n    rs_block = RS_BLOCK_TABLE[(version - 1) * 4 + offset]\n\n    blocks = []\n\n    for i in range(0, len(rs_block), 3):\n        count, total_count, data_count = rs_block[i : i + 3]\n        for _ in range(count):\n            blocks.append(RSBlock(total_count, data_count))\n\n    return blocks\n',
    "qrcode.util": 'import math\nimport re\n\nfrom qrcode import LUT, base, exceptions\nfrom qrcode.base import RSBlock\n\n# QR encoding modes.\nMODE_NUMBER = 1 << 0\nMODE_ALPHA_NUM = 1 << 1\nMODE_8BIT_BYTE = 1 << 2\nMODE_KANJI = 1 << 3\n\n# Encoding mode sizes.\nMODE_SIZE_SMALL = {\n    MODE_NUMBER: 10,\n    MODE_ALPHA_NUM: 9,\n    MODE_8BIT_BYTE: 8,\n    MODE_KANJI: 8,\n}\nMODE_SIZE_MEDIUM = {\n    MODE_NUMBER: 12,\n    MODE_ALPHA_NUM: 11,\n    MODE_8BIT_BYTE: 16,\n    MODE_KANJI: 10,\n}\nMODE_SIZE_LARGE = {\n    MODE_NUMBER: 14,\n    MODE_ALPHA_NUM: 13,\n    MODE_8BIT_BYTE: 16,\n    MODE_KANJI: 12,\n}\n\nALPHA_NUM = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"\nRE_ALPHA_NUM = re.compile(b"^[" + re.escape(ALPHA_NUM) + rb"]*\\Z")\n\n# The number of bits for numeric delimited data lengths.\nNUMBER_LENGTH = {3: 10, 2: 7, 1: 4}\n\nPATTERN_POSITION_TABLE = [\n    [],\n    [6, 18],\n    [6, 22],\n    [6, 26],\n    [6, 30],\n    [6, 34],\n    [6, 22, 38],\n    [6, 24, 42],\n    [6, 26, 46],\n    [6, 28, 50],\n    [6, 30, 54],\n    [6, 32, 58],\n    [6, 34, 62],\n    [6, 26, 46, 66],\n    [6, 26, 48, 70],\n    [6, 26, 50, 74],\n    [6, 30, 54, 78],\n    [6, 30, 56, 82],\n    [6, 30, 58, 86],\n    [6, 34, 62, 90],\n    [6, 28, 50, 72, 94],\n    [6, 26, 50, 74, 98],\n    [6, 30, 54, 78, 102],\n    [6, 28, 54, 80, 106],\n    [6, 32, 58, 84, 110],\n    [6, 30, 58, 86, 114],\n    [6, 34, 62, 90, 118],\n    [6, 26, 50, 74, 98, 122],\n    [6, 30, 54, 78, 102, 126],\n    [6, 26, 52, 78, 104, 130],\n    [6, 30, 56, 82, 108, 134],\n    [6, 34, 60, 86, 112, 138],\n    [6, 30, 58, 86, 114, 142],\n    [6, 34, 62, 90, 118, 146],\n    [6, 30, 54, 78, 102, 126, 150],\n    [6, 24, 50, 76, 102, 128, 154],\n    [6, 28, 54, 80, 106, 132, 158],\n    [6, 32, 58, 84, 110, 136, 162],\n    [6, 26, 54, 82, 110, 138, 166],\n    [6, 30, 58, 86, 114, 142, 170],\n]\n\nG15 = (1 << 10) | (1 << 8) | (1 << 5) | (1 << 4) | (1 << 2) | (1 << 1) | (1 << 0)\nG18 = (\n    (1 << 12)\n    | (1 << 11)\n    | (1 << 10)\n    | (1 << 9)\n    | (1 << 8)\n    | (1 << 5)\n    | (1 << 2)\n    | (1 << 0)\n)\nG15_MASK = (1 << 14) | (1 << 12) | (1 << 10) | (1 << 4) | (1 << 1)\n\nPAD0 = 0xEC\nPAD1 = 0x11\n\n\n# Precompute bit count limits, indexed by error correction level and code size\ndef _data_count(block):\n    return block.data_count\n\n\nBIT_LIMIT_TABLE = [\n    [0]\n    + [\n        8 * sum(map(_data_count, base.rs_blocks(version, error_correction)))\n        for version in range(1, 41)\n    ]\n    for error_correction in range(4)\n]\n\n\ndef BCH_type_info(data):\n    d = data << 10\n    while BCH_digit(d) - BCH_digit(G15) >= 0:\n        d ^= G15 << (BCH_digit(d) - BCH_digit(G15))\n\n    return ((data << 10) | d) ^ G15_MASK\n\n\ndef BCH_type_number(data):\n    d = data << 12\n    while BCH_digit(d) - BCH_digit(G18) >= 0:\n        d ^= G18 << (BCH_digit(d) - BCH_digit(G18))\n    return (data << 12) | d\n\n\ndef BCH_digit(data):\n    digit = 0\n    while data != 0:\n        digit += 1\n        data >>= 1\n    return digit\n\n\ndef pattern_position(version):\n    return PATTERN_POSITION_TABLE[version - 1]\n\n\ndef mask_func(pattern):\n    """\n    Return the mask function for the given mask pattern.\n    """\n    if pattern == 0:  # 000\n        return lambda i, j: (i + j) % 2 == 0\n    if pattern == 1:  # 001\n        return lambda i, j: i % 2 == 0\n    if pattern == 2:  # 010\n        return lambda i, j: j % 3 == 0\n    if pattern == 3:  # 011\n        return lambda i, j: (i + j) % 3 == 0\n    if pattern == 4:  # 100\n        return lambda i, j: (math.floor(i / 2) + math.floor(j / 3)) % 2 == 0\n    if pattern == 5:  # 101\n        return lambda i, j: (i * j) % 2 + (i * j) % 3 == 0\n    if pattern == 6:  # 110\n        return lambda i, j: ((i * j) % 2 + (i * j) % 3) % 2 == 0\n    if pattern == 7:  # 111\n        return lambda i, j: ((i * j) % 3 + (i + j) % 2) % 2 == 0\n    raise TypeError("Bad mask pattern: " + pattern)  # pragma: no cover\n\n\ndef mode_sizes_for_version(version):\n    if version < 10:\n        return MODE_SIZE_SMALL\n    elif version < 27:\n        return MODE_SIZE_MEDIUM\n    else:\n        return MODE_SIZE_LARGE\n\n\ndef length_in_bits(mode, version):\n    if mode not in (MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE, MODE_KANJI):\n        raise TypeError(f"Invalid mode ({mode})")  # pragma: no cover\n\n    check_version(version)\n\n    return mode_sizes_for_version(version)[mode]\n\n\ndef check_version(version):\n    if version < 1 or version > 40:\n        raise ValueError(f"Invalid version (was {version}, expected 1 to 40)")\n\n\ndef lost_point(modules):\n    modules_count = len(modules)\n\n    lost_point = 0\n\n    lost_point = _lost_point_level1(modules, modules_count)\n    lost_point += _lost_point_level2(modules, modules_count)\n    lost_point += _lost_point_level3(modules, modules_count)\n    lost_point += _lost_point_level4(modules, modules_count)\n\n    return lost_point\n\n\ndef _lost_point_level1(modules, modules_count):\n    lost_point = 0\n\n    modules_range = range(modules_count)\n    container = [0] * (modules_count + 1)\n\n    for row in modules_range:\n        this_row = modules[row]\n        previous_color = this_row[0]\n        length = 0\n        for col in modules_range:\n            if this_row[col] == previous_color:\n                length += 1\n            else:\n                if length >= 5:\n                    container[length] += 1\n                length = 1\n                previous_color = this_row[col]\n        if length >= 5:\n            container[length] += 1\n\n    for col in modules_range:\n        previous_color = modules[0][col]\n        length = 0\n        for row in modules_range:\n            if modules[row][col] == previous_color:\n                length += 1\n            else:\n                if length >= 5:\n                    container[length] += 1\n                length = 1\n                previous_color = modules[row][col]\n        if length >= 5:\n            container[length] += 1\n\n    lost_point += sum(\n        container[each_length] * (each_length - 2)\n        for each_length in range(5, modules_count + 1)\n    )\n\n    return lost_point\n\n\ndef _lost_point_level2(modules, modules_count):\n    lost_point = 0\n\n    modules_range = range(modules_count - 1)\n    for row in modules_range:\n        this_row = modules[row]\n        next_row = modules[row + 1]\n        # use iter() and next() to skip next four-block. e.g.\n        # d a f   if top-right a != b bottom-right,\n        # c b e   then both abcd and abef won\'t lost any point.\n        modules_range_iter = iter(modules_range)\n        for col in modules_range_iter:\n            top_right = this_row[col + 1]\n            if top_right != next_row[col + 1]:\n                # reduce 33.3% of runtime via next().\n                # None: raise nothing if there is no next item.\n                next(modules_range_iter, None)\n            elif top_right != this_row[col]:\n                continue\n            elif top_right != next_row[col]:\n                continue\n            else:\n                lost_point += 3\n\n    return lost_point\n\n\ndef _lost_point_level3(modules, modules_count):\n    # 1 : 1 : 3 : 1 : 1 ratio (dark:light:dark:light:dark) pattern in\n    # row/column, preceded or followed by light area 4 modules wide. From ISOIEC.\n    # pattern1:     10111010000\n    # pattern2: 00001011101\n    modules_range = range(modules_count)\n    modules_range_short = range(modules_count - 10)\n    lost_point = 0\n\n    for row in modules_range:\n        this_row = modules[row]\n        modules_range_short_iter = iter(modules_range_short)\n        col = 0\n        for col in modules_range_short_iter:\n            if (\n                not this_row[col + 1]\n                and this_row[col + 4]\n                and not this_row[col + 5]\n                and this_row[col + 6]\n                and not this_row[col + 9]\n                and (\n                    this_row[col + 0]\n                    and this_row[col + 2]\n                    and this_row[col + 3]\n                    and not this_row[col + 7]\n                    and not this_row[col + 8]\n                    and not this_row[col + 10]\n                    or not this_row[col + 0]\n                    and not this_row[col + 2]\n                    and not this_row[col + 3]\n                    and this_row[col + 7]\n                    and this_row[col + 8]\n                    and this_row[col + 10]\n                )\n            ):\n                lost_point += 40\n            # horspool algorithm.\n            # if this_row[col + 10]:\n            #   pattern1 shift 4, pattern2 shift 2. So min=2.\n            # else:\n            #   pattern1 shift 1, pattern2 shift 1. So min=1.\n            if this_row[col + 10]:\n                next(modules_range_short_iter, None)\n\n    for col in modules_range:\n        modules_range_short_iter = iter(modules_range_short)\n        row = 0\n        for row in modules_range_short_iter:\n            if (\n                not modules[row + 1][col]\n                and modules[row + 4][col]\n                and not modules[row + 5][col]\n                and modules[row + 6][col]\n                and not modules[row + 9][col]\n                and (\n                    modules[row + 0][col]\n                    and modules[row + 2][col]\n                    and modules[row + 3][col]\n                    and not modules[row + 7][col]\n                    and not modules[row + 8][col]\n                    and not modules[row + 10][col]\n                    or not modules[row + 0][col]\n                    and not modules[row + 2][col]\n                    and not modules[row + 3][col]\n                    and modules[row + 7][col]\n                    and modules[row + 8][col]\n                    and modules[row + 10][col]\n                )\n            ):\n                lost_point += 40\n            if modules[row + 10][col]:\n                next(modules_range_short_iter, None)\n\n    return lost_point\n\n\ndef _lost_point_level4(modules, modules_count):\n    dark_count = sum(map(sum, modules))\n    percent = float(dark_count) / (modules_count**2)\n    # Every 5% departure from 50%, rating++\n    rating = int(abs(percent * 100 - 50) / 5)\n    return rating * 10\n\n\ndef optimal_data_chunks(data, minimum=4):\n    """\n    An iterator returning QRData chunks optimized to the data content.\n\n    :param minimum: The minimum number of bytes in a row to split as a chunk.\n    """\n    data = to_bytestring(data)\n    num_pattern = rb"\\d"\n    alpha_pattern = b"[" + re.escape(ALPHA_NUM) + b"]"\n    if len(data) <= minimum:\n        num_pattern = re.compile(b"^" + num_pattern + b"+$")\n        alpha_pattern = re.compile(b"^" + alpha_pattern + b"+$")\n    else:\n        re_repeat = b"{" + str(minimum).encode("ascii") + b",}"\n        num_pattern = re.compile(num_pattern + re_repeat)\n        alpha_pattern = re.compile(alpha_pattern + re_repeat)\n    num_bits = _optimal_split(data, num_pattern)\n    for is_num, chunk in num_bits:\n        if is_num:\n            yield QRData(chunk, mode=MODE_NUMBER, check_data=False)\n        else:\n            for is_alpha, sub_chunk in _optimal_split(chunk, alpha_pattern):\n                mode = MODE_ALPHA_NUM if is_alpha else MODE_8BIT_BYTE\n                yield QRData(sub_chunk, mode=mode, check_data=False)\n\n\ndef _optimal_split(data, pattern):\n    while data:\n        match = re.search(pattern, data)\n        if not match:\n            break\n        start, end = match.start(), match.end()\n        if start:\n            yield False, data[:start]\n        yield True, data[start:end]\n        data = data[end:]\n    if data:\n        yield False, data\n\n\ndef to_bytestring(data):\n    """\n    Convert data to a (utf-8 encoded) byte-string if it isn\'t a byte-string\n    already.\n    """\n    if not isinstance(data, bytes):\n        data = str(data).encode("utf-8")\n    return data\n\n\ndef optimal_mode(data):\n    """\n    Calculate the optimal mode for this chunk of data.\n    """\n    if data.isdigit():\n        return MODE_NUMBER\n    if RE_ALPHA_NUM.match(data):\n        return MODE_ALPHA_NUM\n    return MODE_8BIT_BYTE\n\n\nclass QRData:\n    """\n    Data held in a QR compatible format.\n\n    Doesn\'t currently handle KANJI.\n    """\n\n    def __init__(self, data, mode=None, check_data=True):\n        """\n        If ``mode`` isn\'t provided, the most compact QR data type possible is\n        chosen.\n        """\n        if check_data:\n            data = to_bytestring(data)\n\n        if mode is None:\n            self.mode = optimal_mode(data)\n        else:\n            self.mode = mode\n            if mode not in (MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE):\n                raise TypeError(f"Invalid mode ({mode})")  # pragma: no cover\n            if check_data and mode < optimal_mode(data):  # pragma: no cover\n                raise ValueError(f"Provided data can not be represented in mode {mode}")\n\n        self.data = data\n\n    def __len__(self):\n        return len(self.data)\n\n    def write(self, buffer):\n        if self.mode == MODE_NUMBER:\n            for i in range(0, len(self.data), 3):\n                chars = self.data[i : i + 3]\n                bit_length = NUMBER_LENGTH[len(chars)]\n                buffer.put(int(chars), bit_length)\n        elif self.mode == MODE_ALPHA_NUM:\n            for i in range(0, len(self.data), 2):\n                chars = self.data[i : i + 2]\n                if len(chars) > 1:\n                    buffer.put(\n                        ALPHA_NUM.find(chars[0]) * 45 + ALPHA_NUM.find(chars[1]), 11\n                    )\n                else:\n                    buffer.put(ALPHA_NUM.find(chars), 6)\n        else:\n            # Iterating a bytestring in Python 3 returns an integer,\n            # no need to ord().\n            data = self.data\n            for c in data:\n                buffer.put(c, 8)\n\n    def __repr__(self):\n        return repr(self.data)\n\n\nclass BitBuffer:\n    def __init__(self):\n        self.buffer: list[int] = []\n        self.length = 0\n\n    def __repr__(self):\n        return ".".join([str(n) for n in self.buffer])\n\n    def get(self, index):\n        buf_index = math.floor(index / 8)\n        return ((self.buffer[buf_index] >> (7 - index % 8)) & 1) == 1\n\n    def put(self, num, length):\n        for i in range(length):\n            self.put_bit(((num >> (length - i - 1)) & 1) == 1)\n\n    def __len__(self):\n        return self.length\n\n    def put_bit(self, bit):\n        buf_index = self.length // 8\n        if len(self.buffer) <= buf_index:\n            self.buffer.append(0)\n        if bit:\n            self.buffer[buf_index] |= 0x80 >> (self.length % 8)\n        self.length += 1\n\n\ndef create_bytes(buffer: BitBuffer, rs_blocks: list[RSBlock]):\n    offset = 0\n\n    maxDcCount = 0\n    maxEcCount = 0\n\n    dcdata: list[list[int]] = []\n    ecdata: list[list[int]] = []\n\n    for rs_block in rs_blocks:\n        dcCount = rs_block.data_count\n        ecCount = rs_block.total_count - dcCount\n\n        maxDcCount = max(maxDcCount, dcCount)\n        maxEcCount = max(maxEcCount, ecCount)\n\n        current_dc = [0xFF & buffer.buffer[i + offset] for i in range(dcCount)]\n        offset += dcCount\n\n        # Get error correction polynomial.\n        if ecCount in LUT.rsPoly_LUT:\n            rsPoly = base.Polynomial(LUT.rsPoly_LUT[ecCount], 0)\n        else:\n            rsPoly = base.Polynomial([1], 0)\n            for i in range(ecCount):\n                rsPoly = rsPoly * base.Polynomial([1, base.gexp(i)], 0)\n\n        rawPoly = base.Polynomial(current_dc, len(rsPoly) - 1)\n\n        modPoly = rawPoly % rsPoly\n        current_ec = []\n        mod_offset = len(modPoly) - ecCount\n        for i in range(ecCount):\n            modIndex = i + mod_offset\n            current_ec.append(modPoly[modIndex] if (modIndex >= 0) else 0)\n\n        dcdata.append(current_dc)\n        ecdata.append(current_ec)\n\n    data = []\n    for i in range(maxDcCount):\n        for dc in dcdata:\n            if i < len(dc):\n                data.append(dc[i])\n    for i in range(maxEcCount):\n        for ec in ecdata:\n            if i < len(ec):\n                data.append(ec[i])\n\n    return data\n\n\ndef create_data(version, error_correction, data_list):\n    buffer = BitBuffer()\n    for data in data_list:\n        buffer.put(data.mode, 4)\n        buffer.put(len(data), length_in_bits(data.mode, version))\n        data.write(buffer)\n\n    # Calculate the maximum number of bits for the given version.\n    rs_blocks = base.rs_blocks(version, error_correction)\n    bit_limit = sum(block.data_count * 8 for block in rs_blocks)\n    if len(buffer) > bit_limit:\n        raise exceptions.DataOverflowError(\n            "Code length overflow. Data size (%s) > size available (%s)"\n            % (len(buffer), bit_limit)\n        )\n\n    # Terminate the bits (add up to four 0s).\n    for _ in range(min(bit_limit - len(buffer), 4)):\n        buffer.put_bit(False)\n\n    # Delimit the string into 8-bit words, padding with 0s if necessary.\n    delimit = len(buffer) % 8\n    if delimit:\n        for _ in range(8 - delimit):\n            buffer.put_bit(False)\n\n    # Add special alternating padding bitstrings until buffer is full.\n    bytes_to_fill = (bit_limit - len(buffer)) // 8\n    for i in range(bytes_to_fill):\n        if i % 2 == 0:\n            buffer.put(PAD0, 8)\n        else:\n            buffer.put(PAD1, 8)\n\n    return create_bytes(buffer, rs_blocks)\n',
    "qrcode.main": 'import sys\nfrom bisect import bisect_left\nfrom typing import (\n    Generic,\n    NamedTuple,\n    Optional,\n    TypeVar,\n    cast,\n    overload,\n    Literal,\n)\n\nfrom qrcode import constants, exceptions, util\nfrom qrcode.image.base import BaseImage\nfrom qrcode.image.pure import PyPNGImage\n\nModulesType = list[list[Optional[bool]]]\n# Cache modules generated just based on the QR Code version\nprecomputed_qr_blanks: dict[int, ModulesType] = {}\n\n\ndef make(data=None, **kwargs):\n    qr = QRCode(**kwargs)\n    qr.add_data(data)\n    return qr.make_image()\n\n\ndef _check_box_size(size):\n    if int(size) <= 0:\n        raise ValueError(f"Invalid box size (was {size}, expected larger than 0)")\n\n\ndef _check_border(size):\n    if int(size) < 0:\n        raise ValueError(\n            "Invalid border value (was %s, expected 0 or larger than that)" % size\n        )\n\n\ndef _check_mask_pattern(mask_pattern):\n    if mask_pattern is None:\n        return\n    if not isinstance(mask_pattern, int):\n        raise TypeError(\n            f"Invalid mask pattern (was {type(mask_pattern)}, expected int)"\n        )\n    if mask_pattern < 0 or mask_pattern > 7:\n        raise ValueError(f"Mask pattern should be in range(8) (got {mask_pattern})")\n\n\ndef copy_2d_array(x):\n    return [row[:] for row in x]\n\n\nclass ActiveWithNeighbors(NamedTuple):\n    NW: bool\n    N: bool\n    NE: bool\n    W: bool\n    me: bool\n    E: bool\n    SW: bool\n    S: bool\n    SE: bool\n\n    def __bool__(self) -> bool:\n        return self.me\n\n\nGenericImage = TypeVar("GenericImage", bound=BaseImage)\nGenericImageLocal = TypeVar("GenericImageLocal", bound=BaseImage)\n\n\nclass QRCode(Generic[GenericImage]):\n    modules: ModulesType\n    _version: Optional[int] = None\n\n    def __init__(\n        self,\n        version=None,\n        error_correction=constants.ERROR_CORRECT_M,\n        box_size=10,\n        border=4,\n        image_factory: Optional[type[GenericImage]] = None,\n        mask_pattern=None,\n    ):\n        _check_box_size(box_size)\n        _check_border(border)\n        self.version = version\n        self.error_correction = int(error_correction)\n        self.box_size = int(box_size)\n        # Spec says border should be at least four boxes wide, but allow for\n        # any (e.g. for producing printable QR codes).\n        self.border = int(border)\n        self.mask_pattern = mask_pattern\n        self.image_factory = image_factory\n        if image_factory is not None:\n            assert issubclass(image_factory, BaseImage)\n        self.clear()\n\n    @property\n    def version(self) -> int:\n        if self._version is None:\n            self.best_fit()\n        return cast(int, self._version)\n\n    @version.setter\n    def version(self, value) -> None:\n        if value is not None:\n            value = int(value)\n            util.check_version(value)\n        self._version = value\n\n    @property\n    def mask_pattern(self):\n        return self._mask_pattern\n\n    @mask_pattern.setter\n    def mask_pattern(self, pattern):\n        _check_mask_pattern(pattern)\n        self._mask_pattern = pattern\n\n    def clear(self):\n        """\n        Reset the internal data.\n        """\n        self.modules = [[]]\n        self.modules_count = 0\n        self.data_cache = None\n        self.data_list = []\n\n    def add_data(self, data, optimize=20):\n        """\n        Add data to this QR Code.\n\n        :param optimize: Data will be split into multiple chunks to optimize\n            the QR size by finding to more compressed modes of at least this\n            length. Set to ``0`` to avoid optimizing at all.\n        """\n        if isinstance(data, util.QRData):\n            self.data_list.append(data)\n        elif optimize:\n            self.data_list.extend(util.optimal_data_chunks(data, minimum=optimize))\n        else:\n            self.data_list.append(util.QRData(data))\n        self.data_cache = None\n\n    def make(self, fit=True):\n        """\n        Compile the data into a QR Code array.\n\n        :param fit: If ``True`` (or if a size has not been provided), find the\n            best fit for the data to avoid data overflow errors.\n        """\n        if fit or (self.version is None):\n            self.best_fit(start=self.version)\n        if self.mask_pattern is None:\n            self.makeImpl(False, self.best_mask_pattern())\n        else:\n            self.makeImpl(False, self.mask_pattern)\n\n    def makeImpl(self, test, mask_pattern):\n        self.modules_count = self.version * 4 + 17\n\n        if self.version in precomputed_qr_blanks:\n            self.modules = copy_2d_array(precomputed_qr_blanks[self.version])\n        else:\n            self.modules = [\n                [None] * self.modules_count for i in range(self.modules_count)\n            ]\n            self.setup_position_probe_pattern(0, 0)\n            self.setup_position_probe_pattern(self.modules_count - 7, 0)\n            self.setup_position_probe_pattern(0, self.modules_count - 7)\n            self.setup_position_adjust_pattern()\n            self.setup_timing_pattern()\n\n            precomputed_qr_blanks[self.version] = copy_2d_array(self.modules)\n\n        self.setup_type_info(test, mask_pattern)\n\n        if self.version >= 7:\n            self.setup_type_number(test)\n\n        if self.data_cache is None:\n            self.data_cache = util.create_data(\n                self.version, self.error_correction, self.data_list\n            )\n        self.map_data(self.data_cache, mask_pattern)\n\n    def setup_position_probe_pattern(self, row, col):\n        for r in range(-1, 8):\n            if row + r <= -1 or self.modules_count <= row + r:\n                continue\n\n            for c in range(-1, 8):\n                if col + c <= -1 or self.modules_count <= col + c:\n                    continue\n\n                if (\n                    (0 <= r <= 6 and c in {0, 6})\n                    or (0 <= c <= 6 and r in {0, 6})\n                    or (2 <= r <= 4 and 2 <= c <= 4)\n                ):\n                    self.modules[row + r][col + c] = True\n                else:\n                    self.modules[row + r][col + c] = False\n\n    def best_fit(self, start=None):\n        """\n        Find the minimum size required to fit in the data.\n        """\n        if start is None:\n            start = 1\n        util.check_version(start)\n\n        # Corresponds to the code in util.create_data, except we don\'t yet know\n        # version, so optimistically assume start and check later\n        mode_sizes = util.mode_sizes_for_version(start)\n        buffer = util.BitBuffer()\n        for data in self.data_list:\n            buffer.put(data.mode, 4)\n            buffer.put(len(data), mode_sizes[data.mode])\n            data.write(buffer)\n\n        needed_bits = len(buffer)\n        self.version = bisect_left(\n            util.BIT_LIMIT_TABLE[self.error_correction], needed_bits, start\n        )\n        if self.version == 41:\n            raise exceptions.DataOverflowError()\n\n        # Now check whether we need more bits for the mode sizes, recursing if\n        # our guess was too low\n        if mode_sizes is not util.mode_sizes_for_version(self.version):\n            self.best_fit(start=self.version)\n        return self.version\n\n    def best_mask_pattern(self):\n        """\n        Find the most efficient mask pattern.\n        """\n        min_lost_point = 0\n        pattern = 0\n\n        for i in range(8):\n            self.makeImpl(True, i)\n\n            lost_point = util.lost_point(self.modules)\n\n            if i == 0 or min_lost_point > lost_point:\n                min_lost_point = lost_point\n                pattern = i\n\n        return pattern\n\n    def print_tty(self, out=None):\n        """\n        Output the QR Code only using TTY colors.\n\n        If the data has not been compiled yet, make it first.\n        """\n        if out is None:\n            import sys\n\n            out = sys.stdout\n\n        if not out.isatty():\n            raise OSError("Not a tty")\n\n        if self.data_cache is None:\n            self.make()\n\n        modcount = self.modules_count\n        out.write("\\x1b[1;47m" + (" " * (modcount * 2 + 4)) + "\\x1b[0m\\n")\n        for r in range(modcount):\n            out.write("\\x1b[1;47m  \\x1b[40m")\n            for c in range(modcount):\n                if self.modules[r][c]:\n                    out.write("  ")\n                else:\n                    out.write("\\x1b[1;47m  \\x1b[40m")\n            out.write("\\x1b[1;47m  \\x1b[0m\\n")\n        out.write("\\x1b[1;47m" + (" " * (modcount * 2 + 4)) + "\\x1b[0m\\n")\n        out.flush()\n\n    def print_ascii(self, out=None, tty=False, invert=False):\n        """\n        Output the QR Code using ASCII characters.\n\n        :param tty: use fixed TTY color codes (forces invert=True)\n        :param invert: invert the ASCII characters (solid <-> transparent)\n        """\n        if out is None:\n            out = sys.stdout\n\n        if tty and not out.isatty():\n            raise OSError("Not a tty")\n\n        if self.data_cache is None:\n            self.make()\n\n        modcount = self.modules_count\n        codes = [bytes((code,)).decode("cp437") for code in (255, 223, 220, 219)]\n        if tty:\n            invert = True\n        if invert:\n            codes.reverse()\n\n        def get_module(x, y) -> int:\n            if invert and self.border and max(x, y) >= modcount + self.border:\n                return 1\n            if min(x, y) < 0 or max(x, y) >= modcount:\n                return 0\n            return cast(int, self.modules[x][y])\n\n        for r in range(-self.border, modcount + self.border, 2):\n            if tty:\n                if not invert or r < modcount + self.border - 1:\n                    out.write("\\x1b[48;5;232m")  # Background black\n                out.write("\\x1b[38;5;255m")  # Foreground white\n            for c in range(-self.border, modcount + self.border):\n                pos = get_module(r, c) + (get_module(r + 1, c) << 1)\n                out.write(codes[pos])\n            if tty:\n                out.write("\\x1b[0m")\n            out.write("\\n")\n        out.flush()\n\n    @overload\n    def make_image(\n        self, image_factory: Literal[None] = None, **kwargs\n    ) -> GenericImage: ...\n\n    @overload\n    def make_image(\n        self, image_factory: type[GenericImageLocal] = None, **kwargs\n    ) -> GenericImageLocal: ...\n\n    def make_image(self, image_factory=None, **kwargs):\n        """\n        Make an image from the QR Code data.\n\n        If the data has not been compiled yet, make it first.\n        """\n        # allow embeded_ parameters with typos for backwards compatibility\n        if (\n            kwargs.get("embedded_image_path")\n            or kwargs.get("embedded_image")\n            or kwargs.get("embeded_image_path")\n            or kwargs.get("embeded_image")\n        ) and self.error_correction != constants.ERROR_CORRECT_H:\n            raise ValueError(\n                "Error correction level must be ERROR_CORRECT_H if an embedded image is provided"\n            )\n        _check_box_size(self.box_size)\n        if self.data_cache is None:\n            self.make()\n\n        if image_factory is not None:\n            assert issubclass(image_factory, BaseImage)\n        else:\n            image_factory = self.image_factory\n            if image_factory is None:\n                from qrcode.image.pil import Image, PilImage\n\n                # Use PIL by default if available, otherwise use PyPNG.\n                image_factory = PilImage if Image else PyPNGImage\n\n        im = image_factory(\n            self.border,\n            self.modules_count,\n            self.box_size,\n            qrcode_modules=self.modules,\n            **kwargs,\n        )\n\n        if im.needs_drawrect:\n            for r in range(self.modules_count):\n                for c in range(self.modules_count):\n                    if im.needs_context:\n                        im.drawrect_context(r, c, qr=self)\n                    elif self.modules[r][c]:\n                        im.drawrect(r, c)\n        if im.needs_processing:\n            im.process()\n\n        return im\n\n    # return true if and only if (row, col) is in the module\n    def is_constrained(self, row: int, col: int) -> bool:\n        return (\n            row >= 0\n            and row < len(self.modules)\n            and col >= 0\n            and col < len(self.modules[row])\n        )\n\n    def setup_timing_pattern(self):\n        for r in range(8, self.modules_count - 8):\n            if self.modules[r][6] is not None:\n                continue\n            self.modules[r][6] = r % 2 == 0\n\n        for c in range(8, self.modules_count - 8):\n            if self.modules[6][c] is not None:\n                continue\n            self.modules[6][c] = c % 2 == 0\n\n    def setup_position_adjust_pattern(self):\n        pos = util.pattern_position(self.version)\n\n        for i in range(len(pos)):\n            row = pos[i]\n\n            for j in range(len(pos)):\n                col = pos[j]\n\n                if self.modules[row][col] is not None:\n                    continue\n\n                for r in range(-2, 3):\n                    for c in range(-2, 3):\n                        if (\n                            r == -2\n                            or r == 2\n                            or c == -2\n                            or c == 2\n                            or (r == 0 and c == 0)\n                        ):\n                            self.modules[row + r][col + c] = True\n                        else:\n                            self.modules[row + r][col + c] = False\n\n    def setup_type_number(self, test):\n        bits = util.BCH_type_number(self.version)\n\n        for i in range(18):\n            mod = not test and ((bits >> i) & 1) == 1\n            self.modules[i // 3][i % 3 + self.modules_count - 8 - 3] = mod\n\n        for i in range(18):\n            mod = not test and ((bits >> i) & 1) == 1\n            self.modules[i % 3 + self.modules_count - 8 - 3][i // 3] = mod\n\n    def setup_type_info(self, test, mask_pattern):\n        data = (self.error_correction << 3) | mask_pattern\n        bits = util.BCH_type_info(data)\n\n        # vertical\n        for i in range(15):\n            mod = not test and ((bits >> i) & 1) == 1\n\n            if i < 6:\n                self.modules[i][8] = mod\n            elif i < 8:\n                self.modules[i + 1][8] = mod\n            else:\n                self.modules[self.modules_count - 15 + i][8] = mod\n\n        # horizontal\n        for i in range(15):\n            mod = not test and ((bits >> i) & 1) == 1\n\n            if i < 8:\n                self.modules[8][self.modules_count - i - 1] = mod\n            elif i < 9:\n                self.modules[8][15 - i - 1 + 1] = mod\n            else:\n                self.modules[8][15 - i - 1] = mod\n\n        # fixed module\n        self.modules[self.modules_count - 8][8] = not test\n\n    def map_data(self, data, mask_pattern):\n        inc = -1\n        row = self.modules_count - 1\n        bitIndex = 7\n        byteIndex = 0\n\n        mask_func = util.mask_func(mask_pattern)\n\n        data_len = len(data)\n\n        for col in range(self.modules_count - 1, 0, -2):\n            if col <= 6:\n                col -= 1\n\n            col_range = (col, col - 1)\n\n            while True:\n                for c in col_range:\n                    if self.modules[row][c] is None:\n                        dark = False\n\n                        if byteIndex < data_len:\n                            dark = ((data[byteIndex] >> bitIndex) & 1) == 1\n\n                        if mask_func(row, c):\n                            dark = not dark\n\n                        self.modules[row][c] = dark\n                        bitIndex -= 1\n\n                        if bitIndex == -1:\n                            byteIndex += 1\n                            bitIndex = 7\n\n                row += inc\n\n                if row < 0 or self.modules_count <= row:\n                    row -= inc\n                    inc = -inc\n                    break\n\n    def get_matrix(self):\n        """\n        Return the QR Code as a multidimensional array, including the border.\n\n        To return the array without a border, set ``self.border`` to 0 first.\n        """\n        if self.data_cache is None:\n            self.make()\n\n        if not self.border:\n            return self.modules\n\n        width = len(self.modules) + self.border * 2\n        code = [[False] * width] * self.border\n        x_border = [False] * self.border\n        for module in self.modules:\n            code.append(x_border + cast(list[bool], module) + x_border)\n        code += [[False] * width] * self.border\n\n        return code\n\n    def active_with_neighbors(self, row: int, col: int) -> ActiveWithNeighbors:\n        context: list[bool] = []\n        for r in range(row - 1, row + 2):\n            for c in range(col - 1, col + 2):\n                context.append(self.is_constrained(r, c) and bool(self.modules[r][c]))\n        return ActiveWithNeighbors(*context)\n',
}


def _install_vendored_qrcode() -> types.ModuleType:
    """Install the minimal vendored qrcode package into sys.modules."""
    existing = sys.modules.get("qrcode")
    if existing is not None and getattr(existing, "_qr_air_vendored", False):
        return existing

    # Always use the vendored implementation in this file, even if external qrcode is installed.
    for name in list(sys.modules):
        if name == "qrcode" or name.startswith("qrcode."):
            del sys.modules[name]

    pkg = types.ModuleType("qrcode")
    pkg.__path__ = []  # mark as package
    pkg._qr_air_vendored = True
    sys.modules["qrcode"] = pkg

    image_pkg = types.ModuleType("qrcode.image")
    image_pkg.__path__ = []
    sys.modules["qrcode.image"] = image_pkg
    pkg.image = image_pkg

    image_base = types.ModuleType("qrcode.image.base")
    exec(
        "class BaseImage:\n"
        "    needs_context = False\n"
        "    needs_drawrect = False\n"
        "    needs_processing = False\n"
        "    def __init__(self, *args, **kwargs):\n"
        "        raise RuntimeError('Image factories are disabled in the standalone build; use qr_to_svg().')\n",
        image_base.__dict__,
    )
    sys.modules["qrcode.image.base"] = image_base
    image_pkg.base = image_base

    image_pure = types.ModuleType("qrcode.image.pure")
    exec("class PyPNGImage: pass\n", image_pure.__dict__)
    sys.modules["qrcode.image.pure"] = image_pure
    image_pkg.pure = image_pure

    # Load modules in dependency order.
    for mod_name in (
        "qrcode.constants",
        "qrcode.exceptions",
        "qrcode.LUT",
        "qrcode.base",
        "qrcode.util",
        "qrcode.main",
    ):
        module = types.ModuleType(mod_name)
        module.__package__ = mod_name.rpartition(".")[0]
        sys.modules[mod_name] = module
        setattr(pkg, mod_name.rpartition(".")[2], module)
        exec(
            compile(_QRCODE_MODULE_SOURCES[mod_name], f"<vendored {mod_name}>", "exec"),
            module.__dict__,
        )

    pkg.QRCode = sys.modules["qrcode.main"].QRCode
    pkg.make = sys.modules["qrcode.main"].make
    for name in (
        "ERROR_CORRECT_L",
        "ERROR_CORRECT_M",
        "ERROR_CORRECT_Q",
        "ERROR_CORRECT_H",
    ):
        setattr(pkg, name, getattr(sys.modules["qrcode.constants"], name))
    pkg.constants = sys.modules["qrcode.constants"]
    return pkg


# ---------------------------------------------------------------------------
# Minimal AES-128-CBC implementation for Fernet-compatible encryption
# ---------------------------------------------------------------------------

_SBOX = [
    0x63,
    0x7C,
    0x77,
    0x7B,
    0xF2,
    0x6B,
    0x6F,
    0xC5,
    0x30,
    0x01,
    0x67,
    0x2B,
    0xFE,
    0xD7,
    0xAB,
    0x76,
    0xCA,
    0x82,
    0xC9,
    0x7D,
    0xFA,
    0x59,
    0x47,
    0xF0,
    0xAD,
    0xD4,
    0xA2,
    0xAF,
    0x9C,
    0xA4,
    0x72,
    0xC0,
    0xB7,
    0xFD,
    0x93,
    0x26,
    0x36,
    0x3F,
    0xF7,
    0xCC,
    0x34,
    0xA5,
    0xE5,
    0xF1,
    0x71,
    0xD8,
    0x31,
    0x15,
    0x04,
    0xC7,
    0x23,
    0xC3,
    0x18,
    0x96,
    0x05,
    0x9A,
    0x07,
    0x12,
    0x80,
    0xE2,
    0xEB,
    0x27,
    0xB2,
    0x75,
    0x09,
    0x83,
    0x2C,
    0x1A,
    0x1B,
    0x6E,
    0x5A,
    0xA0,
    0x52,
    0x3B,
    0xD6,
    0xB3,
    0x29,
    0xE3,
    0x2F,
    0x84,
    0x53,
    0xD1,
    0x00,
    0xED,
    0x20,
    0xFC,
    0xB1,
    0x5B,
    0x6A,
    0xCB,
    0xBE,
    0x39,
    0x4A,
    0x4C,
    0x58,
    0xCF,
    0xD0,
    0xEF,
    0xAA,
    0xFB,
    0x43,
    0x4D,
    0x33,
    0x85,
    0x45,
    0xF9,
    0x02,
    0x7F,
    0x50,
    0x3C,
    0x9F,
    0xA8,
    0x51,
    0xA3,
    0x40,
    0x8F,
    0x92,
    0x9D,
    0x38,
    0xF5,
    0xBC,
    0xB6,
    0xDA,
    0x21,
    0x10,
    0xFF,
    0xF3,
    0xD2,
    0xCD,
    0x0C,
    0x13,
    0xEC,
    0x5F,
    0x97,
    0x44,
    0x17,
    0xC4,
    0xA7,
    0x7E,
    0x3D,
    0x64,
    0x5D,
    0x19,
    0x73,
    0x60,
    0x81,
    0x4F,
    0xDC,
    0x22,
    0x2A,
    0x90,
    0x88,
    0x46,
    0xEE,
    0xB8,
    0x14,
    0xDE,
    0x5E,
    0x0B,
    0xDB,
    0xE0,
    0x32,
    0x3A,
    0x0A,
    0x49,
    0x06,
    0x24,
    0x5C,
    0xC2,
    0xD3,
    0xAC,
    0x62,
    0x91,
    0x95,
    0xE4,
    0x79,
    0xE7,
    0xC8,
    0x37,
    0x6D,
    0x8D,
    0xD5,
    0x4E,
    0xA9,
    0x6C,
    0x56,
    0xF4,
    0xEA,
    0x65,
    0x7A,
    0xAE,
    0x08,
    0xBA,
    0x78,
    0x25,
    0x2E,
    0x1C,
    0xA6,
    0xB4,
    0xC6,
    0xE8,
    0xDD,
    0x74,
    0x1F,
    0x4B,
    0xBD,
    0x8B,
    0x8A,
    0x70,
    0x3E,
    0xB5,
    0x66,
    0x48,
    0x03,
    0xF6,
    0x0E,
    0x61,
    0x35,
    0x57,
    0xB9,
    0x86,
    0xC1,
    0x1D,
    0x9E,
    0xE1,
    0xF8,
    0x98,
    0x11,
    0x69,
    0xD9,
    0x8E,
    0x94,
    0x9B,
    0x1E,
    0x87,
    0xE9,
    0xCE,
    0x55,
    0x28,
    0xDF,
    0x8C,
    0xA1,
    0x89,
    0x0D,
    0xBF,
    0xE6,
    0x42,
    0x68,
    0x41,
    0x99,
    0x2D,
    0x0F,
    0xB0,
    0x54,
    0xBB,
    0x16,
]
_RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


def _xtime(a: int) -> int:
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1)


def _mul2(a: int) -> int:
    return _xtime(a)


def _mul3(a: int) -> int:
    return _xtime(a) ^ a


def _xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def _aes128_expand_key(key: bytes) -> bytes:
    if len(key) != 16:
        raise ValueError("AES-128 key must be 16 bytes")
    expanded = bytearray(key)
    bytes_generated = 16
    rcon_iter = 1
    temp = list(expanded[-4:])
    while bytes_generated < 176:
        temp = list(expanded[-4:])
        if bytes_generated % 16 == 0:
            temp = temp[1:] + temp[:1]
            temp = [_SBOX[b] for b in temp]
            temp[0] ^= _RCON[rcon_iter]
            rcon_iter += 1
        for i in range(4):
            expanded.append(expanded[bytes_generated - 16] ^ temp[i])
            bytes_generated += 1
    return bytes(expanded)


def _aes_add_round_key(state: bytearray, round_key: bytes) -> None:
    for i in range(16):
        state[i] ^= round_key[i]


def _aes_sub_bytes(state: bytearray) -> None:
    for i in range(16):
        state[i] = _SBOX[state[i]]


def _aes_shift_rows(state: bytearray) -> None:
    # state is column-major: index = row + 4 * column
    state[1], state[5], state[9], state[13] = state[5], state[9], state[13], state[1]
    state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
    state[3], state[7], state[11], state[15] = state[15], state[3], state[7], state[11]


def _aes_mix_columns(state: bytearray) -> None:
    for c in range(4):
        i = 4 * c
        a0, a1, a2, a3 = state[i], state[i + 1], state[i + 2], state[i + 3]
        state[i] = _mul2(a0) ^ _mul3(a1) ^ a2 ^ a3
        state[i + 1] = a0 ^ _mul2(a1) ^ _mul3(a2) ^ a3
        state[i + 2] = a0 ^ a1 ^ _mul2(a2) ^ _mul3(a3)
        state[i + 3] = _mul3(a0) ^ a1 ^ a2 ^ _mul2(a3)


def _aes128_encrypt_block(block: bytes, expanded_key: bytes) -> bytes:
    if len(block) != 16:
        raise ValueError("AES block must be 16 bytes")
    state = bytearray(block)
    _aes_add_round_key(state, expanded_key[0:16])
    for round_index in range(1, 10):
        _aes_sub_bytes(state)
        _aes_shift_rows(state)
        _aes_mix_columns(state)
        _aes_add_round_key(
            state, expanded_key[16 * round_index : 16 * (round_index + 1)]
        )
    _aes_sub_bytes(state)
    _aes_shift_rows(state)
    _aes_add_round_key(state, expanded_key[160:176])
    return bytes(state)


def _pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len


def _aes128_cbc_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    if len(iv) != 16:
        raise ValueError("AES-CBC IV must be 16 bytes")
    expanded_key = _aes128_expand_key(key)
    prev = iv
    out = bytearray()
    for offset in range(0, len(data), 16):
        block = _xor_bytes(data[offset : offset + 16], prev)
        enc = _aes128_encrypt_block(block, expanded_key)
        out.extend(enc)
        prev = enc
    return bytes(out)


def encrypt_payload_fernet_compatible(compressed_bytes: bytes, password: str) -> bytes:
    """
    Create the same outer format as the original sender:
        salt(16 bytes) + raw Fernet token

    Fernet token format:
        0x80 | timestamp(8) | iv(16) | AES-CBC ciphertext | HMAC-SHA256(32)
    """
    salt = os.urandom(16)
    raw_key = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS, dklen=32
    )
    signing_key = raw_key[:16]
    encryption_key = raw_key[16:]
    iv = os.urandom(16)
    ciphertext = _aes128_cbc_encrypt(
        _pkcs7_pad(compressed_bytes, 16), encryption_key, iv
    )
    token_body = b"\x80" + struct.pack("!Q", int(time.time())) + iv + ciphertext
    tag = hmac.new(signing_key, token_body, hashlib.sha256).digest()
    return salt + token_body + tag


# ---------------------------------------------------------------------------
# QR/SVG and sender HTML generation
# ---------------------------------------------------------------------------


def die(message: str, exit_code: int = 1) -> None:
    print(f"エラー: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def read_file(path: Path) -> bytes:
    if not path.is_file():
        die(f"ファイルが見つかりません: {path}")
    return path.read_bytes()


def pack_payload(filename: str, file_bytes: bytes) -> bytes:
    filename_bytes = filename.encode("utf-8")
    if len(filename_bytes) > 255:
        die("ファイル名が長すぎます（UTF-8で255バイト以内）")
    return struct.pack("!B", len(filename_bytes)) + filename_bytes + file_bytes


def compress_payload(payload: bytes) -> bytes:
    return gzip.compress(payload, compresslevel=9)


def chunk_payload(payload: bytes, chunk_size: int) -> list[bytes]:
    if chunk_size <= 0:
        die("チャンクサイズは1以上にしてください")
    chunks = [payload[i : i + chunk_size] for i in range(0, len(payload), chunk_size)]
    if not chunks:
        chunks = [b""]
    if len(chunks) > MAX_CHUNKS:
        die(f"ファイルが大きすぎます（チャンク上限 {MAX_CHUNKS}）")
    return chunks


# ---------------------------------------------------------------------------
# Optional outer FEC for dropped QR frames
# ---------------------------------------------------------------------------

_GF_EXP = [0] * 512
_GF_LOG = [0] * 256
_x = 1
for _i in range(255):
    _GF_EXP[_i] = _x
    _GF_LOG[_x] = _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x11D
for _i in range(255, 512):
    _GF_EXP[_i] = _GF_EXP[_i - 255]


def _gf_mul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return _GF_EXP[_GF_LOG[a] + _GF_LOG[b]]


def _gf_inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError("GF inverse of zero")
    return _GF_EXP[255 - _GF_LOG[a]]


def _fec_coeff(row: int, col: int, data_count: int) -> int:
    # Cauchy matrix: x=row+data_count, y=col, entry = 1/(x xor y).
    # Rows are guaranteed to be disjoint from data columns while data_count + parity <= 255.
    return _gf_inv((data_count + row) ^ col)


def _xor_scaled(dst: bytearray, src: bytes, coef: int) -> None:
    if coef == 0:
        return
    if coef == 1:
        for i, b in enumerate(src):
            dst[i] ^= b
    else:
        for i, b in enumerate(src):
            if b:
                dst[i] ^= _gf_mul(coef, b)


def _build_legacy_qr_frames(chunks: list[bytes]) -> list[bytes]:
    return [
        struct.pack("!HH", idx + 1, len(chunks)) + chunk
        for idx, chunk in enumerate(chunks)
    ]


def _build_fec_qr_frames(
    payload: bytes, chunk_size: int, data_shards: int, parity_shards: int
) -> list[bytes]:
    if not (1 <= data_shards <= 128):
        die("FECデータシャード数は1〜128にしてください")
    if not (0 <= parity_shards <= 64):
        die("FECパリティ数は0〜64にしてください")
    if data_shards + parity_shards > 255:
        die("FECの data + parity は255以下にしてください")
    if len(payload) > 0xFFFFFFFF:
        die("FEC形式ではペイロードは4GiB未満にしてください")

    data_chunks = chunk_payload(payload, chunk_size)
    group_count = (len(data_chunks) + data_shards - 1) // data_shards
    if group_count > 0xFFFF:
        die(
            "FECグループ数が多すぎます。チャンクサイズを大きくするか、data-shardsを増やしてください"
        )

    total_frames = 0
    group_sizes: list[int] = []
    for group_start in range(0, len(data_chunks), data_shards):
        count = min(data_shards, len(data_chunks) - group_start)
        group_sizes.append(count)
        total_frames += count + parity_shards
    if total_frames > MAX_CHUNKS:
        die(f"FEC込みの総QRフレーム数が多すぎます（上限 {MAX_CHUNKS}）")

    frames: list[bytes] = []
    frame_no = 1
    for group_index, group_start in enumerate(range(0, len(data_chunks), data_shards)):
        data_count = group_sizes[group_index]
        group = []
        for chunk in data_chunks[group_start : group_start + data_count]:
            group.append(chunk.ljust(chunk_size, b"\x00"))

        shares = list(group)
        for parity_index in range(parity_shards):
            parity = bytearray(chunk_size)
            for col, shard in enumerate(group):
                _xor_scaled(parity, shard, _fec_coeff(parity_index, col, data_count))
            shares.append(bytes(parity))

        for share_index, share_payload in enumerate(shares):
            header = struct.pack(
                "!2sBBHHHHHBBBBI",
                FEC_MAGIC,
                FEC_VERSION,
                0,
                frame_no,
                total_frames,
                group_index,
                group_count,
                group_start,
                data_count,
                parity_shards,
                share_index,
                0,
                len(payload),
            )
            frames.append(header + share_payload)
            frame_no += 1
    return frames


def make_qr_svg(qr_payload_bytes: bytes, error_level: str) -> str:
    qrcode = _install_vendored_qrcode()
    level_map = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }
    qr = qrcode.QRCode(
        version=None,
        error_correction=level_map[error_level],
        box_size=1,
        border=1,
    )
    qr.add_data(qr_payload_bytes)
    qr.make(fit=True)
    matrix = qr.get_matrix()  # includes border
    size = len(matrix)

    # A compact SVG: consecutive dark modules in each row are emitted as horizontal runs.
    path_parts: list[str] = []
    for r, row in enumerate(matrix):
        c = 0
        while c < size:
            if not row[c]:
                c += 1
                continue
            start = c
            while c < size and row[c]:
                c += 1
            width = c - start
            path_parts.append(f"M{start},{r}h{width}v1H{start}z")

    path_data = "".join(path_parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
        f'shape-rendering="crispEdges"><rect width="100%" height="100%" fill="#fff"/>'
        f'<path fill="#000" d="{path_data}"/></svg>'
    )


def write_html_header(
    out,
    *,
    filename: str,
    total_chunks: int,
    delay_ms: int,
    encrypted: bool,
    fec_label: str = "FECなし",
) -> None:
    safe_filename = html.escape(filename, quote=True)
    badge_class = "badge-secure" if encrypted else "badge-none"
    security_state = "暗号化保護あり" if encrypted else "暗号化なし (平文)"
    safe_fec_label = html.escape(fec_label, quote=True)

    out.write(f"""<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <title>Animated QR Streamer</title>
    <style>
        :root {{ --bg: #090d16; --panel: #131c2e; --accent: #38bdf8; --accent-glow: rgba(56, 189, 248, 0.3); --text: #f8fafc; --text-mut: #64748b; }}
        body {{ font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }}
        .wrapper {{ background: var(--panel); border: 1px solid #1e293b; padding: 32px; border-radius: 24px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7); width: 440px; text-align: center; }}
        h3 {{ margin: 0 0 4px 0; font-size: 20px; letter-spacing: 0.5px; }}
        .file-info {{ color: var(--text-mut); font-size: 13px; margin-bottom: 20px; word-break: break-all; }}
        .badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-bottom: 15px; }}
        .badge-secure {{ background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }}
        .badge-none {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }}
        .qr-viewport {{ width: 360px; height: 360px; background: white; padding: 16px; border-radius: 16px; margin: 0 auto 24px auto; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 30px var(--accent-glow); position: relative; }}
        .qr-frame {{ display: none; width: 100%; height: 100%; }}
        .qr-frame[active="true"] {{ display: block; }}
        svg {{ width: 100%; height: 100%; }}
        .control-row {{ display: flex; justify-content: center; gap: 12px; margin-bottom: 24px; }}
        button {{ background: #1e293b; color: white; border: 1px solid #334155; padding: 10px 18px; font-size: 14px; font-weight: 600; border-radius: 8px; cursor: pointer; transition: all 0.15s; min-width: 70px; }}
        button:hover {{ background: #334155; border-color: var(--accent); }}
        button#play-btn {{ background: var(--accent); color: #090d16; border: none; min-width: 100px; }}
        button#play-btn:hover {{ opacity: 0.9; }}
        .slider-group {{ background: #0f172a; padding: 14px 18px; border-radius: 12px; margin-bottom: 12px; text-align: left; border: 1px solid #1e293b; }}
        .slider-label {{ display: flex; justify-content: space-between; font-size: 12px; color: var(--text-mut); margin-bottom: 6px; font-weight: 500; }}
        .slider-label span {{ color: var(--accent); font-family: monospace; }}
        input[type="range"] {{ width: 100%; margin: 0; cursor: pointer; accent-color: var(--accent); }}
    </style>
</head>
<body>
    <div class="wrapper">
        <h3>Animated QR Streamer</h3>
        <div class="file-info">対象: {safe_filename}</div>
        <div class="badge {badge_class}">{security_state}</div>
        <div class="file-info">{safe_fec_label} / QRフレーム: {total_chunks}</div>
        <div class="qr-viewport">
""")


def write_html_footer(
    out, *, total_chunks: int, delay_ms: int, randomize: bool
) -> None:
    max_idx = max(0, total_chunks - 1)
    random_js = "true" if randomize else "false"
    mode_label = "ランダム表示" if randomize else "連番表示"
    out.write(f"""        </div>
        <div class="file-info">表示: {mode_label}</div>
        <div class="slider-group">
            <div class="slider-label">進捗シーク <span id="counter">1 / {total_chunks}</span></div>
            <input type="range" id="seek-slider" min="0" max="{max_idx}" value="0" oninput="seekFrame(this.value)">
        </div>
        <div class="slider-group">
            <div class="slider-label">再生速度 <span id="speed-val">{delay_ms}ms</span></div>
            <input type="range" id="speed-slider" min="50" max="1000" step="25" value="{delay_ms}" oninput="changeSpeed(this.value)">
        </div>
        <div class="control-row">
            <button onclick="stepFrame(-1)">◀</button>
            <button id="play-btn" onclick="togglePlay()">一時停止</button>
            <button onclick="resetAnimation()">リセット</button>
            <button onclick="stepFrame(1)">▶</button>
        </div>
    </div>
    <script>
        const frames = Array.from(document.querySelectorAll('.qr-frame'));
        const total = frames.length;
        const randomize = {random_js};
        let current = 0, timer = null, delay = {delay_ms};
        let order = Array.from({{length: total}}, (_, i) => i);
        let orderPos = 0;
        const seekSlider = document.getElementById('seek-slider'), speedVal = document.getElementById('speed-val'), counter = document.getElementById('counter'), playBtn = document.getElementById('play-btn');

        function shuffleOrder() {{
            order = Array.from({{length: total}}, (_, i) => i);
            for (let i = order.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [order[i], order[j]] = [order[j], order[i]];
            }}
            orderPos = 0;
        }}

        function showFrame(idx) {{
            if (!total) return;
            frames[current].removeAttribute('active');
            current = (idx + total) % total;
            frames[current].setAttribute('active', 'true');
            seekSlider.value = current;
            counter.innerText = `${{current + 1}} / ${{total}}`;
        }}

        function showOrderPosition(pos) {{
            if (!total) return;
            if (pos >= total || pos < 0) {{
                if (randomize) shuffleOrder();
                pos = pos < 0 ? total - 1 : 0;
            }}
            orderPos = pos;
            showFrame(order[orderPos]);
        }}

        function nextFrame() {{
            if (randomize) showOrderPosition(orderPos + 1);
            else showFrame(current + 1);
        }}

        function stepFrame(dir) {{
            stop();
            if (randomize) showOrderPosition(orderPos + dir);
            else showFrame(current + dir);
        }}

        function play() {{ if (!timer && total > 1) {{ timer = setInterval(nextFrame, delay); playBtn.innerText = "一時停止"; playBtn.style.background = "var(--accent)"; }} }}
        function stop() {{ if (timer) {{ clearInterval(timer); timer = null; playBtn.innerText = "再生"; playBtn.style.background = "white"; }} }}
        function togglePlay() {{ if (timer) stop(); else play(); }}
        function resetAnimation() {{ stop(); if (randomize) {{ shuffleOrder(); showOrderPosition(0); }} else showFrame(0); }}
        function changeSpeed(val) {{ delay = parseInt(val); speedVal.innerText = `${{delay}}ms`; if (timer) {{ stop(); play(); }} }}
        function seekFrame(val) {{
            stop();
            showFrame(parseInt(val));
            if (randomize) {{
                const pos = order.indexOf(current);
                orderPos = pos >= 0 ? pos : 0;
            }}
        }}

        if (randomize) {{ shuffleOrder(); showOrderPosition(0); }}
        play();
    </script>
</body>
</html>
""")


def write_sender_html(
    output_path: Path,
    *,
    filename: str,
    qr_frames: list[bytes],
    level: str,
    delay_ms: int,
    encrypted: bool,
    fec_label: str = "FECなし",
    randomize: bool = True,
) -> None:
    tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        with tmp_path.open("w", encoding="utf-8", newline="") as out:
            write_html_header(
                out,
                filename=filename,
                total_chunks=len(qr_frames),
                delay_ms=delay_ms,
                encrypted=encrypted,
                fec_label=fec_label,
            )
            for idx, qr_payload in enumerate(qr_frames):
                svg = make_qr_svg(qr_payload, level)
                active = ' active="true"' if idx == 0 else ""
                out.write(f'            <div class="qr-frame"{active}>{svg}</div>\n')
            write_html_footer(
                out, total_chunks=len(qr_frames), delay_ms=delay_ms, randomize=randomize
            )
        tmp_path.replace(output_path)
    except Exception:
        try:
            tmp_path.unlink(missing_ok=True)
        finally:
            raise


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="QR Air sender generator - standalone / stdlib-only edition"
    )
    parser.add_argument("input", help="変換したい入力ファイルのパス")
    parser.add_argument(
        "-o", "--output", default="output.html", help="出力HTMLファイル名"
    )
    parser.add_argument(
        "-l",
        "--level",
        choices=["L", "M", "Q", "H"],
        default="L",
        help="誤り訂正レベル（デフォルト: L）",
    )
    parser.add_argument("-k", "--key", default=None, help="暗号化パスワード")
    parser.add_argument(
        "-c",
        "--chunk",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"1フレームあたりのデータサイズ[Byte]（デフォルト: {DEFAULT_CHUNK_SIZE}）",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=int,
        default=DEFAULT_DELAY_MS,
        help=f"フレーム切り替え速度[ms]（デフォルト: {DEFAULT_DELAY_MS}）",
    )
    parser.add_argument(
        "--fec-parity",
        type=int,
        default=2,
        help="各FECグループに追加する復元用QR枚数（0で無効、デフォルト: 2）",
    )
    parser.add_argument(
        "--fec-data",
        type=int,
        default=8,
        help="FEC 1グループあたりのデータQR枚数（デフォルト: 8）",
    )
    parser.add_argument(
        "--sequential",
        action="store_true",
        help="QRをランダムシャッフルせず、従来どおり連番順で表示",
    )
    parser.add_argument(
        "--print-vendored-license",
        action="store_true",
        help="内蔵している qrcode 8.2 のライセンスを表示して終了",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.print_vendored_license:
        print(_QRCODE_LICENSE)
        return
    if args.delay <= 0:
        die("フレーム切り替え速度は1ms以上にしてください")

    input_path = Path(args.input)
    output_path = Path(args.output)

    file_bytes = read_file(input_path)
    filename = input_path.name

    print("-" * 50)
    print(f"📄 対象ファイル: {filename}")

    packed_data = pack_payload(filename, file_bytes)
    compressed_bytes = compress_payload(packed_data)
    print(f"📉 圧縮: {len(file_bytes)}B ➔ {len(compressed_bytes)}B")

    if args.key:
        print("🔒 暗号化を実行中...（stdlib-only Fernet互換）")
        final_payload_bytes = encrypt_payload_fernet_compatible(
            compressed_bytes, args.key
        )
    else:
        print("🔓 暗号化なし")
        final_payload_bytes = compressed_bytes

    if args.fec_parity > 0:
        qr_frames = _build_fec_qr_frames(
            final_payload_bytes, args.chunk, args.fec_data, args.fec_parity
        )
        raw_chunks = chunk_payload(final_payload_bytes, args.chunk)
        fec_label = f"FECあり: data={args.fec_data}, parity={args.fec_parity}"
        print(
            f"📦 元データチャンク数: {len(raw_chunks)} 枚 (1チャンク約: {args.chunk} Byte)"
        )
        print(
            f"🧩 FEC込み総QRフレーム数: {len(qr_frames)} 枚（各グループ最大 {args.fec_parity} 枚欠損まで復元可能）"
        )
    else:
        chunks = chunk_payload(final_payload_bytes, args.chunk)
        qr_frames = _build_legacy_qr_frames(chunks)
        fec_label = "FECなし"
        print(f"📦 総フレーム数: {len(qr_frames)} 枚 (1フレーム約: {args.chunk} Byte)")
    print("🎨 QRコード(SVG)を生成中...（PIL/Pillow不使用）")
    print(f"🔀 表示順: {'連番' if args.sequential else 'ランダムシャッフル'}")

    write_sender_html(
        output_path,
        filename=filename,
        qr_frames=qr_frames,
        level=args.level,
        delay_ms=args.delay,
        encrypted=bool(args.key),
        fec_label=fec_label,
        randomize=not args.sequential,
    )

    print("-" * 50)
    print(f"🎉 送信画面: {output_path}")
    print("依存: Python標準ライブラリのみ")


if __name__ == "__main__":
    main()
