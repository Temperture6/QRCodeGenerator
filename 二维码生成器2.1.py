import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter.font as tkfont
from tkinter import ttk
import os, re
from MyQR import myqr
# from PIL import Image
from tkinter import messagebox
import qrcode
from PIL import Image

print("请不要关闭此窗口")
win = tk.Tk()
width = 300
height = 330
screenwidth = win.winfo_screenwidth()
screenheight = win.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
win.geometry(alignstr)
win.resizable(width=False, height=False)
win.title("二维码生成器")

# 全局变量
desk_path = os.path.join(os.path.expanduser('~'), "Desktop")


# 主要函数
def logo_make(text, icon_path, save_path):
    qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=1)
    qr.add_data(text)  # 要生成二维码的内容
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGBA")

    icon = Image.open(icon_path)  # logo图片要具体到文件夹和图片名称

    img_w, img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h), icon)

    img.save(save_path)

    return


def qrcode_make():
    """获取参数"""

    # 文本内容
    text = text_input.get()
    if text == '':
        tk.messagebox.showerror('错误', '没有输入文本')
        return

    # 图片路径
    if pic_com.get() == '全背景图(1:1)':
        pic_dir = pic_dir_fun()
        if pic_dir == '':
            tk.messagebox.showerror('错误', '没有选择ICO文件')
            return
    elif pic_com.get() == '中间小logo':
        # 处理输入以及报错处理———logo
        icon_path = logo_dir_fun()
        if not icon_path:
            tk.messagebox.showerror('错误', '没有选择图片文件')
            return

        save_path = pic_save()
        ext = os.path.splitext(icon_path)
        if ext[-1] not in ['.png', '.jpg']:
            tk.messagebox.showerror('错误', '不支持的图片格式，仅支持 *.jpg ， *.png')
            return
        save_name = save_path + '.png'
        try:
            logo_make(text, icon_path, save_name)
        except ValueError:
            tk.messagebox.showerror('错误', '没有选择保存路径及名称')
            return
        fin_tip = '图片已生成，图片位置：桌面' + \
                  '\n\n' + save_name + '\n\n\n' + '是否打开图片？'

        res = tk.messagebox.askyesno('二维码生成器', fin_tip)
        if res:
            if os.path.exists(save_name):
                os.system('start ' + save_name)
            else:
                tk.messagebox.showerror('错误', '没有找到文件')
        else:
            return
        # logo 完
        return
    else:
        pic_dir = None

    # 纠错等级
    my_level = None
    if level_com.get() == '高':
        my_level = 'H'
    elif level_com.get() == '较高':
        my_level = 'Q'
    elif level_com.get() == '中等':
        my_level = 'M'
    elif level_com.get() == '低':
        my_level = 'L'

    # 颜色
    if color_com.get() == '彩色':
        color = True
    else:
        color = False

    # 对比度
    cont = float(contrast_com.get())

    # 亮度
    brint = float(brintness_com.get())

    # 保存路径

    s_dir = pic_save()
    if s_dir == '':
        tk.messagebox.showerror('警告', '没有选择保存路径')
        return

    save = s_dir[0:s_dir.rfind('/')]
    name = s_dir[s_dir.rfind('/'):len(s_dir)]
    str_list = list(name)
    del str_list[0]

    if pic_dir is not None:
        if pic_dir[pic_dir.rfind('.'):len(pic_dir)] == '.gif':
            name = ''.join(str_list) + '.gif'
        else:
            name = ''.join(str_list) + '.png'
    # 边长
    if version_com.get() == '自动(根据字符长度)':
        win.withdraw()
        print('请耐心等待...')
        if not '.gif' in name:
            if not '.png' in name:
                name = name + '.png'
        name = name.replace('/', '')
        print(name)
        myqr.run(
            words=text,
            level=my_level,
            picture=pic_dir,
            contrast=cont,
            brightness=brint,
            colorized=color,
            save_dir=save,
            save_name=name)
        win.deiconify()
        tk.messagebox.showinfo('完成', '二维码生成完成')
    else:
        win.withdraw()
        print('请耐心等待...')
        if not '.gif' in name:
            if not '.png' in name:
                name = name + '.png'
        name = name.replace('/', '')
        print(name)
        version = int(version_com.get())
        myqr.run(
            words=text,
            version=version,
            level=my_level,
            contrast=cont,
            brightness=brint,
            picture=pic_dir,
            colorized=color,
            save_dir=save,
            save_name=name)
        win.deiconify()
        tk.messagebox.showinfo('完成', '二维码生成完成')

    return


def pic_save():
    save_dir = filedialog.asksaveasfilename(title='保存位置以及图片名称',
                                            initialdir=desk_path)
    return save_dir


def pic_dir_fun():
    pic_dir = filedialog.askopenfilename(title='选择图片文件',
                                         filetypes=[('图片', '*.jpg'),
                                                    ('图片', '*.png'),
                                                    ('图片', '*.gif')],
                                         initialdir=desk_path)
    return pic_dir


def logo_dir_fun():
    pic_dir = filedialog.askopenfilename(title='选择图片文件',
                                         filetypes=[('图片', '*.jpg'),
                                                    ('图片', '*.png')],
                                         initialdir=desk_path)
    return pic_dir


def close():
    res = tk.messagebox.askokcancel('退出', '您确定要退出吗？')
    if not res:
        return
    else:
        win.destroy()
        os._exit(1)


def tip():
    tips = tk.Tk()
    tips.geometry('580x200')
    tips.resizable(0, 0)
    tips.title('小提示')

    tk.Label(tips,
             text='1、我也不知道‘亮度’和‘对比度’是个什么玩意').place(x=10, y=10)
    tk.Label(tips,
             text='2、本程序采用‘先设置保存路径后生成’的方式生成二维码，设置好保存路径后才开始生成二维码').place(x=10, y=30)
    tk.Label(tips,
             text='3、程序使用单核单线程处理，二维码生成过程中窗口无响应属于正常现象').place(x=10, y=50)
    tk.Label(tips,
             text='4、具体无响应时间取决于生成二维码的难度，与图片、纠错等级、边长有关').place(x=10, y=70)
    tk.Label(tips,
             text='5、纠错等级是指容错率的大小，越高，容错率越大，生成所需时间越长').place(x=10, y=90)
    tk.Label(tips,
             text='6、边长越大，生成的二维码图像大小越大，生成所需时间越长').place(x=10, y=110)
    tk.Label(tips,
             text='7、gif图片作为背景时，所需生成时间较长，jpg或png图片作为背景时所需时间相对较少').place(x=10, y=130)

    tk.Button(tips,
              text='我知道了',
              command=tips.destroy).place(x=500, y=165)
    tips.mainloop()
    return


def delete():
    text_input.delete(0, 'end')
    return


def tips(self):
    if pic_com.get() == '中间小logo':
        tk.messagebox.showinfo('提醒', '此模式下支持中文输入\n不支持纠错等级、颜色、对比度、亮度、边长的调整')
    return


# 定义字体模板
ft = tkfont.Font(size=15, weight=tkfont.BOLD)

tk.Label(win,
         text='输入文本或网址(不支持中文)：',
         font=ft,
         fg='YellowGreen').place(x=6, y=5)
my_text = tk.StringVar()
text_input = tk.Entry(win,
                      textvariable=my_text,
                      width=30,
                      highlightcolor='Red',
                      highlightthickness=1)
text_input.place(x=15, y=40)
text_input.focus()

tk.Button(win,
          text='删除',
          fg='Red',
          command=delete).place(x=260, y=36)

# 是否有图片
tk.Label(win, text='图   片:', font=ft, fg='Orange').place(x=10, y=70)
xVariable1 = tk.StringVar()
pic_com = ttk.Combobox(win, textvariable=xVariable1)
pic_com["value"] = ("(无)", "全背景图(1:1)", "中间小logo")
pic_com.current(0)
pic_com.bind("<<ComboboxSelected>>", tips)
pic_com.place(x=112, y=70)

# 纠错等级
tk.Label(win, text='纠错等级:', font=ft, fg='YellowGreen').place(x=10, y=100)
xVariable2 = tk.StringVar()
level_com = ttk.Combobox(win, textvariable=xVariable2)
level_com["value"] = ("高", "较高", "中等", "低")
level_com.current(0)
level_com.bind("<<ComboboxSelected>>")
level_com.place(x=112, y=100)

# 颜色
tk.Label(win, text='颜   色：', font=ft, fg='Blue').place(x=10, y=130)
xVariable3 = tk.StringVar()
color_com = ttk.Combobox(win, textvariable=xVariable3)
color_com["value"] = ("彩色", "黑白")
color_com.current(0)
color_com.bind("<<ComboboxSelected>>")
color_com.place(x=112, y=130)

# 对比度
tk.Label(win, text='对 比 度：', font=ft, fg='Red').place(x=10, y=160)
xVariable4 = tk.StringVar()
contrast_com = ttk.Combobox(win, textvariable=xVariable4)
value_list = []
for i in range(0, 20):
    i += 1
    value_list.append(i / 10)
contrast_com["value"] = value_list
contrast_com.current(9)
contrast_com.bind("<<ComboboxSelected>>")
contrast_com.place(x=112, y=160)

# 亮度
tk.Label(win, text='亮   度：', font=ft, fg='Black').place(x=10, y=190)
xVariable5 = tk.StringVar()
brintness_com = ttk.Combobox(win, textvariable=xVariable5)
value_list = []
for i in range(0, 20):
    i += 1
    value_list.append(i / 10)
brintness_com["value"] = value_list
brintness_com.current(9)
brintness_com.bind("<<ComboboxSelected>>")
brintness_com.place(x=112, y=190)

# 边长
tk.Label(win, text='边   长：', font=ft, fg='Violet').place(x=10, y=220)
xVariable6 = tk.StringVar()
version_com = ttk.Combobox(win, textvariable=xVariable6)
version_list = ['自动(根据字符长度)']
for i in range(0, 40):
    i += 1
    version_list.append(i)
version_com["value"] = version_list
version_com.current(0)
version_com.bind("<<ComboboxSelected>>")
version_com.place(x=112, y=220)

# 按钮
tk.Button(win,
          text='生成二维码',
          width=10,
          bg='LightCyan',
          fg='Red',
          command=qrcode_make).place(x=120, y=285)

tk.Button(win,
          text='退出',
          width=10,
          bg='Silver',
          command=close).place(x=10, y=285)

tk.Button(win,
          text='...',
          command=tip).place(x=275, y=285)
win.protocol('WM_DELETE_WINDOW', close)

win.mainloop()
