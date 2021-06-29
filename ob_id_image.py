# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:28:50 2019

@author: qingyang
"""

# Import packages
import os
#import cv2
import numpy as np
import tensorflow as tf
#import json
from utils import label_map_util
import sys
from PIL import Image, ImageFont, ImageDraw
sys.path.append("..")

#image_resize = Image.open('test.png').convert("RGB")
#img = image_resize.resize((378, 504),Image.ANTIALIAS)
#img.save('ouput_image.png', "PNG")
def identification():
    CWD_PATH = os.getcwd()
    MODEL_NAME = 'inference_graph'
    IMAGE_NAME = CWD_PATH+"/images/"+'/part_image.png'
    
    
    # for object detection.
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph3.pb')
    
    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap3.pbtxt')
    
    NUM_CLASSES = 6
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
#    category_index = label_map_util.create_category_index(categories)
    
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    
        sess = tf.Session(graph=detection_graph)
        
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    
    # Output tensors are the detection boxes, scores, and classes
    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    
    # Each score represents level of confidence for each of the objects.
    # The score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    
    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    
#    image = cv2.imread(IMAGE_NAME)
    image_draw = Image.open(IMAGE_NAME).convert("RGB")
    image_draw = image_draw.resize((378, 504),Image.ANTIALIAS)
    image = np.array(image_draw)
    image_expanded = np.expand_dims(image, axis=0)
    
    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})
    
    # Draw the results of the detection (aka 'visulaize the results')
    
    part_image=image
    height_part_image, width_part_image = part_image.shape[:2]
    
    thershold = (scores[0] >= 0.8)
    thershold_sum = sum(thershold)
    for i in range(0,thershold_sum):
        
        # Draw the results of the detection (aka 'visulaize the results')
        y_min = boxes[0][i][0]
        x_min = boxes[0][i][1]
        y_max = boxes[0][i][2]
        x_max = boxes[0][i][3]
        
        tag_id  = int(classes[0][i])
        tag_name = categories[tag_id-1]['name']
        tag_scores = round(scores[0][i]*100,2)
        
        left, right, top, bottom = x_min*width_part_image,x_max*width_part_image,y_min*height_part_image,y_max*height_part_image
        draw = ImageDraw.Draw(image_draw)
        draw.rectangle(((int(left), int(top)), (int(right), int(bottom))),outline=(0,255,0))
        draw.text((int(left), int(top)), tag_name,fill=(255,0,0,255),font=ImageFont.truetype("GOTHIC.TTF",14))
        draw.text((int(left), int(bottom)), str(tag_scores)+'%',fill=(0,0,255,255),font=ImageFont.truetype("GOTHIC.TTF",14))
#        cv2.rectangle(part_image,(int(left),int(top)),(int(right) ,int(bottom)),(0,255,0),2)
#        cv2.putText(part_image, tag_name, (int(left),int(top)), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255), 1, cv2.LINE_AA)
#        cv2.putText(part_image, str(tag_scores)+'%', (int(left),int(bottom)), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,0,0), 1, cv2.LINE_AA)

    
#    cv2.imwrite(CWD_PATH+"/images/"+'ouput_image.png',part_image) 
    image_draw.save(CWD_PATH+"/images/"+'ouput_image.png', "PNG")
    
    
    
    
    
    
    
    
    
    