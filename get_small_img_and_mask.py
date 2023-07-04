# 根据labelme标注的json文件和原图，得到单个物体的小图和对应大小小图的mask图

import os
import json
import cv2
import numpy as np

# 设置图像文件夹路径和JSON文件夹路径
image_folder_path = r'C:\Users\15135\Desktop\ceshi\jiemian_fenge\image'
json_folder_path = r'C:\Users\15135\Desktop\ceshi\jiemian_fenge\json'
output_image_folder_path = r'C:\Users\15135\Desktop\ceshi\jiemian_fenge\output_image'

# 遍历JSON文件夹下的所有文件
for filename in os.listdir(json_folder_path):
    if filename.endswith(".json"):
        # 解析JSON文件
        json_path = os.path.join(json_folder_path, filename)
        with open(json_path, "r") as file:
            data = json.load(file)

        # 获取图像文件名
        image_filename = data["imagePath"]
        image_path = os.path.join(image_folder_path, image_filename)

        # 读取原图像
        image = cv2.imread(image_path)

        # 获取输出文件夹路径
        output_image_subfolder_path = os.path.join(output_image_folder_path, os.path.splitext(image_filename)[0])

        # 创建输出文件夹（如果不存在）
        os.makedirs(output_image_subfolder_path, exist_ok=True)

        # 记录每个类别的物体数量
        object_counts = {}

        # 遍历每个目标物体
        for shape in data["shapes"]:
            label = shape["label"]

            # 获取当前类别的物体数量
            if label in object_counts:
                object_counts[label] += 1
            else:
                object_counts[label] = 1

            # 计算外接矩形框
            points = shape["points"]
            points = np.array(points, dtype=np.int32)
            x_min, y_min = np.min(points, axis=0)
            x_max, y_max = np.max(points, axis=0)

            # 扩展外接矩形框
            x_min -= 10  # 向左扩展10个像素
            y_min -= 10  # 向上扩展10个像素
            x_max += 10  # 向右扩展10个像素
            y_max += 10  # 向下扩展10个像素

            # 确保外接矩形框不超出原图像边界
            x_min = max(x_min, 0)
            y_min = max(y_min, 0)
            x_max = min(x_max, image.shape[1])
            y_max = min(y_max, image.shape[0])

            # 截取目标物体区域
            object_image = image[y_min:y_max, x_min:x_max]

            # 检查截取图像是否为空
            if object_image.size == 0:
                continue

            # 创建全黑的 mask 图像
            mask = np.zeros_like(object_image)

            # 在 mask 图像上绘制物体区域
            cv2.fillPoly(mask, [points - np.array([x_min, y_min])], (255, 255, 255))

            # 生成物体文件名（使用类别和物体索引）
            object_index = object_counts[label]
            object_image_filename = f"{label}_{object_index}.png"

            # 保存截取的图像
            object_image_path = os.path.join(output_image_subfolder_path, object_image_filename)
            cv2.imwrite(object_image_path, object_image)

            # 生成物体的 mask 图像文件名
            mask_filename = f"{label}_{object_index}_mask.png"

            # 构建物体的 mask 图像完整路径
            mask_path = os.path.join(output_image_subfolder_path, mask_filename)

            # 保存物体的 mask 图像
            cv2.imwrite(mask_path, mask)
