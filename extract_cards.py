#!/usr/bin/env python3
"""
Extract Dutch vocabulary card illustrations from PDF.
Uses explicit (y_start, y_sep) pairs per row instead of auto-detection.
Each y_sep is set 2-4 px above the actual label/border line so the crop
contains the full illustration and no label text.
"""

import fitz
from PIL import Image
import io, os

PDF = "/Users/alexeyivanov/Library/CloudStorage/Dropbox/_Obsidian/Alex Ivanov Personal Vault/KNOWLEDGE/DUTCH - LEARNING/Dutch_vocab_outline_A4_landscape (1).pdf"
OUT_DIR = "/Users/alexeyivanov/Library/CloudStorage/Dropbox/_Obsidian/Alex Ivanov Personal Vault/KNOWLEDGE/DUTCH - LEARNING/card_images"

os.makedirs(OUT_DIR, exist_ok=True)
doc = fitz.open(PDF)

def get_page_img(page_num):
    page = doc[page_num]
    xref = page.get_images(full=True)[0][0]
    return Image.open(io.BytesIO(doc.extract_image(xref)["image"]))

MX = 5   # inner margin on left/right
MY = 5   # inner margin on top

def crop_cells(img, row_bounds, col_bounds):
    """row_bounds: list of (y_start, y_cut), col_bounds: list of (x_start, x_end)"""
    crops = []
    for (ry1, ry2) in row_bounds:
        for (cx1, cx2) in col_bounds:
            crop = img.crop((cx1 + MX,  ry1 + MY,
                             cx2 - MX,  ry2 - 2))
            crops.append(crop)
    return crops

# ── Explicit cell bounds: (y_start, y_cut) where y_cut is BEFORE the label ───
# Each y_cut is 3-5px above the actual separator/label-text row.

# PAGE 1
P1_TOP_ROWS    = [(60, 188), (228, 354), (390, 497)]
P1_BOT_L_ROWS  = [(593, 715), (752, 872), (908, 1026)]  # huishouden activities
P1_BOT_R_ROWS  = [(584, 703), (734, 852), (884, 1012)]  # servies (no section title)
P1_L_COLS      = [(70, 285), (285, 489), (489, 681)]
P1_R_COLS      = [(765, 977), (977, 1185), (1185, 1378)]

# PAGE 2 — clothing seps at 139, 291, 453; row 4 sep around 580; shoe seps at 758, 902, 1045
P2_CLO_ROWS    = [(15, 136), (165, 289), (314, 450)]
P2_CLO_ROW4    = [(458, 578)]
P2_CLO_L       = [(61, 262), (272, 471), (480, 679)]
P2_CLO_R       = [(751, 947), (956, 1142), (1151, 1333)]
P2_SHOE_ROWS   = [(621, 755), (763, 899), (908, 1042)]
P2_SHL_COLS    = [(65, 262), (271, 471), (480, 679)]
P2_SHR_COLS    = [(755, 939), (947, 1142), (1151, 1333)]

# PAGE 3 — animal row seps at 183, 336, 502 ; bos/sport seps near 740, 879, 1040
P3_ANI_ROWS    = [(15, 180), (192, 333), (366, 498)]
P3_ANI_COLS    = [(152, 352), (358, 553), (562, 753), (762, 947), (956, 1151)]
P3_BOS_ROWS    = [(586, 737), (748, 876), (900, 1037)]
P3_BOS_COLS    = [(143, 325), (333, 512), (520, 698)]
P3_SPO_ROWS    = [(586, 737), (748, 876), (900, 1037)]
P3_SPO_COLS    = [(762, 947), (957, 1126), (1150, 1308)]

# PAGE 4 — prof seps at 202, 385, 497; build seps at 749, 899, 1039
P4_PRF_ROWS    = [(50, 199), (230, 382), (411, 494)]
P4_BLD_ROWS    = [(615, 746), (780, 896), (924, 1036)]
P4_L_COLS      = [(93, 275), (290, 469), (489, 666)]
P4_R_COLS      = [(763, 943), (963, 1147), (1169, 1351)]

# PAGE 5 — post labels at y=235, 440, 535; cut just before them
P5_PST_ROWS    = [(45, 228), (260, 435), (465, 528)]
P5_PST_L       = [(92, 283), (297, 482), (497, 685)]
P5_PST_R       = [(742, 934), (947, 1140), (1156, 1351)]
# Body — seps at 781, 911, 1040 (row 3 estimate)
P5_BOD_ROWS    = [(615, 778), (807, 908)]
P5_BOD_ROW3    = [(938, 1037)]
P5_BOD_COLS5   = [(75, 335), (335, 595), (595, 855), (855, 1115), (1115, 1375)]
P5_BOD_COLS4   = [(75, 335), (335, 595), (595, 855), (855, 1115)]

SECTIONS = [
    # PAGE 1
    (0, P1_TOP_ROWS,   P1_L_COLS, [
        'emmer','spons','ramentrekker',
        'plumeau','schuurspons','bezem',
        'stoffer','blik','handschoenen',
    ]),
    (0, P1_TOP_ROWS,   P1_R_COLS, [
        'mop','stofzuiger','teil',
        'borstel','stofdoeken','wasmiddel',
        'wasmand','sop','strijkplank',
    ]),
    (0, P1_BOT_L_ROWS, P1_L_COLS, [
        'koken','afwassen','afdrogen',
        'opruimen','stofzuigen','boodschappen',
        'wassen','naaien','schoonmaken',
    ]),
    (0, P1_BOT_R_ROWS, P1_R_COLS, [
        'lepel','beker','glas',
        'kopje','schotel','schaaltje',
        'bord','vork','mes',
    ]),
    # PAGE 2
    (1, P2_CLO_ROWS,   P2_CLO_L, [
        'bril','broek','handschoenen2',
        'laars','onderbroek','overhemd',
        'rok','rugzak','schoen',
    ]),
    (1, P2_CLO_ROWS,   P2_CLO_R, [
        'handtas','hoed','jurk',
        'paraplu','pet','riem',
        'sjaal','slipje','sokken',
    ]),
    (1, P2_CLO_ROW4,   P2_CLO_L[:2], ['stropdas','t-shirt']),
    (1, P2_SHOE_ROWS,  P2_SHL_COLS, [
        'schoen2','laars2','teenslippers',
        'instapper','boot','pump',
        'sandalen','klomp','sneakers',
    ]),
    (1, P2_SHOE_ROWS,  P2_SHR_COLS, [
        'passpiegel','doos','kassa',
        'pinapparaat','bord2','voetmeter',
        'veter','zool','hak',
    ]),
    # PAGE 3
    (2, P3_ANI_ROWS,   P3_ANI_COLS, [
        'bij','hond','kat','kip','koe',
        'krokodil','leeuw','olifant','slak','spin',
        'vis','vlinder','vogel','konijn','paard',
    ]),
    (2, P3_BOS_ROWS,   P3_BOS_COLS, [
        'vos','egel','wolf',
        'haas','uil','zwijn',
        'ree','hert','eekhoorn',
    ]),
    (2, P3_SPO_ROWS,   P3_SPO_COLS, [
        'gewichten','fiets','tennisracket',
        'basketbal','surfplank','frisbee',
        'knuppel','doel','voetbal',
    ]),
    # PAGE 4
    (3, P4_PRF_ROWS,   P4_L_COLS, [
        'bakker','dokter','timmervrouw',
        'lerares','schoonmaker','politieagent',
        'muzikant','secretaresse','glaszetter',
    ]),
    (3, P4_PRF_ROWS,   P4_R_COLS, [
        'astronaut','boerin','brandweerman',
        'architect','clown','wetenschapper',
        'stewardess','kok','metselaar',
    ]),
    (3, P4_BLD_ROWS,   P4_L_COLS, [
        'metselen','emmer2','troffel',
        'cementmolen','betonmixer','stenen',
        'muur','kruiwagen', None,
    ]),
    (3, P4_BLD_ROWS,   P4_R_COLS, [
        'timmerman','planken','rolmaat',
        'spijkers','hamer','schroeven',
        'schroevendraaier','moeren','zaag',
    ]),
    # PAGE 5
    (4, P5_PST_ROWS,   P5_PST_L, [
        'postbode','brievenbus','postfiets',
        'kaart','envelop','postzegel',
        'posttas','stempel','huisnummer',
    ]),
    (4, P5_PST_ROWS,   P5_PST_R, [
        'pakket','pakketzegel','wegen',
        'bezorger','postnl_auto','handtekening',
        'sorteerkast','postbussen','postduif',
    ]),
    (4, P5_BOD_ROWS,   P5_BOD_COLS5, [
        'arm','hand','longen','mond','neus',
        'tand','tong','voet','been','bot',
    ]),
    (4, P5_BOD_ROW3,   P5_BOD_COLS4, [
        'hart','hoofd','oog','oor',
    ]),
]

page_cache = {}
saved = []
for sect in SECTIONS:
    page_num, row_bounds, col_bounds, words = sect
    if page_num not in page_cache:
        page_cache[page_num] = get_page_img(page_num)
    img = page_cache[page_num]
    crops = crop_cells(img, row_bounds, col_bounds)
    for word, crop in zip(words, crops):
        if word is None: continue
        crop.save(os.path.join(OUT_DIR, f"{word}.png"), 'PNG', optimize=True)
        saved.append(word)

print(f"Done: {len(saved)} images")
