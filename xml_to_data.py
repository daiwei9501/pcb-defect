import xml.etree.ElementTree as ET
from os import getcwd


classes = ['missing_hole', 'mouse_bite', 'open_circuit', 'short', 'spur', 'spurious_copper']

def convert_annotation(image_id, list_file):
    in_file = open('model_data/label_train/%s.xml'%(image_id), encoding='UTF-8')
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
wd = getcwd()

import os


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        list_name.append(file.replace('.jpg',''))

image_ids = []
listdir('model_data/train', image_ids)
#print(image_ids)

list_file = open('model_data/train.txt', 'w', encoding='UTF-8')
for image_id in image_ids:
    list_file.write('model_data/train/%s.jpg'%(image_id))
    convert_annotation(image_id, list_file)
    list_file.write('\n')
list_file.close()

