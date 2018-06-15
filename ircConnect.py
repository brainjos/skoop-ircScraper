import socket
import time

class IRC:
    def __init__(self, server, channel, botnick):
        self.server = server
        self.channel = channel
        self.botnick = botnick
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.ircsock.connect((self.server, 6668))
        self.ircsock.send(bytes("NICK " + self.botnick + "\r\n", "UTF-8"))
        self.ircsock.send(bytes("USER " + self.botnick + " " + self.botnick + " " + self.botnick + " :" + 
            self.botnick + "\r\n", "UTF-8"))
        time.sleep(2) #to deal with bot not joining channel properly
        self.ircsock.send(bytes("JOIN " + self.channel + "\n", "UTF-8"))
        ircmsg = ""
        while ircmsg.find("End of /NAMES list.") == -1: 
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            ircmsg = ircmsg.strip('\n\r')
            print(ircmsg)
        print("Done connecting to server!\n")

    def rec_message(self):
        ircmsg = self.ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if ircmsg.find("PRIVMSG") != -1: #diagnosis: message to channel
            name = ircmsg.split('!', 1)[0][1:] #extract name from message data
            message = ircmsg.split('PRIVMSG', 1)[1].split(':', 1)[1] #extract message text from message data
            return name, message
        if ircmsg.find("PING :") != 1: #add ping functionality so bot does not disconnect from server
            self.ircsock.send(bytes("PONG :pingis\n", "UTF-8"))
            return self.rec_message() #wait for next non-ping incoming message

    def send_message(self, message, target=None):
        if target is None:
            target = self.channel
        self.ircsock.send(bytes("PRIVMSG " + target + " :" + message + "\n", "UTF-8"))
