import os
import json
import cv2
import numpy as np

def create_mask_from_json(json_file, image_path):
    # 读取JSON文件
    with open(json_file) as f:
        data = json.load(f)

    # 读取图像
    image = cv2.imread(image_path)

    # 创建空白掩码图像
    mask = np.zeros_like(image)

    # 遍历每个标注对象
    for shape in data['shapes']:
        # 提取标注的多边形点集
        points = shape['points']
        polygon = np.array(points, dtype=np.int32)

        # 填充多边形区域
        cv2.fillPoly(mask, [polygon], (0, 0, 255))  # 目标物体为红色

    # 将掩码图像转为灰度图像
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    return mask_gray

def generate_masks(image_folder, json_folder, output_folder):
    # 检查输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历图像文件夹中的图像文件
    image_files = os.listdir(image_folder)
    for image_file in image_files:
        # 图像文件路径
        image_path = os.path.join(image_folder, image_file)

        # 对应的JSON文件路径
        json_file = os.path.join(json_folder, os.path.splitext(image_file)[0] + '.json')

        # 生成掩码图
        mask = create_mask_from_json(json_file, image_path)

        # 保存掩码图像
        output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + '_mask.png')
        cv2.imwrite(output_path, mask)

# 图像文件夹、JSON文件夹和输出文件夹路径
output_folder = r'C:\Users\15135\Desktop\ceshi\jiemian_fenge\muti_img_red_mask'
image_folder = r'C:\Users\15135\Desktop\ceshi\jiemian_fenge\image'
json_folder = r'C:\Users\15135\Desktop\ceshi\jiemian_fenge\json'

# 生成掩码图像
generate_masks(image_folder, json_folder, output_folder)
