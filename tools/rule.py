import os

def resize():
    path = input("请输入路径(例如D:\\\\picture)：")
    scaling = float(input("请输入缩放比例:"))
    count = 0
    file_list = os.listdir(path)
    for files in file_list:
        img_dir = os.path.join(path, files)
        img = Image.open(img_dir)
        img_size = img.size
        print("图片宽度和高度分别是{}".format(img_size))
        # if img_size[0] > 2000:
        #     scaling = 0.25
        # elif img_size[0] > 1000:
        #     scaling = 0.5
        # else:
        #     scaling = 1
        img = img.resize((int(img_size[0]*scaling), int(img_size[1]*scaling)))
        img.save(img_dir)
        count += 1
    print("一共修改了"+str(count)+"个文件")

def rename():
    path = input("请输入路径(例如D:\\\\picture)：")
    name = input("请输入开头名:")
    start_number = input("请输入开始数:")
    file_type = input("请输入后缀名（如 .jpg、.txt等等）:")
    print("正在生成以" + name + start_number + file_type + "迭代的文件名")
    count = 0
    file_list = os.listdir(path)
    for files in file_list:
        old_dir = os.path.join(path, files)
        new_dir = os.path.join(path, name + str(count + int(start_number)) + file_type)
        os.rename(old_dir, new_dir)
        count += 1
    print("一共修改了" + str(count) + "个文件")


rename()