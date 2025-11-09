import os
from PIL import Image

def make_square_image(input_path, output_path, fill_color=(0, 0, 0, 0)):
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    size = max(w, h)

    # 创建正方形画布
    new_img = Image.new("RGBA", (size, size), fill_color)

    # 计算居中位置
    offset = ((size - w) // 2, (size - h) // 2)

    # 贴图
    new_img.paste(img, offset, img)
    new_img.save(output_path)


# 设置输入输出目录
input_dir = "in"
output_dir = "out"
os.makedirs(output_dir, exist_ok=True)

# 支持的格式
exts = (".png", ".jpg", ".jpeg")

# 处理所有文件
for file in os.listdir(input_dir):
    if file.lower().endswith(exts):
        input_path = os.path.join(input_dir, file)

        # 输出统一为 PNG（支持透明）
        filename_no_ext = os.path.splitext(file)[0]
        output_path = os.path.join(output_dir, filename_no_ext + ".png")

        print(f"Processing: {file} -> {output_path}")
        make_square_image(input_path, output_path, fill_color=(0, 0, 0, 0)) # 透明背景

print("All images processed!")
