import xml.etree.ElementTree as ET

def convert_voc_to_yolo(voc_annotation_file, yolo_annotation_file):
    tree = ET.parse(voc_annotation_file)
    root = tree.getroot()
    
    image_width = int(root.find('size/width').text)
    image_height = int(root.find('size/height').text)
    
    with open(yolo_annotation_file, 'w') as yolo_file:
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            class_id = 0 if class_name == 'validation' else -1  # Assuming 'validation' is the only class, and its ID is 0
            
            xmin = int(obj.find('bndbox/xmin').text)
            ymin = int(obj.find('bndbox/ymin').text)
            xmax = int(obj.find('bndbox/xmax').text)
            ymax = int(obj.find('bndbox/ymax').text)
            
            x_center = (xmin + xmax) / 2.0 / image_width
            y_center = (ymin + ymax) / 2.0 / image_height
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height
            
            yolo_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

import os

xmls = os.listdir(os.getcwd())

for xml in xmls:
    convert_voc_to_yolo(xml, xml[:-4] + '.txt')
