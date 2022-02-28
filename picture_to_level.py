from PIL import Image
 
name = str(input())
f = open(f"C:/Users/user/Desktop/Yandex_game/data/{name}.txt", 'w')
im = Image.open(f"C:/Users/user/Desktop/Yandex_game/data/{name}.png")
pixels = im.load() # список с пикселями
x, y = im.size # ширина (x) и высота (y) изображения
 
for i in range(x):  
    for j in range(y):
        r, g, b, s = pixels[j, i]
        if r == 107 and g == 190 and b == 62:
            f.write(".")
        elif r == 65 and g == 5 and b == 233:
            f.write("~")
        elif r == 94 and g == 94 and b == 94:
            f.write("@")
        elif r == 198 and g == 198 and b == 198:
            f.write("#")
        elif r == 255 and g == 0 and b == 0:
            f.write("$")
        elif r == 98 and g == 255 and b == 0:
            f.write("e")
    f.write("\n")
im.close
f.close