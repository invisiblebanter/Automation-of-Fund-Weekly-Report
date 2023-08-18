from PIL import Image

def merge_images_horizontally(image_path1, image_path2):
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    # 获取两个图像的宽度和高度
    width1, height1 = image1.size
    width2, height2 = image2.size

    # 确保两个图像高度相同，其提示
    if height1 != height2:
        raise ValueError("两个图像的高度不一致，需重新生成")
    # 计算合并后的图像宽度
    merged_width = width1 + width2
    # 创建一个新的空白图像，大小为合并后的宽度和高度
    merged_image = Image.new('RGB', (merged_width, height1))

    # 将两个图像粘贴到合并图像上
    merged_image.paste(image1, (0, 0))
    merged_image.paste(image2, (width1, 0))
    output_path = r'../png_file/合并.png'
    # 保存合并后的图像
    merged_image.save(output_path)
    # 关闭被合并的图片
    image1.close()
    image2.close()

