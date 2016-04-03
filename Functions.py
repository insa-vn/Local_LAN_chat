from Tkinter import *


def filter_msg(msg):
    end_msg = ''
    for i in range(len(msg)-1, -1, -1):
        if msg[i] != '\n':
            end_msg = msg[0:i+1]
            break
    for i in range(0, len(end_msg), 1):
            if end_msg[i] != "\n":
                    return end_msg[i:]+'\n'
    return ''


def LoadConnectionInfo(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') is not None:
            ChatLog.insert(END, EntryText)
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)


def LoadMyEntry(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            LineNumber = float(ChatLog.index('end'))-1.0
            ChatLog.insert(END, "You: " + EntryText)
            ChatLog.tag_add("You", LineNumber, LineNumber+0.4)
            ChatLog.tag_config("You", foreground="#FF8000", font=("Arial", 12, "bold"))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)


def LoadOtherEntry(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            try:
                LineNumber = float(ChatLog.index('end'))-1.0
            except:
                pass
            ChatLog.insert(END, "Other: " + EntryText)
            ChatLog.tag_add("Other", LineNumber, LineNumber+0.6)
            ChatLog.tag_config("Other", foreground="#04B404", font=("Arial", 12, "bold"))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)


def display_msg(msg_window, msg):
    if msg != '':
        msg_window.config(state=NORMAL)
        LineNumber = float(msg_window.index('end'))-1.0
        if msg_window.index('end') is not None:
            msg_window.insert(END, msg)
            msg_window.config(state=DISABLED)
            msg_window.yview(END)
