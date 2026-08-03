import win32ui,os,base64
from PIL import Image,ImageGrab
​
im = ImageGrab.grabclipboard()
if isinstance(im, Image.Image):
 img = im
else:
 dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
 dlg.SetOFNInitialDir('C:\\Pictures')  # 设置打开文件对话框中的初始显示目录
 dlg.DoModal()
 filename = dlg.GetPathName()  # 获取选择的文件名称
 img = Image.open(filename)
​
img.thumbnail((778,439),Image.ANTIALIAS)
img=img.convert('RGB')
img.save("D:\\PythonCode\\base64pic\\1.jpg", quality=70)
​
with open("D:\\PythonCode\\base64pic\\1.jpg", 'rb') as f:
 base64_data = base64.b64encode(f.read())
 s = base64_data.decode()
 print('![](data:image/jpeg;base64,%s)'%s)

os.remove("D:\\PythonCode\\base64pic\\1.jpg")