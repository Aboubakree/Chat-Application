import socket 
import threading
import rsa
import tkinter
import tkinter.scrolledtext

#------------------- functions ------------------------ 
"""
def sending_messages(client):
    while True :
        message = input("")
        print("You : " + message)
        message = f"{name} : " + message
        client.send(rsa.encrypt(message.encode(), public_partner))
"""     

def receiving_messages(client):
    while True:
        message = rsa.decrypt(client.recv(1024), private_key).decode()
        textarea.config(state='normal')
        textarea.insert('end', message)
        #textarea.yview('end')
        textarea.config(state='disabled')
        print(message)

def get_input():
    global client
    message = f"{inputbox.get('1.0','end')}"
    textarea.config(state='normal')
    textarea.insert('end',"You :"+message)
    textarea.config(state='disabled')
    print("You : " + message)
    message = f"{name} :" + message
    client.send(rsa.encrypt(message.encode(), public_partner))
    inputbox.delete('1.0','end')

#-------------------- connecting with client -------------------
public_key, private_key = rsa.newkeys(1024)
public_partner = None

name = input("Enter Your name : ")
print("Your Are the Host !")
print("\t\t\t----------------------------------\n")


server = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
server.bind(("127.0.0.1",7777))
server.listen()

client, addr = server.accept()
print(f"{addr} has join the chat !")

client.send(public_key.save_pkcs1("PEM"))
public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

#------------------------- GUI -----------------------

win = tkinter.Tk()
win.config(bg="lightgray")

chat_label = tkinter.Label(win,text="Chat : ",bg="lightgray")
chat_label.config(font=("Arial",12))
chat_label.pack(padx=20,pady=5)

textarea = tkinter.scrolledtext.ScrolledText(win)
textarea.pack(padx=20,pady=5)
textarea.config(state='disabled')

msglabel = tkinter.Label(win,text="Message:",bg="lightgray")
msglabel.config(font=("Arial",12))
msglabel.pack(padx=20,pady=5)

inputbox = tkinter.Text(win,height=3)
inputbox.pack(padx=20,pady=5)

sendbutton = tkinter.Button(win,text="Send",command=get_input)
sendbutton.config(font=("Arial",12))
sendbutton.pack(padx=20,pady=5)

threading.Thread(target = receiving_messages ,args=(client,)).start()
#threading.Thread(target = sending_messages ,args=(client,)).start()
        
win.mainloop()





