import os
import argparse
from datetime import datetime
from PIL import Image


def make_square_image(input_path, output_path, output_format='png'):
    """
    ## 将图片放入正方形画布并保存。

    - 如果 output_format 为 'jpg' 或 'jpeg'，会使用白色背景并以 JPEG 保存。
    - 否则使用透明背景并以 PNG 保存。
    """
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    size = max(w, h)

    # PNG：RGBA（透明）；JPEG：先在 RGBA 白底上合成，再转换成 RGB 保存
    if output_format in ("jpg", "jpeg"):
        canvas = Image.new("RGBA", (size, size), (255, 255, 255, 255))
        offset = ((size - w) // 2, (size - h) // 2)
        canvas.paste(img, offset, img)
        rgb = canvas.convert("RGB")
        rgb.save(output_path, format="JPEG", quality=95)
    else:
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        offset = ((size - w) // 2, (size - h) // 2)
        canvas.paste(img, offset, img)
        canvas.save(output_path, format="PNG")


def main():
    parser = argparse.ArgumentParser(description="把图片放入正方形画布并输出 png 或 jpg（可选透明/白底）")
    # 注意：输出行为由输入文件类型决定（覆盖原有 --format 行为）
    # 保留 argparse 用于显示帮助信息；实际输出格式由输入文件扩展名决定
    _ = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    input_dir = "in"
    out_jpg_dir = f"out_jpg_{timestamp}"
    out_png_dir = f"out_png_{timestamp}"

    # 检查 in 文件夹
    os.makedirs(input_dir, exist_ok=True)

    # 查找支持的输入文件
    exts = (".png", ".jpg", ".jpeg")
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(exts)]
    if not files:
        print(f"No matching files found in '{input_dir}'. Please add images with extensions: {exts} and re-run.")
        return

    # 处理所有文件
    for file in files:
        input_path = os.path.join(input_dir, file)
        filename_no_ext, input_ext = os.path.splitext(file)
        input_ext = input_ext.lower()

        if input_ext in (".jpg", ".jpeg"):
            os.makedirs(out_jpg_dir, exist_ok=True)
            output_path = os.path.join(out_jpg_dir, f"{filename_no_ext}.jpg")
            print(f"Processing (jpg input): {file} -> {output_path}")
            make_square_image(input_path, output_path, output_format='jpg')

        elif input_ext == ".png":
            # 对 png 输入：在 out_jpg_dir 下生成 jpg（1 份），在 out_png_dir 下生成 png（1 份）
            os.makedirs(out_jpg_dir, exist_ok=True)
            os.makedirs(out_png_dir, exist_ok=True)

            # 生成 jpg 放到 out_jpg_dir（白底）
            out_jpg_path = os.path.join(out_jpg_dir, f"{filename_no_ext}.jpg")
            print(f"Processing (png input -> jpg): {file} -> {out_jpg_path}")
            make_square_image(input_path, out_jpg_path, output_format='jpg')

            # 生成 png 放到 out_png_dir（透明）
            out_png_path = os.path.join(out_png_dir, f"{filename_no_ext}.png")
            print(f"Processing (png input -> png): {file} -> {out_png_path}")
            make_square_image(input_path, out_png_path, output_format='png')

        else:
            print(f"Skipping unsupported file: {file}")

    print("All images processed!")


if __name__ == "__main__":
    main()
