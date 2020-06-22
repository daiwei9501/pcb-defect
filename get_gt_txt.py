#----------------------------------------------------#
#   获取测试集的ground-truth
#----------------------------------------------------#
import sys
import os
import glob
import xml.etree.ElementTree as ET


xmlfilepath=r'./model_data/label_train/'
temp_xml = os.listdir(xmlfilepath)
total_xml = []
for xml in temp_xml:
    if xml.endswith(".xml"):
        total_xml.append(xml)

ftrain = open('image_list.txt', 'w')
for i in range(len(total_xml)):
    name = total_xml[i][:-4] + '\n'
    ftrain.write(name)
ftrain.close()


image_ids = open('image_list.txt').read().strip().split()
print(image_ids)
if not os.path.exists("./input"):
    os.makedirs("./input")
if not os.path.exists("./input/ground-truth"):
    os.makedirs("./input/ground-truth")

for image_id in image_ids:
    with open("./input/ground-truth/"+image_id+".txt", "w") as new_f:
        root = ET.parse("model_data/label_train/" + image_id+".xml").getroot()
        for obj in root.findall('object'):
            if obj.find('difficult')!=None:
                difficult = obj.find('difficult').text
                if int(difficult)==1:
                    continue
            obj_name = obj.find('name').text
            if obj_name == 'double':
                print(image_id)
            bndbox = obj.find('bndbox')
            left = bndbox.find('xmin').text
            top = bndbox.find('ymin').text
            right = bndbox.find('xmax').text
            bottom = bndbox.find('ymax').text
            new_f.write("%s %s %s %s %s\n" % (obj_name, left, top, right, bottom))
            
print("Conversion completed!")
