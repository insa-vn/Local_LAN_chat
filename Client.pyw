import thread
import socket
from Functions import *


# ---------------------------------------------------#
# ---------INITIALIZE CONNECTION VARIABLES-----------#
# ---------------------------------------------------#


WindowTitle = 'Client'
HOST = 'localhost'
PORT = 5000
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# ---------------------------------------------------#
# ------------------ MOUSE EVENTS -------------------#
# ---------------------------------------------------#


def send_msg():
    # Write message to chat window
    message = filter_msg(EntryBox.get("0.0", END))
    LoadMyEntry(ChatLog, message)

    # Scroll to the bottom of chat windows
    ChatLog.yview(END)

    # Erase previous message in Entry Box
    EntryBox.delete("0.0", END)

    socket_client.sendall(message)

# ---------------------------------------------------#
# ----------------- KEYBOARD EVENTS -----------------#
# ---------------------------------------------------#


def PressAction(event):
    EntryBox.config(state=NORMAL)
    send_msg()


def DisableEntry(event):
    EntryBox.config(state=DISABLED)


# ---------------------------------------------------#
# -----------------GRAPHICS MANAGEMENT---------------#
# ---------------------------------------------------#

# Create a window
base = Tk()
base.title(WindowTitle)
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

# Create a Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.insert(END, "Connecting to your partner..\n")
ChatLog.config(state=DISABLED)

# Bind a scrollbar to the Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

# Create the Button to send message
SendButton = Button(base, font=30, text="Send", width="12", height=5,
                    bd=0, bg="#FFBF00", activebackground="#FACC2E",
                    command=send_msg)

# Create the box to enter message
EntryBox = Text(base, bd=0, bg="white", width="29", height="5", font="Arial")
EntryBox.bind("<Return>", DisableEntry)
EntryBox.bind("<KeyRelease-Return>", PressAction)

# Place all components on the screen
scrollbar.place(x=376, y=6, height=386)
ChatLog.place(x=6, y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)


# ---------------------------------------------------#
# ----------------CONNECTION MANAGEMENT--------------#
# ---------------------------------------------------#

def ReceiveData():
    try:
        socket_client.connect((HOST, PORT))
        LoadConnectionInfo(ChatLog, '[ Successfully connected ]\-------------------------------------------------------')
    except:
        LoadConnectionInfo(ChatLog, '[ Unable to connect ]')
        return

    while 1:
        try:
            data = socket_client.recv(1024)
        except:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break
        if data != '':
            LoadOtherEntry(ChatLog, data)

        else:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break
    # socket_client.close()

thread.start_new_thread(ReceiveData, ())

base.mainloop()


