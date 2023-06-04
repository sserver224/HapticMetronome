from tendo import singleton
import sys
try:
    me = singleton.SingleInstance()
except:
    from tkinter import messagebox
    messagebox.showwarning('Warning','Haptic Metronome is already running')
    sys.exit()
from tkinter import messagebox
from customtkinter import *
import os
from XInput import *
from idlelib.tooltip import Hovertip
from threading import Thread
from tk_tools import *
from pygame import mixer
import time
mixer.init()
channel=mixer.find_channel()
def get_resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
click=mixer.Sound(get_resource_path('click.wav'))
click_accent=mixer.Sound(get_resource_path('click_accent.wav'))
def close():
    try:
        root.destroy()
    except:
        pass
    for i in range(4):
        set_vibration(i, 0, 0)
    messagebox.showinfo('Feedback', 'Please take a moment give feedback on this program in the  Exclusive Access group chat. Thank you!')
    sys.exit()
import struct
set_vibration(0, 0, 0)
def get_tuple(color):
    return (color, color)
def check_status():
    # Print the loudness value
    bpmLabel.set_value(str(bpm.get()))
    if get_connected()[0]:
        if get_battery_information(0)[0]=='DISCONNECTED':
            statusLabel.configure(text='Connected*', text_color=get_tuple('#00ff00'))
        elif get_battery_information(0)[1]=='EMPTY':
            if time.time()%1>0.5:
                statusLabel.configure(text='Battery Critical', text_color=get_tuple('red'))
            else:
                statusLabel.configure(text='Battery Critical', text_color=get_tuple('grey'))
        elif get_battery_information(0)[1]=='LOW':
            statusLabel.configure(text='Battery Low', text_color=get_tuple('orange'))
        else:
            statusLabel.configure(text='Connected', text_color=get_tuple('#00ff00'))
    else:
        statusLabel.configure(text='Not Connected', text_color=get_tuple('grey'))
    if get_connected()[1]:
        if get_battery_information(1)[0]=='DISCONNECTED':
            status1Label.configure(text='Connected*', text_color=get_tuple('#00ff00'))
        elif get_battery_information(1)[1]=='EMPTY':
            if time.time()%1>0.5:
                status1Label.configure(text='Battery Critical', text_color=get_tuple('red'))
            else:
                status1Label.configure(text='Battery Critical', text_color=get_tuple('grey'))
        elif get_battery_information(1)[1]=='LOW':
            status1Label.configure(text='Battery Low', text_color=get_tuple('orange'))
        else:
            status1Label.configure(text='Connected', text_color=get_tuple('#00ff00'))
    else:
        status1Label.configure(text='Not Connected', text_color=get_tuple('grey'))
    if get_connected()[2]:
        if get_battery_information(2)[0]=='DISCONNECTED':
            status2Label.configure(text='Connected*', text_color=get_tuple('#00ff00'))
        elif get_battery_information(2)[1]=='EMPTY':
            if time.time()%1>0.5:
                status2Label.configure(text='Battery Critical', text_color=get_tuple('red'))
            else:
                status2Label.configure(text='Battery Critical', text_color=get_tuple('grey'))
        elif get_battery_information(2)[1]=='LOW':
            status2Label.configure(text='Battery Low', text_color=get_tuple('orange'))
        else:
            status2Label.configure(text='Connected', text_color=get_tuple('#00ff00'))
    else:
        status2Label.configure(text='Not Connected', text_color=get_tuple('grey'))
    if get_connected()[3]:
        if get_battery_information(3)[0]=='DISCONNECTED':
            status3Label.configure(text='Connected*', text_color=get_tuple('#00ff00'))
        elif get_battery_information(3)[1]=='EMPTY':
            if time.time()%1>0.5:
                status3Label.configure(text='Battery Critical', text_color=get_tuple('red'))
            else:
                status3Label.configure(text='Battery Critical', text_color=get_tuple('grey'))
        elif get_battery_information(3)[1]=='LOW':
            status3Label.configure(text='Battery Low', text_color=get_tuple('orange'))
        else:
            status3Label.configure(text='Connected', text_color=get_tuple('#00ff00'))
    else:
        status3Label.configure(text='Not Connected', text_color=get_tuple('grey'))
    root.after(100, check_status)
def _count():
    counter=1
    last_beat=0
    while True:
        if root.running and time.time()-last_beat>=60/int(bpm.get()):
            if counter==1:
                channel.play(click_accent)
                if get_connected()[0]:
                    set_vibration(0, vibSlider.get(), vibSlider.get())
                if get_connected()[1]:
                    set_vibration(1, vibSlider1.get(), vibSlider1.get())
                if get_connected()[2]:
                    set_vibration(2, vibSlider2.get(), vibSlider2.get())
                if get_connected()[3]:
                    set_vibration(3, vibSlider3.get(), vibSlider3.get())
            else:
                channel.play(click)
                if get_connected()[0]:
                    set_vibration(0, vibSlider.get()*0.5, vibSlider.get()*0.5)
                if get_connected()[1]:
                    set_vibration(1, vibSlider1.get()*0.5, vibSlider1.get()*0.5)
                if get_connected()[2]:
                    set_vibration(2, vibSlider2.get()*0.5, vibSlider2.get(*0.5))
                if get_connected()[3]:
                    set_vibration(3, vibSlider3.get()*0.5, vibSlider3.get()*0.5)
            counter+=1
            if counter>int(beatspm.get()):
                counter=1
            last_beat=time.time()
            time.sleep(0.1)
            for i in range(4):
                set_vibration(i, 0, 0)
        elif not root.running:
            counter=1
            for i in range(4):
                set_vibration(i, 0, 0)
            return
        time.sleep(0.01)
def start_stop():
    root.running=not root.running
    if root.running:
        startButton.configure(text='Stop')
        Thread(target=_count, daemon=True).start()
    else:
        startButton.configure(text='Start')
def bpm_0():
    bpm.set(max(min(300, bpm.get()-1), 10))
def bpm_1():
    bpm.set(max(min(300, bpm.get()+1), 10))
def controller_thread():
    Apressed=False
    Apressed1=False
    Apressed2=False
    Apressed3=False
    while True:
        if get_connected()[0]:
            try:
                if get_button_values(get_state(0))['A'] and bool(allow0.get()) and not Apressed:
                    start_stop()
                    Apressed=True
                elif Apressed and not get_button_values(get_state(0))['A']:
                    Apressed=False
                if get_button_values(get_state(0))['DPAD_UP'] and bool(allow0.get()):
                    bpm_1()
                if get_button_values(get_state(0))['DPAD_DOWN'] and bool(allow0.get()):
                    bpm_0()
                if get_button_values(get_state(0))['DPAD_RIGHT']:
                    vibSlider.set(max(min(0.9999, vibSlider.get()+0.01), 0))
                if get_button_values(get_state(0))['DPAD_LEFT']:
                    vibSlider.set(max(min(0.9999, vibSlider.get()-0.01), 0))
            except:
                pass
        if get_connected()[1]:
            try:
                if get_button_values(get_state(1))['A'] and bool(allow1.get()) and not Apressed1:
                    start_stop()
                    Apressed1=True
                elif Apressed1 and not get_button_values(get_state(1))['A']:
                    Apressed1=False
                if get_button_values(get_state(1))['DPAD_UP'] and bool(allow1.get()):
                    bpm_1()
                if get_button_values(get_state(1))['DPAD_DOWN'] and bool(allow1.get()):
                    bpm_0()
                if get_button_values(get_state(1))['DPAD_RIGHT']:
                    vibSlider1.set(max(min(0.9999, vibSlider1.get()+0.01), 0))
                if get_button_values(get_state(1))['DPAD_LEFT']:
                    vibSlider1.set(max(min(0.9999, vibSlider1.get()-0.01), 0))
            except:
                pass
        if get_connected()[2]:
            try:
                if get_button_values(get_state(2))['A'] and bool(allow2.get()) and not Apressed2:
                    start_stop()
                    Apressed2=True
                elif Apressed2 and not get_button_values(get_state(2))['A']:
                    Apressed2=False
                if get_button_values(get_state(2))['DPAD_UP'] and bool(allow2.get()):
                    bpm_1()
                if get_button_values(get_state(2))['DPAD_DOWN'] and bool(allow2.get()):
                    bpm_0()
                if get_button_values(get_state(2))['DPAD_RIGHT']:
                    vibSlider2.set(max(min(0.9999, vibSlider2.get()+0.01), 0))
                if get_button_values(get_state(2))['DPAD_LEFT']:
                    vibSlider2.set(max(min(0.9999, vibSlider2.get()-0.01), 0))
            except:
                pass
        if get_connected()[3]:
            try:
                if get_button_values(get_state(3))['A'] and bool(allow3.get()) and not Apressed3:
                    start_stop()
                    Apressed3=True
                elif Apressed3 and not get_button_values(get_state(3))['A']:
                    Apressed3=False
                if get_button_values(get_state(3))['DPAD_UP'] and bool(allow3.get()):
                    bpm_1()
                if get_button_values(get_state(3))['DPAD_DOWN'] and bool(allow3.get()):
                    bpm_0()
                if get_button_values(get_state(3))['DPAD_RIGHT']:
                    vibSlide3r.set(max(min(0.9999, vibSlider3.get()+0.01), 0))
                if get_button_values(get_state(3))['DPAD_LEFT']:
                    vibSlider3.set(max(min(0.9999, vibSlider3.get()-0.01), 0))
            except:
                pass
        time.sleep(0.01)
def change_vol_0(n):
    if bool(linkIn.get()):
        vibSlider1.set(n)
        vibSlider2.set(n)
        vibSlider3.set(n)
def change_vol_1(n):
    if bool(linkIn.get()):
        vibSlider.set(n)
        vibSlider2.set(n)
        vibSlider3.set(n)
def change_vol_2(n):
    if bool(linkIn.get()):
        vibSlider1.set(n)
        vibSlider.set(n)
        vibSlider3.set(n)
def change_vol_3(n):
    if bool(linkIn.get()):
        vibSlider1.set(n)
        vibSlider2.set(n)
        vibSlider.set(n)
root=CTk()
root.title('Haptic Metronome v0.7 (c) HapticWave Software - Beta')
root.iconbitmap(get_resource_path('metronome.ico'))
LEFT='left'
root.running=False
root.resizable(False, False)
CTkLabel(root, text='Haptic Metronome').pack()
root.protocol('WM_DELETE_WINDOW', close)
frame0=CTkFrame(root)
frame0.pack()
bpm=IntVar()
CTkLabel(frame0, text='BPM').pack()
bpmLabel=SevenSegmentDigits(frame0, digits=3, background='black', digit_color='#00ff00')
bpmLabel.pack()
CTkLabel(frame0, text='with').pack()
beatspm=CTkOptionMenu(frame0, values=tuple(map(str,range(1, 17))))
beatspm.pack()
beatspm.set('4')
CTkLabel(frame0, text='Beats per Measure').pack()
CTkButton(frame0, text='-', command=bpm_0).pack(side=LEFT, padx=5)
bpmEntry=CTkSlider(frame0, from_=10, to=300, variable=bpm)
bpmEntry.pack(side=LEFT)
bpmEntry.set(120)
CTkButton(frame0, text='+', command=bpm_1).pack(side=LEFT, padx=5)
startButton=CTkButton(frame0, text='Start', command=start_stop)
startButton.pack(side=LEFT, padx=5)
linkIn=CTkSwitch(root, text='Link Intensity Sliders')
linkIn.pack()
frame1=CTkFrame(root)
frame1.pack(anchor=NW)
CTkLabel(frame1, text='P1').pack(side=LEFT, padx=5)
allow0=CTkCheckBox(frame1, text='Allow metronome control')
allow0.pack(side=LEFT, padx=5)
vibSlider=CTkSlider(frame1, from_=0, to=0.999999, command=change_vol_0)
vibSlider.pack(side=LEFT, padx=5)
CTkLabel(frame1, text='Status:').pack(side=LEFT, padx=5)
statusLabel=CTkLabel(frame1, text='Not Connected', text_color=('grey','grey'), width=30)
statusLabel.pack(side=LEFT, padx=5)
frame2=CTkFrame(root)
frame2.pack(anchor=NW)
CTkLabel(frame2, text='P2').pack(side=LEFT, padx=5)
allow1=CTkCheckBox(frame2, text='Allow metronome control')
allow1.pack(side=LEFT, padx=5)
vibSlider1=CTkSlider(frame2, from_=0, to=0.999999, command=change_vol_1)
vibSlider1.pack(side=LEFT, padx=5)
CTkLabel(frame2, text='Status:').pack(side=LEFT, padx=5)
status1Label=CTkLabel(frame2, text='Not Connected', text_color=('grey','grey'), width=30)
status1Label.pack(side=LEFT, padx=5)
frame3=CTkFrame(root)
frame3.pack(anchor=NW)
CTkLabel(frame3, text='P3').pack(side=LEFT, padx=5)
allow2=CTkCheckBox(frame3, text='Allow metronome control')
allow2.pack(side=LEFT, padx=5)
vibSlider2=CTkSlider(frame3, from_=0, to=0.999999, command=change_vol_2)
vibSlider2.pack(side=LEFT, padx=5)
CTkLabel(frame3, text='Status:').pack(side=LEFT, padx=5)
status2Label=CTkLabel(frame3, text='Not Connected', text_color=('grey','grey'), width=30)
status2Label.pack(side=LEFT, padx=5)
frame4=CTkFrame(root)
frame4.pack(anchor=NW)
CTkLabel(frame4, text='P4').pack(side=LEFT, padx=5)
allow3=CTkCheckBox(frame4, text='Allow metronome control')
allow3.pack(side=LEFT, padx=5)
vibSlider3=CTkSlider(frame4, from_=0, to=0.999999, command=change_vol_3)
vibSlider3.pack(side=LEFT, padx=5)
CTkLabel(frame4, text='Status:').pack(side=LEFT, padx=5)
status3Label=CTkLabel(frame4, text='Not Connected', text_color=('grey','grey'), width=30)
status3Label.pack(side=LEFT, padx=5)
check_status()
vibSlider.set(0)
vibSlider1.set(0)
vibSlider2.set(0)
vibSlider3.set(0)
Thread(target=controller_thread, daemon=True).start()
root.mainloop()
