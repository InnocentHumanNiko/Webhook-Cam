from discord import *
from PIL import Image
import aiohttp, asyncio, sys, keyboard, pyautogui, threading, time, pygetwindow, json, pytesseract, ahk, re, win32gui, win32ui, win32con, math, discord

webhook_link = 'https://discord.com/api/webhooks/1312025418802528298/g_B1SZ7kgdcWjdz2eHSY3v4I3EKf54e4JwVQyd9ORvP9WE5YQd5EuyTONOgN-rnWJIwA'
screenshot = sys.path[0] + "\\images\\screenshot.png"
start_pic = sys.path[0] + "\\images\\start.png"
end_pic = sys.path[0] + "\\images\\end.png"
item_pic = sys.path[0] + "\\images\\item.png"
biome_pic = sys.path[0] + "\\images\\biome.png"
result_bg = sys.path[0] + "\\images\\test.png"
enabled = False
started = True
runtime = 0
runtime_hours = 0
total_runtime_hours = 0
runtime_str = ''
total_runtime_str = ''
cooldown = 3
focus_enabled = True
count = 0
ahk = ahk.AHK()
curr_game = ''
curr_game2 = ''
pref_roblox = 0
pref_game = 0
skip = False
lp = ''
sp = ''
pumpkin = ''
status = ''
biome = 'Normal'
hwnd = 0
window_rect = ()

default_settings = {
    "total_runtime": 0,
    "lp": '0',
    "sp": '0',
    "pumpkin": '0'
}

data_path = sys.path[0] + "\\data.json"

for _ in range(2):
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
            break
    except:
        with open(data_path, 'w') as f:
            json.dump(default_settings, f)

def update_data(var = data):
    with open(data_path, 'w') as f:
        json.dump(var, f)

lp = str(data['lp'])
sp = str(data['sp'])
pumpkin = str(data['pumpkin'])

def focus_roblox():
    global focus_enabled
    if focus_enabled:
        try:
            roblox = pygetwindow.getWindowsWithTitle("Roblox")[0]
            for _ in range(10):
                roblox.activate()
        except IndexError:
            print("Roblox window not found.")

def get_xy(name):
    game = pygetwindow.getWindowsWithTitle(name)[0]
    width = game.width
    height = game.height
    left = game.left
    top = game.top
    return width, height, left, top

def start():
    global enabled
    enabled = True
    threading.Thread(target=clock_loop, daemon=True).start()
    print("Started!")

def end():
    global enabled, started, pref_roblox
    enabled = False
    started = False
    pref_roblox = 0
    print("Ended!")

try:
    pref_game = int(input("Roblox | Other Games | Screen [1, 2, 3]\n"))
    if pref_game == 1:
        pref_roblox = int(input("Sol's RNG | Others [1, 2]\n"))
    elif pref_game == 2:
        focus_enabled = False
    elif pref_game == 3:
        curr_game = 'Screen Sharing'
        skip = True
        focus_enabled = False

    if pref_roblox != 1 and skip == False:
        curr_game = input("Enter the name of the game you're playing.\n")
    elif pref_roblox == 1:
        curr_game = "Roblox"
        curr_game2 = "Sol's RNG"
except:
    print("Invalid Input")
    end()

def getHWND(name):
    global hwnd, window_rect
    window_handle = win32gui.FindWindow(None, name)
    window_rect   = win32gui.GetWindowRect(window_handle)
    hwnd = win32gui.FindWindow(None, name)

def background_screenshot(hwnd, path = 'screenshot.png', width = 1920, height = 1080):
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, path)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

def runtime_calc():
    global runtime_str, total_runtime_str
    rt = runtime
    trt = total_runtime
    rh = 0
    trth = 0
    if rt >= 60:
        rh = math.floor(runtime/60)
        rt = rt%60
    if trt >= 60:
        trth = math.floor(trt/60)
        trt = trt%60
    
    runtime_str = f"{rh} hours and {rt} minutes" if rh > 0 else f"{rt} minutes"
    total_runtime_str = f"{trth} hours and {trt} minutes" if trth > 0 else f"{trt} minutes"

total_runtime = data['total_runtime']

sol_stat = f'''- {lp} Lucky Potions
- {sp} Speed Potions
- {pumpkin} Pumpkins
- Current biome: {biome}'''

def biome_dect():
    global biome
    n = 0
    ahk.click(40, 600)
    ahk.click(40, 420)
    ahk.click(900, 435)
    time.sleep(0.2)
    ahk.click(625, 635)
    time.sleep(0.2)
    ahk.click(820, 435)
    time.sleep(0.2)
    ahk.click(625, 635)
    time.sleep(0.5)
    ahk.click(625, 635)
    time.sleep(0.2)
    ahk.send('{F9}')
    time.sleep(0.2)
    ahk.click(40, 420)
    time.sleep(0.5)
    biomes = ['NORMAL', 'RAINY', 'WINDY', 'SNOWY', 'HELL', 'STARFALL', 'SAND STORM', 'CORRUPTION', 'NULL', 'GLITCHED', 'GRAVEYARD', 'PUMPKIN MOON']
    while n < 5:
        pyautogui.screenshot(biome_pic, (870, 1020, 210, 20))
        biome = pytesseract.image_to_string(biome_pic)
        print(biome)
        n += 1
        for i in biomes:
            detected = re.search(i, biome)
            if detected:
                biome = i
                print(i)
                print(biome)
                update_solstat()
                ahk.send('{F9}')
                return
    
    ahk.send('{F9}')
    biome = 'NORMAL'

def result_screen():
    bg = Image.open(result_bg)
    fg1 = Image.open(biome_pic)

    bg.paste(fg1, (50, 50), fg1)

    bg.save("pasted_picture.png")
    return

def macro_loop():
    global count

    mouse_pos = ahk.get_mouse_position()
    old = pygetwindow.getActiveWindowTitle()
    roblox = pygetwindow.getWindowsWithTitle("Roblox")[0]
    for _ in range(10):
        roblox.activate()
    
    count += 1
    print(count)
    if count > 0:
        biome_dect()
    
    if count >= 5:
        macro_test()
        count = 0
    
    old_window = pygetwindow.getWindowsWithTitle(old)[0]
    old_window.activate()
    ahk.mouse_move(mouse_pos[0], mouse_pos[1])

async def update(extra = '', status_w = "Just Vibin'", event = 0):
    global camsession, runtime_str, total_runtime_str, curr_game, curr_game2, skip, status
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_link, session=session)
        if event == 0:
            if skip == True:
                pyautogui.screenshot(screenshot, (0, 0, 1920, 1080))
            else:
                getHWND(curr_game)
                background_screenshot(hwnd, screenshot, window_rect[2], window_rect[3])
                img = Image.open(screenshot)
                img.save(screenshot, optimize = True, quality=95)
            time.sleep(0.2)
            file = File(screenshot, filename="screenshot.png")
        elif event == 1:
            file = File(start_pic, filename="start.png")
        elif event == 2:
            file = File(end_pic, filename="end.png")

        status_w = status if status_w == 'None' else status_w
        runtime_calc()
        try:
            await webhook.edit_message(message_id=1312030999181398077,
                                    content=f'''# Roblox Cam | Update Every {cooldown}s{extra}
Currently playing: {curr_game if curr_game2 == ''or event == 2 else curr_game2}{'\n' + sol_stat if pref_roblox == 1 else ''}
Status: {status_w}
Runtime: {runtime_str}
Total Runtime: {total_runtime_str}''',
                                        attachments=[file]
                                    )
        except discord.errors.HTTPException:
            return

def update_solstat():
    global sol_stat
    sol_stat = f'''- {lp} Lucky Potions
- {sp} Speed Potions
- {pumpkin} Pumpkins
- Current biome: {biome}'''

def macro_test():
    global lp, sp, pumpkin
    
    ahk.click(40, 600)
    time.sleep(0.05)
    ahk.click(40, 540)
    time.sleep(0.1)
    ahk.click(1265, 335)
    time.sleep(0.1)
    test_list = ['luckypotion', 'speedpotion', 'pumpkin'] #, 'windessence', 'rainybottle', 'icicle', 'hourglass', 'eternalflame', 'pieceofstar', 'curruptaine', 'null?']
    amount_list = []
    for i in test_list:
        ahk.click(835, 370)
        ahk.click(1265, 335)
        ahk.click(835, 370)
        time.sleep(0.2)
        ahk.send(i)
        pyautogui.screenshot(item_pic, region=(750, 450, 190, 140))
        amount_list.append(re.findall("[0-9]", pytesseract.image_to_string(item_pic)))
        print(pytesseract.image_to_string(item_pic))

    print(amount_list)
    lp = ''
    sp = ''
    pumpkin = ''
    for idx in range(len(amount_list)):
        if len(amount_list[idx]) < 1:
            amount_list[idx].append('0')
    
    for i in amount_list[0]:
        lp = str(lp) + str(i)
    
    for i in amount_list[1]:
        sp = str(sp) + str(i)
    
    for i in amount_list[2]:
        pumpkin = str(pumpkin) + str(i)
    
    update_solstat()
    data['sp'] = sp if sp != '' else data['sp']
    data['lp'] = lp if lp != '' else data['sp']
    data['pumpkin'] = pumpkin if pumpkin != '' else data['pumpkin']
    update_data()
    ahk.click(40, 420)
    
def clock_loop():
    global runtime, total_runtime
    count = 0
    while enabled:
        time.sleep(60)
        count += 1
        if enabled:
            runtime += 1
            total_runtime += 1
            data['total_runtime'] = total_runtime
            update_data()
            threading.Thread(target=macro_loop, daemon=True).start()

def change_pref():
    global status
    old_status = status
    status = ahk.input_box(prompt="Enter the new status:", title="Changing Preference", width=265, height=125)
    print(status)
    if status == None:
        status = old_status

def merchant_snipe():
    roblox = pygetwindow.getWindowsWithTitle("Roblox")[0]
    for _ in range(10):
        roblox.activate()
    ahk.click(40, 600)
    ahk.click(40, 540)
    ahk.click(1265, 335)
    ahk.click(835, 370)
    ahk.click(1265, 335)
    ahk.click(835, 370)
    ahk.send('merchant')
    ahk.click(835, 430)
    ahk.click(680, 580)
    ahk.click(40, 540)

keyboard.add_hotkey('F1', start)
keyboard.add_hotkey('F2', lambda: threading.Thread(target=end, daemon=True).start())
keyboard.add_hotkey('F3', lambda: threading.Thread(target=change_pref, daemon=True).start())
keyboard.add_hotkey('F4', lambda: threading.Thread(target=merchant_snipe, daemon=True).start())
keyboard.add_hotkey('F6', lambda: threading.Thread(target=result_screen, daemon=True).start())
keyboard.add_hotkey('F7', lambda: threading.Thread(target=biome_dect, daemon=True).start())

curr = round(time.time())
asyncio.run(update(f" | Started <t:{curr}:R>", 'Starting :3', 1))

while started:
    while enabled:
        asyncio.run(update())
        for _ in range(cooldown):
            time.sleep(1)
            if enabled != True:
                break
    time.sleep(0.1)

curr = round(time.time())
curr_game = 'Snoozing...'# input('Ending Status...\n')
if curr_game == (None or ''):
    curr_game = 'Snoozing...'
curr_game2 = curr_game
time.sleep(0.1)
asyncio.run(update(f" | Stopped <t:{curr}:R>", 'Offline', 2))
data['total_runtime'] = total_runtime
update_data()