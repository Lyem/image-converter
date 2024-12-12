from PySimpleGUI import PySimpleGUI as sg
from wand.image import Image as WandImage
import math
import os
import time
sg.theme('DarkBlue9')

options = [".jpg", ".png", ".webp"]

layout = [
    [sg.Text('Select your files:')],
    [sg.Input(key='_FILES_',disabled_readonly_background_color='black', readonly=True), 
     sg.FilesBrowse('Select',file_types=(('image', '*.png'),('image', '*.jpg'),('image', '*.webp'),('image', '*.jpeg'),('image', '*.JPG'),('image', '*.PNG'),('image', '*.JPEG'),('image', '*.WEBP'),('image', '*.PNG'),('image', '*.bmp'),('image', '*.BMP'),('image', '*.dds'),('image', '*.DDS'),('image', '*.dib'),('image', '*.DIB'),('image', '*.eps'),('image', '*.EPS'),('image', '*.icns'),('image', '*.ICNS'),('image', '*.ico'),('image', '*.ICO'),('image', '*.bmp'),('image', '*.BMP'),('image', '*.avif')))],
    [sg.Text('Convert to:')],
    [sg.OptionMenu(key='type',values=options)],
    [sg.Text('Slice Files:'), sg.Checkbox('', default=False, key="_SLICE_")],
    [sg.Input(key='_TOP_', readonly=False, default_text='10000'), sg.Input(key='_TOP2_', readonly=False, default_text='5000')],
    [sg.Button('To convert')],
    [sg.ProgressBar(100, orientation='h', border_width=4, key='progbar', bar_color=['Green','Black'])]
]

window = sg.Window('Image converter', layout)

while True:
    events, values = window.read()

    if events == sg.WINDOW_CLOSED:
        break

    if events == 'To convert':
        if not os.path.isdir(os.path.join('converted')):
            os.makedirs(os.path.join('converted'))
        page_number = 1
        if(values['_FILES_'] != "" and values['type'] != ""):
            file_list = values['_FILES_'].split(';')
            total_files = len(file_list)
            for image_path in file_list:
                with WandImage(filename=image_path) as img:
                    icc_profile = img.profiles.get('icc')

                    if img.alpha_channel:
                        img.alpha_channel = 'remove'

                    if img.type == 'palette':
                        img.type = 'truecolor'
                    
                    width, height = img.width, img.height

                    img.compression_quality = 80
                    img.density = (72, 72)

                    if(height > int(values['_TOP_']) and values['_SLICE_']):
                        top = 0
                        left = 0
                        slice_height = int(values['_TOP2_'])
                        slices = int(math.ceil(height / slice_height))
                        count = 1
                        for s in range(slices):
                            if count == slices:
                                bottom = height
                            else:
                                bottom = count * slice_height

                            img_slice = img.clone()
                            crop_width = width - left
                            crop_height = bottom - top
                            img_slice.crop(left=left, top=top, width=crop_width, height=crop_height)

                            if icc_profile:
                                img_slice.profiles['icc'] = icc_profile

                            img_slice.compression_quality = 80
                            img_slice.density = (72, 72)
                            
                            img_slice.save(filename=os.path.join('converted', f"%03d{values['type']}" % page_number))
                            top += slice_height
                            count += 1
                            page_number += 1
                    else:
                        if icc_profile:
                            img.profiles['icc'] = icc_profile

                        img.save(filename=os.path.join('converted', f"%03d{values['type']}" % page_number))
                        window['progbar'].update_bar(int((page_number * 100) / total_files))
                        page_number += 1
            time.sleep(0.1)
            window['progbar'].update_bar(0)
