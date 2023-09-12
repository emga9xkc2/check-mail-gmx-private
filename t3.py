from PIL import Image


class himagesearch:
    def __init__(self, image: Image):
        self.image = image
        pass
    def findMultiColorInRegionFuzzy(self, color, color_positions, degree, x1, y1, x2, y2):
        degree = 100 - degree
        # Load the image
        # image = Image.open(r"C:\Users\Admin\Pictures\Screenshots\Capture.PNG")
        image = self.image
        # Convert the color to RGB
        r = (color & 0xFF0000) >> 16
        g = (color & 0x00FF00) >> 8
        b = (color & 0x0000FF)
        color_rgb = (r, g, b)
        color_positions = color_positions.split(",")
        # Loop through the region of the image
        for y in range(y1, y2):
            for x in range(x1, x2):
                # Get the color at the current position
                current_color = image.getpixel((x, y))
                if len(current_color) == 4:  # PNG image
                    current_color = current_color[:3]  # Ignore the alpha channel
                # Check if the current color matches the reference color
                if current_color == color_rgb:

                    # Check if the colors around the current position match
                    lis = []
                    lis2 = []
                    for pos in color_positions:
                        dx, dy, ref_color = pos.split("|")
                        dx = int(dx)
                        dy = int(dy)
                        r = (int(ref_color, 16) & 0xFF0000) >> 16
                        g = (int(ref_color, 16) & 0x00FF00) >> 8
                        b = (int(ref_color, 16) & 0x0000FF)
                        ref_color_rgb = (r, g, b)
                        newx = x + dx
                        newy = y + dy
                        # Get the color at the position around the current position
                        if newx <= 0 or newy <= 0:
                            lis.append("False")
                            break
                        around_color = image.getpixel((newx, newy))

                        # Check if the color around the current position matches the reference color with the specified degree of fuzziness
                        if (around_color[0] >= ref_color_rgb[0] - degree and around_color[0] <= ref_color_rgb[0] + degree
                                and around_color[1] >= ref_color_rgb[1] - degree and around_color[1] <= ref_color_rgb[1] + degree
                                and around_color[2] >= ref_color_rgb[2] - degree and around_color[2] <= ref_color_rgb[2] + degree):
                            # hex_color_code = '0x{:02X}{:02X}{:02X}'.format(around_color[0],around_color[1],around_color[2])
                            # lis2.append((newx, newy, hex_color_code))
                            lis.append("True")
                        else:
                            lis.append("False")
                            break
                    if "False" in lis:
                        continue
                    # print(lis2)
                    return x, y

        return (0,0)

from hwin import *
exe = r"C:\Program Files\Privax\HMA VPN\VyprVPN.exe"
if not hfile.checkExists(exe):
    exe = r"C:\Program Files (x86)\HMA VPN\VyprVPN.exe"
nameexe = hfile.getFilenameWithoutExtension(exe)
hwnd = None
pids = hwin.getPidsOfProcess(nameexe)

for pid in pids:
    if hwnd:
        break
    hwnds = hwin.getHandlesByPid(pid)
    size = None
    if len(hwnds) == 1:
        hwnd = hwnds[0]
    else:
        for i in hwnds:
            isize = hwin.getClientSizeByHandle(i)
            if isize[1] == 570:
                hwnd = i
                size = isize
                break
image = hwin.captureHandle(hwnd)
image.save(r"C:\Users\Admin\Pictures\Screenshots\abc.png")
hi = himagesearch(image)
# x,y = findMultiColorInRegionFuzzy( 0x472814, "-335|-221|0xefa037,-435|-465|0xfff3c3,10|-473|0xfae474,238|-449|0xfceb5f,39|-216|0xcb6b04,-310|-64|0x7f6669,-491|10|0x663a2d,-136|65|0x553c38,-344|-256|0xfbaa27", 90, 0, 0, 1023, 575)
findMultiColorInRegionFuzzy = hi.findMultiColorInRegionFuzzy
x,y = findMultiColorInRegionFuzzy( 0x6f767c, "6|7|0x6f767c,-12|-79|0x12a1fc,-194|-74|0x0978fb,-150|-374|0xc1c1c1,-132|-436|0xd6d6d6", 90, 0, 0, 375, 606)

print(x,y)
