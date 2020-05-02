from __future__ import print_function
# best model until now
import argparse
import glob
import os
import sys
import json
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path", help='/Users/edacaner/Desktop/FLIR-new/FLIR_ADAS_1_3/val/')
    parser.add_argument(
        "--output_path", help='/Users/edacaner/Desktop/FLIR-new/FLIR_ADAS_1_3/val/txtFiles/')
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    json_files = sorted(glob.glob(os.path.join('/Users/edacaner/Desktop/FLIR-new/FLIR_ADAS_1_3/val/', 'thermal_annotations.json')))
    if args.debug:
        total_count = 0
        cats = {0: 0, 1: 0, 2: 0}
        bike_images = set()
    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)
            info = data['info']
            categories = data['categories']
            annotations = data['annotations']
            images = data['images']
            converted_results = []
            for ann in annotations:
                image_id = int(ann['image_id'])
                cat_id = int(ann['category_id'])
                file = images[image_id]
                file_name = file['file_name']
                index1 = file_name.find('/')
                index1 = index1+1
                index2 = file_name.find('.')
                file_name = file_name[index1:index2]
                width = float(file['width'])
                height = float(file['height'])
                if cat_id <= 81:
                    left, top, bbox_width, bbox_height = map(
                        float, ann['bbox'])

                    # Yolo classes are starting from zero index
                    cat_id -= 1
                    if args.debug:
                        cats[cat_id] += 1
                        total_count += 1
                        if cat_id == 1:
                            bike_images.add(file_name)
                    x_center, y_center = (
                        left + bbox_width / 2, top + bbox_height / 2)
                    # darknet expects relative values wrt image width&height
                    x_rel, y_rel = (x_center / width, y_center / height)
                    w_rel, h_rel = (bbox_width / width, bbox_height / height)
                    converted_results.append(
                        (image_id, file_name, cat_id, x_rel, y_rel, w_rel, h_rel))


    order=[]
    dic=dict()
    for key, *rest in converted_results:
        try:
            dic[key].append(rest)
        except KeyError:
            order.append(key)
            dic[key]=[rest]
    newlist=map(dic.get, order)

    #print(dic[0])
    d_dic = dic.items()

    #new_list = groups.values()

    for obj in d_dic:
        print(obj[1][0][0])
        file_name = obj[1][0][0]
        tbp = []
        for i in range(len(obj[1])):
            temp = obj[1][i][1:]
            tbp.append(temp)
        with open(os.path.join('/Users/edacaner/Desktop/FLIR-new/FLIR_ADAS_1_3/val/txtFiles/', file_name + '.txt'), 'w+') as fp:
            for res in tbp:
                fp.write(str(res[0]) + ' ' + str(res[1])[:8] + ' ' + str(res[2])[:8] + ' ' +  str(res[3])[:8] + ' ' +  str(res[4])[:8] + ' ' + '\n')

