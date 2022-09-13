from PySimpleGUI import PySimpleGUI as sg
from PIL import Image
import math
import os
Image.MAX_IMAGE_PIXELS = 933120000
import time
sg.theme('DarkBlue9')

options = [".jpg", ".png", ".webp"]

layout = [
    [sg.Text('Select your files:')],
    [sg.Input(key='_FILES_',disabled_readonly_background_color='black', readonly=True), sg.FilesBrowse('Select',file_types=(('image', '*.png'),('image', '*.jpg'),('image', '*.webp'),('image', '*.jpeg'),('image', '*.JPG'),('image', '*.PNG'),('image', '*.JPEG'),('image', '*.WEBP'),('image', '*.PNG'),('image', '*.bmp'),('image', '*.BMP'),('image', '*.dds'),('image', '*.DDS'),('image', '*.dib'),('image', '*.DIB'),('image', '*.eps'),('image', '*.EPS'),('image', '*.icns'),('image', '*.ICNS'),('image', '*.ico'),('image', '*.ICO'),('image', '*.bmp'),('image', '*.BMP')))],
    [sg.Text('Convert to:')],
    [sg.OptionMenu(key='type',values=options)],
    [sg.Text('Slice Files:'),sg.Checkbox('', default=False, key="_SLICE_")],
    [sg.Input(key='_TOP_', readonly=False, default_text='10000'),sg.Input(key='_TOP2_', readonly=False, default_text='5000')],
    [sg.Button('To convert')],
    [sg.ProgressBar(100, orientation='h', border_width=4, key='progbar',bar_color=['Green','Black'])]
]

window = sg.Window('Image converter', layout)

while True:
    events, values = window.read()

    if events == sg.WINDOW_CLOSED:
        break

    if events == 'To convert':
        if os.path.isdir(os.path.join('converted')) == False: 
            os.makedirs(os.path.join('converted'))
        page_number = 1
        if(values['_FILES_'] != "" and values['type'] != ""):
            for image in values['_FILES_'].split(';'):
                img = Image.open(image)
                icc = img.info.get('icc_profile')
                if img.mode in ("RGBA", "P"): img = img.convert("RGB")
                width, height = img.size
                if(height > int(values['_TOP_']) and values['_SLICE_']):
                    top = 0
                    left = 0
                    slices = int(math.ceil(height/int(values['_TOP2_'])))
                    count = 1
                    for slice in range(slices):
                        if count == slices:
                            bottom = height
                        else:
                            bottom = int(count * int(values['_TOP2_']))  

                        box = (left, top, width, bottom)
                        img_slice = img.crop(box)
                        top += int(values['_TOP2_'])
                        img_slice.save(os.path.join('converted',f"%03d{values['type']}" % page_number), quality=80, dpi=(72, 72), icc_profile=icc)
                        count += 1
                        page_number += 1
                else:
                    img.save(os.path.join('converted',f"%03d{values['type']}" % page_number), quality=80, dpi=(72, 72), icc_profile=icc)
                    window['progbar'].update_bar(int((page_number * 100)/len(values['_FILES_'].split(';'))))
                    page_number += 1
            time.sleep(0.1)
            window['progbar'].update_bar(0)
