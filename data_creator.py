import os
import subprocess as sp

def make_data_set(path):
    info_index = 1
    for img in os.listdir(path):
        path_to_image = path + img
        info_output = 'info/info' + str(info_index) + '.lst'

        sp.run(
            ['opencv_createsamples', '-img', path_to_image, '-bg', 'bg.txt', '-info', info_output, '-pngoutput',
             'info', '-maxxangle', '0.5', '-maxyangle', '0.5', '-maxzangle', '0.5', '-num', '550'])

        print('Processing... Done ', info_index, ' out from ', len(os.listdir(path)))
        info_index += 1

make_data_set('pos/')

print(len([name for name in os.listdir('pos/') if os.path.isfile(name)]))
