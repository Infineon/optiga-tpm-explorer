import wx
import shell_util as exec_cmd
import multiprocessing
import time
import os
import subprocess
from subprocess import call
import images as img
import time
# from wx.lib.pubsub import setuparg1
# from wx.lib.pubsub import pub as Publisher
from pubsub import pub as Publisher
import threading
from threading import Thread
import signal
import ctypes

"""
Already done: The creation of the server and CA keypairs, CA self-signed certificate. RSA miscellaneous functions and hashing are okay already.

TO-DO: Get the start_client/start_server and write_client/write_server functions to work. The aim of the two tabs are to:
Display a client and server process that connect to each other using the TPM commands.
Additionally show connectivity by sending messages from client/server and showing that the message appears in the server/client.

Running subprocess does not block the UI, however, sending messages through the PIPE in subprocess does block the UI.
The main issue here is the many methods of sending messages to the client/server processes are blocking (the UI).
"""
# index 0, 1 respectively
rng_type_list = ['hex', 'base64']
server_proc = None
server_thread=None
client_proc = None
client_thread=None
server_log = None
client_log = None
RSA_Server_thread_active_flag=0
RSA_Client_thread_active_flag=0

ecc_server_proc = None
ecc_server_thread=None
ecc_client_proc = None
ecc_client_thread=None

ECC_Server_thread_active_flag=0
ECC_Client_thread_active_flag=0

def ServerProcess(server_log):
    global server_proc
    if (server_proc is not None):
        try:
            server_proc.terminate()
        except OSError:
            server_proc = None
    #server_proc = exec_cmd.createProcess("openssl s_server -cert CAsigned_rsa_cert.crt -accept 4433 -keyform engine -engine tpm2tss -key rsa_server.tss", server_log)
    server_proc = exec_cmd.createProcess("lxterminal --command='openssl s_server -cert CAsigned_rsa_cert.crt -accept 4433 -keyform engine -engine tpm2tss -key rsa_server.tss'", server_log)


def ClientProcess(client_log):
    global client_proc
    if (client_proc is not None):
        try:
            client_proc.terminate()
        except OSError:
            client_proc = None
    client_proc = exec_cmd.createProcess("lxterminal --command='openssl s_client -connect localhost:4433 -tls1_2 -CAfile CA_rsa_cert.pem'", client_log)


def LogReader(text_server, text_client, server_log, client_log):
    print(("server log is: " + str(server_log)))
    print(("client log is: " + str(client_log)))
    print(("text_server is: " + str(text_server)))
    print(("text_client is: " + str(text_client)))
    time.sleep(2)
    server_log.seek(0)
    client_log.seek(0)
    while (True):
        line_client = client_log.readline()
        if (line_client != ''):
            text_client.AppendText(line_client + "\n")
        line_server = server_log.readline()
        if (line_server != ''):
            text_server.AppendText(line_server + "\n")


# check and kill the processes if they are still running
def checkProcesses():
    global server_proc, client_proc, server_log, client_log
    if (server_proc is not None):
        try:
            server_proc.terminate()
        except OSError:
            server_proc = None
    if (client_proc is not None):
        try:
            client_proc.terminate()
        except OSError:
            client_proc = None
    if (server_log is not None):
        server_log.close()
    if (client_log is not None):
        client_log.close()

def kill_child_processes(parent_pid, sig=signal.SIGTERM):
        ps_command = subprocess.Popen("ps -o pid --ppid %d --noheaders" % parent_pid, shell=True, stdout=subprocess.PIPE)
        ps_output = ps_command.stdout.read()
        retcode = ps_command.wait()
        #assert retcode == 0, "ps command returned %d" % retcode
        if (retcode==0):
            for pid_str in ps_output.split("\n".encode())[:-1]:
                    os.kill(int(pid_str), sig)
        else:
            print("ps command returned %d" % retcode)
class RSA_Server_Thread(threading.Thread):
    
    
    def __init__(self, threadID, Process):
        global RSA_Server_thread_active_flag
        threading.Thread.__init__(self)
        
        self.threadID = threadID
        self.Process = Process
        self.daemon= True
        RSA_Server_thread_active_flag=1

    def run(self):
           
        global RSA_Server_thread_active_flag,server_proc
        try:    
            while RSA_Server_thread_active_flag==1 :
                line = self.Process.stdout.readline()
                if line != '':
                    wx.CallAfter(Publisher.sendMessage, "Server_Text", msg=line) 
                    #os.write(1, line)
                    #print line
                #else:
                #    break
        finally:
            
            RSA_Server_thread_active_flag=0
            print("Exit RSA server Thread")
            wx.CallAfter(Publisher.sendMessage, "Server_Text", msg="Server Stopped..\n")

    def get_id(self): 
  
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'):
            return self._thread_id 
        for id, thread in list(threading._active.items()): 
            if thread is self: 
                print("thread ID")
                print(id)
                return id
   
    def raise_exception(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure')            
        
class RSA_Client_Thread(threading.Thread):
    
    def __init__(self, threadID, Process):
        global RSA_Client_thread_active_flag
        threading.Thread.__init__(self)
        
        self.threadID = threadID
        self.Process = Process
        self.daemon= True
        RSA_Client_thread_active_flag=1

    def run(self):
           
        global RSA_Client_thread_active_flag,client_proc
        while RSA_Client_thread_active_flag==1 :
            line = self.Process.stdout.readline()
            
            if line != '':
                wx.CallAfter(Publisher.sendMessage, "Client_Text", msg=line) 
            #else:
            #    break
        RSA_Client_thread_active_flag=0
        #self.Process.terminate()
        #self.Process.wait()
        #client_proc=None
        print("Exit RSA client Thread")
        wx.CallAfter(Publisher.sendMessage, "Client_Text", msg="Client Stopped..\n")

        
class Tab_RSA_CS(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        steps_sizer = wx.BoxSizer(wx.VERTICAL)
        server_sizer = wx.BoxSizer(wx.VERTICAL)
        client_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # instantiate the objects
        button_gen_ca = wx.Button(self, -1, 'Generate CA && CA Cert', size = (-1, 48))
        button_gen_keypair = wx.Button(self, -1, 'Create Keypair (for server)', size = (-1, 48))
        button_gen_csr = wx.Button(self, -1, 'Create CSR', size = (-1, 48))
        button_gen_cert = wx.Button(self, -1, 'Create Server Cert', size = (-1, 48))
        button_start_server = wx.Button(self, -1, 'Start/Stop Server')
        button_start_client = wx.Button(self, -1, 'Start/Stop Client')
        button_write_from_server = wx.Button(self, -1, 'Write to Client')
        button_write_from_client = wx.Button(self, -1, 'Write to Server')
        button_flush_client = wx.Button(self, -1, 'Clear client text', size = (-1, 48))
        button_flush_server = wx.Button(self, -1, 'Clear server text', size = (-1, 48))
        self.text_client = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.text_client.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.text_server = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.text_server.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.input_client = wx.TextCtrl(self, -1,value="Send from Client")
        self.input_server = wx.TextCtrl(self, -1,value="Send from Server")
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the sizers to the main sizer
        mainsizer.Add(steps_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 5)
        mainsizer.Add(server_sizer, 1, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)
        mainsizer.Add(client_sizer, 1, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)

        # attach the objects to the sizers
        steps_sizer.Add(button_gen_ca, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_gen_keypair, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_gen_csr, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_gen_cert, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_flush_server, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_flush_client, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.AddSpacer(236)
        steps_sizer.Add(backbutton, 0, wx.ALL, 5)
        
        server_sizer.Add(self.text_server, 1, wx.EXPAND | wx.ALL, 5)
        server_sizer.Add(button_start_server, 0, wx.EXPAND | wx.ALL, 5)
        server_sizer.Add(self.input_server, 0, wx.EXPAND | wx.ALL, 5)
        server_sizer.Add(button_write_from_server, 0, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(self.text_client, 1, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(button_start_client, 0, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(self.input_client, 0, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(button_write_from_client, 0, wx.EXPAND | wx.ALL, 5)

        # Set tooltips
        button_gen_ca.SetToolTip(wx.ToolTip("Generate Key Pair and Self-Signed Certificate for the Certificate Authority (CA)."))
        button_gen_keypair.SetToolTip(wx.ToolTip("Generate Key Pair for the Server."))
        button_gen_csr.SetToolTip(wx.ToolTip("Generate Certificate Signing Request (CSR) for the CA, from the Server's private key."))
        button_gen_cert.SetToolTip(wx.ToolTip("Generate Server Certificate from the CSR and the CA's private key."))

        # declare and bind events
        self.Bind(wx.EVT_BUTTON, self.OnFlushClient, button_flush_client)
        self.Bind(wx.EVT_BUTTON, self.OnFlushServer, button_flush_server)
        self.Bind(wx.EVT_BUTTON, self.OnGenCA1, button_gen_ca)
        self.Bind(wx.EVT_BUTTON, self.OnGenKeyPair1, button_gen_keypair)
        self.Bind(wx.EVT_BUTTON, self.OnGenCSR1, button_gen_csr)
        self.Bind(wx.EVT_BUTTON, self.OnGenCert, button_gen_cert)
        self.Bind(wx.EVT_BUTTON, self.OnStartServer, button_start_server)
        self.Bind(wx.EVT_BUTTON, self.OnStartClient, button_start_client)
        self.Bind(wx.EVT_BUTTON, self.OnWriteServer, button_write_from_server)
        self.Bind(wx.EVT_BUTTON, self.OnWriteClient, button_write_from_client)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)
        # Setup Publisher for text field update
        Publisher.subscribe(self.Upd_Server_Status, "Server_Text")
        Publisher.subscribe(self.Upd_Client_Status, "Client_Text")
        
        self.server_multiproc = None
        self.client_multiproc = None
        self.log_reader_multiproc = None

        self.SetSizer(mainsizer)
    def Upd_Server_Status(self,msg):
        self.text_server.AppendText(msg)
        
    def Upd_Client_Status(self,msg):
        self.text_client.AppendText(msg)        
         
    def OnFlushClient(self, evt):
        self.text_client.Clear()

    def OnFlushServer(self, evt):
        self.text_server.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        #~ global server_proc,client_proc,RSA_Server_thread_active_flag,RSA_Client_thread_active_flag
        #~ if (server_proc is not None):
            #~ RSA_Server_thread_active_flag=0

            #~ if (client_proc is not None):
                #~ RSA_Client_thread_active_flag=0
                #~ print "Client Thread Active..killing it: %d \n" % client_proc.pid
                #~ kill_child_processes(client_proc.pid)
                #~ client_proc.terminate()
                #~ client_proc.wait()
                #~ client_proc = None                

            #~ print "Server Thread Active..killing it: %d \n" % server_proc.pid
            #~ kill_child_processes(server_proc.pid)
            #~ #server_proc.stdin.write("stop\n")
            #~ #server_thread.raise_exception()
            #~ #server_thread.join()
            
            #~ server_proc.terminate()
            #~ server_proc.wait()
            #~ server_proc = None
        
        self.Parent.Parent.OnCloseWindow(None)
        
    def Destroy(self):
        global server_proc,client_proc,RSA_Server_thread_active_flag,RSA_Client_thread_active_flag
        if (server_proc is not None):
            RSA_Server_thread_active_flag=0

            if (client_proc is not None):
                RSA_Client_thread_active_flag=0
                print("Client Thread Active..killing it: %d \n" % client_proc.pid)
                kill_child_processes(client_proc.pid)
                client_proc.terminate()
                client_proc.wait()
                client_proc = None                

            print("Server Thread Active..killing it: %d \n" % server_proc.pid)
            kill_child_processes(server_proc.pid)
            
            server_proc.terminate()
            server_proc.wait()
            server_proc = None
                    
    def OnGenCA1(self, evt):
        self.text_server.AppendText("Generating CA key-pair...\n")
        wx.CallLater(10, self.OnGenCA)
    
    def OnGenCA(self):

        exec_cmd.execCLI(["rm", "rsa_CA.tss", ])
        exec_cmd.execCLI(["rm", "CA_rsa_cert.pem", ])
        exec_cmd.execCLI(["rm", "rsa_server.tss", ])
        exec_cmd.execCLI(["rm", "server_rsa.csr", ])
        exec_cmd.execCLI(["rm", "CAsigned_rsa_cert.crt", ])


        if (exec_cmd.ownerAuth !=""):

            f = open("temp.conf", "w+")
            f.write(exec_cmd.openssl_cnf)
            f.close()
            exec_cmd.execCLI([
                "tpm2tss-genkey",
                "-a", "rsa",
                "-o",exec_cmd.ownerAuth,
                "rsa_CA.tss",
            ])
            self.text_server.AppendText("'tpm2tss-genkey -a rsa -o %s rsa_CA.tss'\n" % exec_cmd.ownerAuth)
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            self.text_server.AppendText("Creating Self-Signed Certificate:\n")

            cmd =" openssl req -config temp.conf -key rsa_CA.tss -new -x509 -days 7300 -sha256 -engine tpm2tss -keyform engine  -out CA_rsa_cert.pem -subj '/C=SG/ST=Singapore/L=Singapore/O=Infineon Technologies/OU=DSS/CN=TPMEvalKitCA'"
            ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            command_output = ps_command.stdout.read()
            retcode = ps_command.wait()        
        else:
            exec_cmd.execCLI([
                "tpm2tss-genkey",
                "-a", "rsa",
                "rsa_CA.tss",
            ])
            self.text_server.AppendText("Generating CA key-pair: 'tpm2tss-genkey -a rsa  rsa_CA.tss'\n" )
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            self.text_server.AppendText("Creating Self-Signed Certificate:\n")

            cmd =" openssl req -key rsa_CA.tss -new -x509 -days 7300 -sha256 -engine tpm2tss -keyform engine  -out CA_rsa_cert.pem -subj '/C=SG/ST=Singapore/L=Singapore/O=Infineon Technologies/OU=DSS/CN=TPMEvalKitCA'"
            ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            command_output = ps_command.stdout.read()
            retcode = ps_command.wait()        


        
        self.text_server.AppendText(str(command_output))
        self.text_server.AppendText(str(cmd)+"\n")
        
        #~ self.text_server.AppendText("openssl req -key rsa_CA.tss -new -x509 -days 7300 -sha256 -engine tpm2tss -keyform engine -extensions v3_ca -out CA_rsa_cert.pem -subj '/C=SG/ST=Singapore/L=Singapore/O=Infineon Technologies/OU=DSS/CN=TPMEvalKitCA'\n")
        self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnGenKeyPair1(self, evt):
        self.text_server.AppendText("Generating SERVER key-pair...\n")
        wx.CallLater(10, self.OnGenKeyPair)
    
    def OnGenKeyPair(self):
        if (exec_cmd.ownerAuth !=""):
            exec_cmd.execCLI([
                "tpm2tss-genkey",
                "-o",exec_cmd.ownerAuth,
                "-a", "rsa",
                "rsa_server.tss",
            ])
            self.text_server.AppendText("'tpm2tss-genkey -o %s -a rsa rsa_server.tss'\n" %exec_cmd.ownerAuth)
        else:
            exec_cmd.execCLI([
                "tpm2tss-genkey",
                "-a", "rsa",
                "rsa_server.tss",
            ])
            self.text_server.AppendText("Generating SERVER key-pair: 'tpm2tss-genkey -a rsa rsa_server.tss'\n")
        self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnGenCSR1(self, evt):
        self.text_server.AppendText("Creating Certificate Signing Request...\n")
        wx.CallLater(10, self.OnGenCSR)
    
    def OnGenCSR(self):
        if (exec_cmd.ownerAuth !=""):
            f = open("temp.conf", "w+")
            f.write(exec_cmd.openssl_cnf)
            f.close()
            #~ self.text_server.AppendText("Creating Certificate Signing Request:\n")
            command_output = exec_cmd.execCLI([
                "openssl",
                "req", "-new",
                "-config","temp.conf",
                "-engine", "tpm2tss",
                "-key", "rsa_server.tss",
                "-keyform", "engine",
                "-subj", "/CN=TPM_UI/O=Infineon/C=SG",
                "-out", "server_rsa.csr",
            ])
            self.text_server.AppendText(str(command_output))
            self.text_server.AppendText("openssl req -new -config temp.conf -engine tpm2tss -key rsa_server.tss -keyform engine -subj /CN=TPM_UI/O=Infineon/C=SG -out server_rsa.csr\n")
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        else:
            command_output = exec_cmd.execCLI([
                "openssl",
                "req", "-new",
                "-engine", "tpm2tss",
                "-key", "rsa_server.tss",
                "-keyform", "engine",
                "-subj", "/CN=TPM_UI/O=Infineon/C=SG",
                "-out", "server_rsa.csr",
            ])
            self.text_server.AppendText(str(command_output))
            self.text_server.AppendText("openssl req -new -engine tpm2tss -key rsa_server.tss -keyform engine -subj /CN=TPM_UI/O=Infineon/C=SG -out server_rsa.csr\n")
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            
    def OnGenCert(self, evt):
        self.text_server.AppendText("Creating Server Certificate...\n")
        if (exec_cmd.ownerAuth !=""):
            f = open("temp.conf", "w+")
            f.write(exec_cmd.openssl_cnf)
            f.close()
            openssl_cmd="OPENSSL_CONF=temp.conf openssl x509 -req -in server_rsa.csr -CA CA_rsa_cert.pem -CAkey rsa_CA.tss -engine tpm2tss -CAkeyform engine -out CAsigned_rsa_cert.crt -days 365 -sha256 -CAcreateserial"                
            server_proc = exec_cmd.createProcess(openssl_cmd, server_log)
            #~ command_output = exec_cmd.execCLI([
                #~ "OPENSSL_CONF=temp.conf", "openssl", "x509", 
                #~ "-req", "-in", "server_rsa.csr",
                #~ "-CA","CA_rsa_cert.pem",
                #~ "-CAkey", "rsa_CA.tss", "-engine tpm2tss", 
                #~ "-CAkeyform", "engine",
                #~ "-out", "CAsigned_rsa_cert.crt", 
                #~ "-days", "365", "-sha256", "-CAcreateserial", 
            #~ ])
            #~ self.text_server.AppendText(str(command_output))
            self.text_server.AppendText("OPENSSL_CONF=temp.conf openssl x509 -req -in server_rsa.csr -CA CA_rsa_cert.pem -CAkey rsa_CA.tss -engine tpm2tss -CAkeyform engine -out CAsigned_rsa_cert.crt -days 365 -sha256 -CAcreateserial\n")
        else:
            command_output = exec_cmd.execCLI([
                "openssl",
                "req", "-x509", "-sha256",
                "-engine", "tpm2tss",
                "-key", "rsa_CA.tss",
                "-keyform", "engine",
                "-in", "server_rsa.csr",
                "-out", "CAsigned_rsa_cert.crt",
            ])
            self.text_server.AppendText(str(command_output))
            self.text_server.AppendText("openssl req -x509 -sha256 -key rsa_CA.tss -engine tpm2tss -keyform engine -in server_rsa.csr -out CAsigned_rsa_cert.crt\n")
            

        self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnStartServer(self, evt):
        global server_proc,client_proc,server_log
        global server_thread
        global RSA_Server_thread_active_flag,RSA_Client_thread_active_flag
        if (server_proc is not None):
            RSA_Server_thread_active_flag=0

            if (client_proc is not None):
                RSA_Client_thread_active_flag=0
                print("Client Thread Active..killing it: %d \n" % client_proc.pid)
                kill_child_processes(client_proc.pid)
                client_proc.terminate()
                client_proc.wait()
                client_proc = None                

            print("Server Thread Active..killing it: %d \n" % server_proc.pid)
            kill_child_processes(server_proc.pid)
            #server_proc.stdin.write("stop\n")
            #server_thread.raise_exception()
            #server_thread.join()
            
            server_proc.terminate()
            server_proc.wait()
            server_proc = None

        else:
            #server_proc = exec_cmd.createProcess("lxterminal --title=Server --geometry=55x24 --command='openssl s_server -cert CAsigned_rsa_cert.crt -accept 4433 -keyform engine -engine tpm2tss -key rsa_server.tss'", server_log)
            if (exec_cmd.ownerAuth !=""):
                openssl_cmd="OPENSSL_CONF=temp.conf openssl s_server -cert CAsigned_rsa_cert.crt -accept 4433 -keyform engine -engine tpm2tss -key rsa_server.tss"
            else:
                openssl_cmd="openssl s_server -cert CAsigned_rsa_cert.crt -accept 4433 -keyform engine -engine tpm2tss -key rsa_server.tss"                
            
            server_proc = exec_cmd.createProcess(openssl_cmd, server_log)
            server_thread = RSA_Server_Thread(1, server_proc)
            server_thread.start()
            wx.CallAfter(Publisher.sendMessage, "Server_Text", msg="\n\n" + openssl_cmd +"\n\n")      

    def OnStartClient(self, evt):
        global client_proc,client_log,server_proc
        global RSA_Client_thread_active_flag,RSA_Server_thread_active_flag
        
        if (client_proc is not None):
            RSA_Client_thread_active_flag=0
            print("Client Thread Active..killing it: %d \n" % client_proc.pid)
            kill_child_processes(client_proc.pid)
            client_proc.terminate()
            client_proc.wait()
            
            client_proc = None
        else:
            #client_proc = exec_cmd.createProcess("lxterminal --title=Server --geometry=55x24 --command='openssl s_server -cert CAsigned_rsa_cert.crt -accept 4433 -keyform engine -engine tpm2tss -key rsa_server.tss'", server_log)
            openssl_cmd="openssl s_client -connect localhost:4433 -tls1_2 -CAfile CA_rsa_cert.pem"
            if (server_proc is not None):
                client_proc = exec_cmd.createProcess(openssl_cmd, client_log)
                client_thread = RSA_Client_Thread(2, client_proc)
                client_thread.start() 
                wx.CallAfter(Publisher.sendMessage, "Client_Text", msg="\n\n" +openssl_cmd+"\n\n")
            else:
                wx.CallAfter(Publisher.sendMessage, "Client_Text", msg="Server is not active..\n")     
            
    def OnWriteServer(self, evt):
        global server_proc
        if (server_proc is None):
            self.text_server.AppendText("Server is not running!\n")
            return
        write_value = self.input_server.GetValue()
        if (write_value == ""):
            self.text_server.AppendText("I need something to write!\n")
            return
        server_proc.stdin.write((write_value+"\n").encode())
        server_proc.stdin.flush()
    
    def OnWriteClient(self, evt):
        global client_proc
        if (client_proc is None):
            self.text_client.AppendText("Client is not running!\n")
            return
        write_value = self.input_client.GetValue()
        if (write_value == ""):
            self.text_client.AppendText("I need something to write!\n")
            return
   
        client_proc.stdin.write((write_value+"\n").encode())
        client_proc.stdin.flush()
        


class Tab_ECC_CS(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        steps_sizer = wx.BoxSizer(wx.VERTICAL)
        server_sizer = wx.BoxSizer(wx.VERTICAL)
        client_sizer = wx.BoxSizer(wx.VERTICAL)

        # instantiate the objects
        button_gen_ca = wx.Button(self, -1, 'Generate CA && CA Cert', size = (-1, 48))
        button_gen_keypair = wx.Button(self, -1, 'Create Keypair (for server)', size = (-1, 48))
        button_gen_csr = wx.Button(self, -1, 'Create CSR', size = (-1, 48))
        button_gen_cert = wx.Button(self, -1, 'Create Server Cert', size = (-1, 48))
        button_start_server = wx.Button(self, -1, 'Start/Stop Server')
        button_start_client = wx.Button(self, -1, 'Start/Stop Client')
        button_write_from_server = wx.Button(self, -1, 'Write to Client')
        button_write_from_client = wx.Button(self, -1, 'Write to Server')
        button_flush_client = wx.Button(self, -1, 'Clear client text', size = (-1, 48))
        button_flush_server = wx.Button(self, -1, 'Clear server text', size = (-1, 48))
        self.text_client = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.text_server = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.text_client.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.text_server.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        self.input_client = wx.TextCtrl(self, -1,value="Send from Client")
        self.input_server = wx.TextCtrl(self, -1,value="Send from Server")
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the objects to the sizers
        mainsizer.Add(steps_sizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 5)
        mainsizer.Add(server_sizer, 1, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)
        mainsizer.Add(client_sizer, 1, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)
        steps_sizer.Add(button_gen_ca, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_gen_keypair, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_gen_csr, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_gen_cert, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_flush_server, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.Add(button_flush_client, 0, wx.EXPAND | wx.ALL, 5)
        steps_sizer.AddSpacer(236)
        steps_sizer.Add(backbutton, 0, wx.ALL, 5)
        server_sizer.Add(self.text_server, 1, wx.EXPAND | wx.ALL, 5)
        server_sizer.Add(button_start_server, 0, wx.EXPAND | wx.ALL, 5)
        server_sizer.Add(self.input_server, 0, wx.EXPAND | wx.ALL, 5)
        server_sizer.Add(button_write_from_server, 0, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(self.text_client, 1, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(button_start_client, 0, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(self.input_client, 0, wx.EXPAND | wx.ALL, 5)
        client_sizer.Add(button_write_from_client, 0, wx.EXPAND | wx.ALL, 5)

        # Set tooltips
        button_gen_ca.SetToolTip(wx.ToolTip("Generate Key Pair and Self-Signed Certificate for the Certificate Authority (CA)."))
        button_gen_keypair.SetToolTip(wx.ToolTip("Generate Key Pair for the Server."))
        button_gen_csr.SetToolTip(wx.ToolTip("Generate Certificate Signing Request (CSR) for the CA, from the Server's private key."))
        button_gen_cert.SetToolTip(wx.ToolTip("Generate Server Certificate from the CSR and the CA's private key."))

        # declare and bind events
        self.Bind(wx.EVT_BUTTON, self.OnFlushClient, button_flush_client)
        self.Bind(wx.EVT_BUTTON, self.OnFlushServer, button_flush_server)
        self.Bind(wx.EVT_BUTTON, self.OnGenCA1, button_gen_ca)
        self.Bind(wx.EVT_BUTTON, self.OnGenKeyPair1, button_gen_keypair)
        self.Bind(wx.EVT_BUTTON, self.OnGenCSR1, button_gen_csr)
        self.Bind(wx.EVT_BUTTON, self.OnGenCert, button_gen_cert)
        self.Bind(wx.EVT_BUTTON, self.OnStartServer, button_start_server)
        self.Bind(wx.EVT_BUTTON, self.OnStartClient, button_start_client)
        self.Bind(wx.EVT_BUTTON, self.OnWriteServer, button_write_from_server)
        self.Bind(wx.EVT_BUTTON, self.OnWriteClient, button_write_from_client)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)
        
        # Setup Publisher for text field update
        Publisher.subscribe(self.Upd_Server_Status, "ECC_Server_Text")
        Publisher.subscribe(self.Upd_Client_Status, "ECC_Client_Text")

        self.SetSizer(mainsizer)
        # declare threads related parameters
        self.Server_thread_active_flag=0
        self.Client_thread_active_flag=0
        self.server_proc=None
        self.client_proc=None
        
    def server_thread(self):
        
        try:    
            while self.Server_thread_active_flag==1 :
                line = self.server_proc.stdout.readline()
                if line != '':
                    wx.CallAfter(Publisher.sendMessage, "ECC_Server_Text", msg=line) 
        finally:
            
            self.Server_thread_active_flag=0
            print("Exit ECC server Thread\n")
            wx.CallAfter(Publisher.sendMessage, "ECC_Server_Text", msg="Server Stopped..\n")

    def client_thread(self):
        
        while self.Client_thread_active_flag==1 :
            line = self.client_proc.stdout.readline()
            
            if line != '':
                wx.CallAfter(Publisher.sendMessage, "ECC_Client_Text", msg=line) 
            
        self.Client_thread_active_flag=0
        print("Exit ECC client Thread\n")
        wx.CallAfter(Publisher.sendMessage, "ECC_Client_Text", msg="Client Stopped..\n")        
                
    def Upd_Server_Status(self,msg):
        self.text_server.AppendText(msg)
        
    def Upd_Client_Status(self,msg):
        self.text_client.AppendText(msg)                
        
    def OnBack(self, evt):

        #~ if (self.server_proc is not None):
            #~ self.Server_thread_active_flag=0

            #~ if (self.client_proc is not None):
                #~ self.Client_thread_active_flag=0
                #~ print "Client Thread Active..killing it: %d \n" % self.client_proc.pid
                #~ kill_child_processes(self.client_proc.pid)
                #~ self.client_proc.terminate()
                #~ self.client_proc.wait()
                #~ self.client_proc = None                

            #~ print "Server Thread Active..killing it: %d \n" % self.server_proc.pid
            #~ kill_child_processes(self.server_proc.pid)
            
            #~ self.server_proc.terminate()
            #~ self.server_proc.wait()
            #~ self.server_proc = None
                    
        self.Parent.Parent.OnCloseWindow(None)
    
    def Destroy(self):
        if (self.server_proc is not None):
            self.Server_thread_active_flag=0

            if (self.client_proc is not None):
                self.Client_thread_active_flag=0
                print("Client Thread Active..killing it: %d \n" % self.client_proc.pid)
                kill_child_processes(self.client_proc.pid)
                self.client_proc.terminate()
                self.client_proc.wait()
                self.client_proc = None                

            print("Server Thread Active..killing it: %d \n" % self.server_proc.pid)
            kill_child_processes(self.server_proc.pid)
            
            self.server_proc.terminate()
            self.server_proc.wait()
            self.server_proc = None        
    
    def OnFlushClient(self, evt):
        self.text_client.Clear()

    def OnFlushServer(self, evt):
        self.text_server.Clear()
    
    def OnGenCA1(self, evt):
        self.text_server.AppendText("Generating CA key-pair...\n")
        wx.CallLater(10, self.OnGenCA)
        
    def OnGenCA(self):
        exec_cmd.execCLI(["rm", "ecc_CA.tss", ])
        exec_cmd.execCLI(["rm", "CA_ecc_cert.pem", ])
        exec_cmd.execCLI(["rm", "ecc_server.tss", ])
        exec_cmd.execCLI(["rm", "server_ecc.csr", ])
        exec_cmd.execCLI(["rm", "CAsigned_ecc_cert.crt", ])

        if (exec_cmd.ownerAuth !=""):

            f = open("temp.conf", "w+")
            f.write(exec_cmd.openssl_cnf)
            f.close()
            exec_cmd.execCLI([
                "tpm2tss-genkey",
                "-a", "ecdsa",
                "-o",exec_cmd.ownerAuth,
                "ecc_CA.tss",
            ])
            
            self.text_server.AppendText("'tpm2tss-genkey -a ecdsa -o %s ecc_CA.tss'\n" % exec_cmd.ownerAuth)
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            self.text_server.AppendText("Creating Self-Signed Certificate:\n")
            command_output = exec_cmd.execCLI([
                "openssl",
                "req", "-new",
                "-config","temp.conf",
                "-engine", "tpm2tss",
                "-key", "ecc_CA.tss",
                "-keyform", "engine",
                "-x509", "-sha256",
                "-days", "7300",
                #~ "-extensions", "v3_ca",
                "-subj", "/C=SG/ST=Singapore/L=Singapore/O=Infineon Technologies/OU=DSS/CN=TPMEvalKitCA",
                "-out", "CA_ecc_cert.pem",
            ])
            self.text_server.AppendText(str(command_output))
            self.text_server.AppendText("openssl req -config temp.conf -key ecc_CA.tss -new -x509 -days 7300 -sha256 -engine tpm2tss -keyform engine -extensions v3_ca -out CA_ecc_cert.pem -subj '/C=SG/ST=Singapore/L=Singapore/O=Infineon Technologies/OU=DSS/CN=TPMEvalKitCA'\n")
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        else:
            exec_cmd.execCLI([
                "tpm2tss-genkey",
                "-a", "ecdsa",
                "ecc_CA.tss",
            ])
            self.text_server.AppendText("Generating CA key-pair: 'tpm2tss-genkey -a ecdsa ecc_CA.tss'\n")
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            self.text_server.AppendText("Creating Self-Signed Certificate:\n")
            command_output = exec_cmd.execCLI([
                "openssl",
                "req", "-new",
                "-engine", "tpm2tss",
                "-key", "ecc_CA.tss",
                "-keyform", "engine",
                "-x509", "-sha256",
                "-days", "7300",
                #~ "-extensions", "v3_ca",
                "-subj", "/C=SG/ST=Singapore/L=Singapore/O=Infineon Technologies/OU=DSS/CN=TPMEvalKitCA",
                "-out", "CA_ecc_cert.pem",
            ])
            self.text_server.AppendText(str(command_output))
            self.text_server.AppendText("openssl req -key ecc_CA.tss -new -x509 -days 7300 -sha256 -engine tpm2tss -keyform engine -extensions v3_ca -out CA_ecc_cert.pem -subj '/C=SG/ST=Singapore/L=Singapore/O=Infineon Technologies/OU=DSS/CN=TPMEvalKitCA'\n")
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            
    def OnGenKeyPair1(self, evt):
        self.text_server.AppendText("Generating SERVER key-pair...\n")
        wx.CallLater(10, self.OnGenKeyPair)
    
    def OnGenKeyPair(self):
        
        if (exec_cmd.ownerAuth !=""):
        
            exec_cmd.execCLI([
                "tpm2tss-genkey",
                "-a", "ecdsa",
                "-o",exec_cmd.ownerAuth,   
                "ecc_server.tss",
            ])
            self.text_server.AppendText("'tpm2tss-genkey -a ecdsa -o %s ecc_server.tss'\n" % exec_cmd.ownerAuth)
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        else:
            exec_cmd.execCLI([
            "tpm2tss-genkey",
            "-a", "ecdsa",
            "ecc_server.tss",
            ])
            self.text_server.AppendText("Generating SERVER key-pair: 'tpm2tss-genkey -a ecdsa ecc_server.tss'\n")
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnGenCSR1(self, evt):
        self.text_server.AppendText("Creating Certificate Signing Request...\n")
        wx.CallLater(10, self.OnGenCSR)
        
    def OnGenCSR(self):
        if (exec_cmd.ownerAuth !=""):

            f = open("temp.conf", "w+")
            f.write(exec_cmd.openssl_cnf)
            f.close()

            command_output = exec_cmd.execCLI([
                "openssl",
                "req", "-new",
                "-config","temp.conf",
                "-engine", "tpm2tss",
                "-key", "ecc_server.tss",
                "-keyform", "engine",
                "-subj", "/CN=TPM_UI/O=Infineon/C=SG",
                "-out", "server_ecc.csr",
            ])
            self.text_server.AppendText(str(command_output))
            self.text_server.AppendText("openssl req -new -config temp.conf -engine tpm2tss -key ecc_server.tss -keyform engine -subj /CN=TPM_UI/O=Infineon/C=SG -out server_ecc.csr\n")
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        else:
            command_output = exec_cmd.execCLI([
            "openssl",
            "req", "-new",
            "-engine", "tpm2tss",
            "-key", "ecc_server.tss",
            "-keyform", "engine",
            "-subj", "/CN=TPM_UI/O=Infineon/C=SG",
            "-out", "server_ecc.csr",
        ])
        self.text_server.AppendText(str(command_output))
        self.text_server.AppendText("openssl req -new -engine tpm2tss -key ecc_server.tss -keyform engine -subj /CN=TPM_UI/O=Infineon/C=SG -out server_ecc.csr\n")
        self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnGenCert(self, evt):
        self.text_server.AppendText("Creating Server Certificate...\n")
        if (exec_cmd.ownerAuth !=""):
   
            f = open("temp.conf", "w+")
            f.write(exec_cmd.openssl_cnf)
            f.close()
            openssl_cmd="OPENSSL_CONF=temp.conf openssl x509 -req -in server_ecc.csr -CA CA_ecc_cert.pem -CAkey ecc_CA.tss -engine tpm2tss -CAkeyform engine -out CAsigned_ecc_cert.crt -days 365 -sha256 -CAcreateserial"                
            server_proc = exec_cmd.createProcess(openssl_cmd, server_log)
            #~ command_output = exec_cmd.execCLI([
            #~ "openssl",
            #~ "req", "-x509", "-sha256",
            #~ "-config","temp.conf",
            #~ "-engine", "tpm2tss",
            #~ "-key", "ecc_CA.tss",
            #~ "-keyform", "engine",
            #~ "-in", "server_ecc.csr",
            #~ "-out", "CAsigned_ecc_cert.crt",
            #~ ])
            #~ self.text_server.AppendText(str(command_output))
            self.text_server.AppendText("OPENSSL_CONF=temp.conf openssl x509 -req -in server_ecc.csr -CA CA_ecc_cert.pem -CAkey ecc_CA.tss -engine tpm2tss -CAkeyform engine -out CAsigned_ecc_cert.crt -days 365 -sha256 -CAcreateserial\n")
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        else:
            command_output = exec_cmd.execCLI([
            "openssl",
            "req", "-x509", "-sha256",
            "-engine", "tpm2tss",
            "-key", "ecc_CA.tss",
            "-keyform", "engine",
            "-in", "server_ecc.csr",
            "-out", "CAsigned_ecc_cert.crt",
            ])
            self.text_server.AppendText(str(command_output))
            self.text_server.AppendText("openssl req -x509 -sha256 -key ecc_CA.tss -engine tpm2tss -keyform engine -in server_ecc.csr -out CAsigned_ecc_cert.crt\n")
            self.text_server.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            
    def OnStartServer(self,evt):
        if (self.server_proc is not None):
            self.Server_thread_active_flag=0

            if (self.client_proc is not None):
                self.Client_thread_active_flag=0
                print("Client Thread Active..killing it: %d \n" % self.client_proc.pid)
                kill_child_processes(self.client_proc.pid)
                self.client_proc.terminate()
                self.client_proc.wait()
                self.client_proc = None                

            print("Server Thread Active..killing it: %d \n" % self.server_proc.pid)
            kill_child_processes(self.server_proc.pid)

            self.server_proc.terminate()
            self.server_proc.wait()
            self.server_proc = None

        else:
            if (exec_cmd.ownerAuth !=""):
                openssl_cmd="OPENSSL_CONF=temp.conf openssl s_server -cert CAsigned_ecc_cert.crt -accept 4432 -keyform engine -engine tpm2tss -key ecc_server.tss"
            else:
                openssl_cmd="openssl s_server -cert CAsigned_ecc_cert.crt -accept 4432 -keyform engine -engine tpm2tss -key ecc_server.tss"
            
            self.server_proc = exec_cmd.createProcess(openssl_cmd, None)
            
            self.Server_thread_active_flag=1
            s_thread = threading.Thread(name='Server-daemon', target=self.server_thread)
            s_thread.setDaemon(True)
            s_thread.start()
            wx.CallAfter(Publisher.sendMessage, "ECC_Server_Text", msg="\n\n" + openssl_cmd +"\n\n")      
    
    def OnStartClient(self, evt):
        
        if (self.client_proc is not None):
            self.Client_thread_active_flag=0
            print("Client Thread Active..killing it: %d \n" % self.client_proc.pid)
            kill_child_processes(self.client_proc.pid)
            self.client_proc.terminate()
            self.client_proc.wait()
            
            self.client_proc = None
        else:
            #client_proc = exec_cmd.createProcess("lxterminal --title=Server --geometry=55x24 --command='openssl s_server -cert CAsigned_rsa_cert.crt -accept 4433 -keyform engine -engine tpm2tss -key rsa_server.tss'", server_log)
            openssl_cmd="openssl s_client -connect localhost:4432 -tls1_2 -CAfile CA_ecc_cert.pem"
            if (self.server_proc is not None):
                self.client_proc = exec_cmd.createProcess(openssl_cmd, None)

                self.Client_thread_active_flag=1
                c_thread = threading.Thread(name='Client-daemon', target=self.client_thread)
                c_thread.setDaemon(True)
                c_thread.start()                
                wx.CallAfter(Publisher.sendMessage, "ECC_Client_Text", msg="\n\n" +openssl_cmd+"\n\n")
            else:
                wx.CallAfter(Publisher.sendMessage, "ECC_Client_Text", msg="Server is not active..\n")
                
    def OnWriteServer(self, evt):
        global server_proc
        if (self.server_proc is None):
            self.text_server.AppendText("Server is not running!\n")
            return
        write_value = self.input_server.GetValue()
        if (write_value == ""):
            self.text_server.AppendText("I need something to write!\n")
            return
        self.server_proc.stdin.write((write_value+"\n").encode())
        self.server_proc.stdin.flush()

    def OnWriteClient(self, evt):
        if (self.client_proc is None):
            self.text_client.AppendText("Client is not running!\n")
            return
        write_value = self.input_client.GetValue()
        if (write_value == ""):
            self.text_client.AppendText("I need something to write!\n")
            return
   
        self.client_proc.stdin.write((write_value+"\n").encode())
        self.client_proc.stdin.flush()


class Tab_RSA_MISC(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # instantiate the objects
        self.data_input = wx.TextCtrl(self, -1)
        data_input_blurb = wx.StaticText(self, -1, "Data Input: ")
        self.command_out = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY), size=(500, 500))
        self.command_out.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        button_gen_rsakey = wx.Button(self, -1, 'Generate RSA Keypair', size = (-1, 47))
        button_rsa_enc = wx.Button(self, -1, 'RSA Encrypt', size = (-1, 47))
        button_rsa_dec = wx.Button(self, -1, 'RSA Decrypt', size = (-1, 47))
        button_rsa_sign = wx.Button(self, -1, 'RSA Signing', size = (-1, 47))
        button_rsa_verify = wx.Button(self, -1, 'RSA Verification', size = (-1, 47))
        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        # ~clearbutton = wx.BitmapButton(self, -1, img.clear.getBitmap())
        
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the ui elements to the main sizer
        mainsizer.AddSpacer(5)
        mainsizer.Add(input_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        mainsizer.Add(button_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        mainsizer.Add(self.command_out, 1, wx.EXPAND | wx.TOP, 5)
        input_sizer.Add(data_input_blurb, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        input_sizer.Add(self.data_input, 1, wx.ALL, 5)
        button_sizer.Add(button_gen_rsakey, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        button_sizer.Add(button_rsa_enc, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        button_sizer.Add(button_rsa_dec, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        button_sizer.Add(button_rsa_sign, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        button_sizer.Add(button_rsa_verify, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        button_sizer.Add(clearbutton, 0, wx.ALL, 5)
        button_sizer.Add(backbutton, 0, wx.ALL, 5)

        # Set tooltips
        button_gen_rsakey.SetToolTip(wx.ToolTip("Generate a RSA key pair."))
        button_rsa_enc.SetToolTip(wx.ToolTip("Encrypt the data"))
        button_rsa_dec.SetToolTip(wx.ToolTip("Decrypt the data"))
        button_rsa_sign.SetToolTip(wx.ToolTip("Sign the data input with the private key"))
        button_rsa_verify.SetToolTip(wx.ToolTip("Verify the signature with the public key"))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # declare and bind events
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnGenKey1, button_gen_rsakey)
        self.Bind(wx.EVT_BUTTON, self.OnEnc1, button_rsa_enc)
        self.Bind(wx.EVT_BUTTON, self.OnDec1, button_rsa_dec)
        self.Bind(wx.EVT_BUTTON, self.OnSign1, button_rsa_sign)
        self.Bind(wx.EVT_BUTTON, self.OnVerify, button_rsa_verify)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)

        self.data_input.write("Hello World")
        self.SetSizer(mainsizer)

    def OnGenKey1(self, evt):
        self.command_out.write("Setting up TPM...\n")
        wx.CallLater(10, self.OnGenKey)
    
    def OnGenKey(self):
        exec_cmd.execCLI(["rm", "rsa2.tss", ])
        exec_cmd.execCLI(["rm", "mycipher", ])
        exec_cmd.execCLI(["rm", "mysig", ])

        if (exec_cmd.ownerAuth !=""):
            command_output = exec_cmd.execCLI([
                "tpm2tss-genkey",
                "-o",exec_cmd.ownerAuth,
                "-a", "rsa",
                "rsa2.tss",
            ])
            self.command_out.AppendText(str(command_output))
            self.command_out.AppendText("'tpm2tss-genkey -a rsa rsa2.tss' executed \n")
            command_output = exec_cmd.execCLI([
                "openssl", "rsa",
                "-engine", "tpm2tss",
                "-inform", "engine",
                "-in", "rsa2.tss",
                "-pubout",
                "-outform", "pem",
                "-out", "rsa2.pub",
            ])
            self.command_out.AppendText("'openssl rsa -engine tpm2tss -inform engine -in rsa2.tss -pubout -outform pem -out rsa2.pub' executed \n")
            self.command_out.AppendText("rsa.tss contains: \n")
            filehandle = open("rsa2.tss", 'r')
            self.command_out.AppendText(filehandle.read() + "\n")
            filehandle.close()
            self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        else:
            command_output = exec_cmd.execCLI([
                "tpm2tss-genkey",
                "-a", "rsa",
                "rsa2.tss",
            ])
            self.command_out.AppendText(str(command_output))
            self.command_out.AppendText("'tpm2tss-genkey -a rsa rsa2.tss' executed \n")
            command_output = exec_cmd.execCLI([
                "openssl", "rsa",
                "-engine", "tpm2tss",
                "-inform", "engine",
                "-in", "rsa2.tss",
                "-pubout",
                "-outform", "pem",
                "-out", "rsa2.pub",
            ])
            self.command_out.AppendText("'openssl rsa -engine tpm2tss -inform engine -in rsa2.tss -pubout -outform pem -out rsa2.pub' executed \n")
            self.command_out.AppendText("rsa.tss contains: \n")
            filehandle = open("rsa2.tss", 'r')
            self.command_out.AppendText(filehandle.read() + "\n")
            filehandle.close()
            self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
    
    def OnEnc1(self, evt):
        self.command_out.write("Encrypting Data...\n")
        wx.CallLater(10, self.OnEnc)
    
    def OnEnc(self):
        if (self.data_input.GetValue()):
            input_data = self.data_input.GetValue()
        else:
            self.command_out.AppendText("Input data cannot be blank")
            return
        data_file = open("engine_data.txt", "w")
        data_file.write(input_data)
        data_file.close()
        exec_cmd.execCLI([
            "openssl", "pkeyutl",
            "-pubin",
            "-inkey", "rsa2.pub",
            "-in", "engine_data.txt",
            "-encrypt",
            "-out", "mycipher",
        ])
        self.command_out.AppendText("'openssl pkeyutl -pubin -inkey rsa2.pub -in engine_data.txt -encrypt -out mycipher' executed \n")
        self.command_out.AppendText("mycipher contains: \n")
        command_output = exec_cmd.execCLI(["xxd", "mycipher", ])
        self.command_out.AppendText(command_output + "\n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            
    def OnDec1(self, evt):
        self.command_out.write("Decrypting Data...\n")
        wx.CallLater(10, self.OnDec)

    def OnDec(self):
        if (exec_cmd.ownerAuth !=""):
        
            f = open("temp.conf", "w+")
            f.write(exec_cmd.openssl_cnf)
            f.close()

            cmd ="OPENSSL_CONF=temp.conf openssl pkeyutl -engine tpm2tss -keyform engine -inkey rsa2.tss -decrypt -in mycipher"
            ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            command_output = ps_command.stdout.read()
            retcode = ps_command.wait()        


            self.command_out.AppendText(str(command_output.decode()))
            self.command_out.AppendText("\n' OPENSSL_CONF=temp.conf openssl pkeyutl -engine tpm2tss -keyform engine -inkey rsa2.tss -decrypt -in mycipher' executed \n")
            self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        else:

            cmd ="openssl pkeyutl -engine tpm2tss -keyform engine -inkey rsa2.tss -decrypt -in mycipher"
            ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            command_output = ps_command.stdout.read()
            retcode = ps_command.wait()        


            self.command_out.AppendText(str(command_output.decode()))
            self.command_out.AppendText("\n'openssl pkeyutl -engine tpm2tss -keyform engine -inkey rsa2.tss -decrypt -in mycipher' executed \n")
            self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnSign1(self, evt):
        self.command_out.write("Signing Data Input with Private Key...\n")
        wx.CallLater(10, self.OnSign)

    def OnSign(self):
        if (self.data_input.GetValue()):
            input_data = self.data_input.GetValue()
        else:
            self.command_out.AppendText("Input data cannot be blank\n")
            return
        data_file = open("engine_data.txt", "w")
        data_file.write(input_data)
        data_file.close()
        if (exec_cmd.ownerAuth !=""):
            #~ exec_cmd.execCLI([
                #~ "openssl", "pkeyutl",
                #~ "-engine", "tpm2tss",
                #~ "-keyform", "engine",
                #~ "-inkey", "rsa2.tss",
                #~ "-in", "engine_data.txt",
                #~ "-sign",
                #~ "-out", "mysig",
            #~ ])

            f = open("temp.conf", "w+")
            f.write(exec_cmd.openssl_cnf)
            f.close()

            cmd ="OPENSSL_CONF=temp.conf openssl pkeyutl -engine tpm2tss -keyform engine -inkey rsa2.tss -sign -in engine_data.txt -out mysig"
        else:
            cmd ="openssl pkeyutl -engine tpm2tss -keyform engine -inkey rsa2.tss -sign -in engine_data.txt -out mysig"
        ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        command_output = ps_command.stdout.read()
        retcode = ps_command.wait()        

        self.command_out.AppendText(cmd +" executed \n")
        self.command_out.AppendText("mysig contains: \n")
        command_output = exec_cmd.execCLI(["xxd", "mysig", ])
        self.command_out.AppendText(command_output + "\n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            
    def OnVerify(self, evt):
        input_data = self.data_input.GetValue()
        if(input_data==""):
            self.command_out.AppendText("Input data cannot be blank\n")
            return
        data_file = open("engine_data.txt", "w")
        data_file.write(input_data)
        data_file.close()
        command_output = exec_cmd.execCLI([
            "openssl", "pkeyutl",
            "-pubin",
            "-inkey", "rsa2.pub",
            "-verify",
            "-in", "engine_data.txt",
            "-sigfile", "mysig",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'openssl pkeyutl -pubin -inkey rsa2.pub -verify -in engine_data.txt -sigfile mysig' executed \n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnClear(self, evt):
        self.command_out.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)


class Tab_RNG(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # instantiate the objects
        button_gen_rng = wx.Button(self, -1, 'Generate RNG', size = (-1, 47))
        self.rng_input = wx.TextCtrl(self, -1)
        rng_input_blurb = wx.StaticText(self, -1, "No. of bytes to be generated:")
        self.command_out = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.command_out.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        rng_type_blurb = wx.StaticText(self, -1, "Pick encoding of Random Number:")
        self.rng_type = wx.ComboBox(self, -1, "RN Encoding", choices=rng_type_list, style=wx.CB_READONLY)
        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        # ~clearbutton = wx.BitmapButton(self, -1, img.clear.getBitmap())
        
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the ui elements to the main sizer
        mainsizer.Add(button_sizer, 0, wx.EXPAND | wx.LEFT, 5)
        mainsizer.Add(self.command_out, 1, wx.EXPAND, 0)
        button_sizer.Add(rng_input_blurb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        button_sizer.Add(self.rng_input, 1, wx.ALIGN_CENTRE | wx.RIGHT, 10)
        button_sizer.Add(rng_type_blurb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        button_sizer.Add(self.rng_type, 1, wx.ALIGN_CENTRE | wx.LEFT, 5)
        button_sizer.Add(button_gen_rng, 0, wx.ALIGN_CENTRE | wx.LEFT, 10)
        button_sizer.Add(clearbutton, 0, wx.ALIGN_CENTRE | wx.LEFT, 10)
        button_sizer.Add(backbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

        # Set tooltips
        button_gen_rng.SetToolTip(wx.ToolTip("Generate a Random Number, output is based on the dropdown menu."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # declare and bind events
        self.Bind(wx.EVT_BUTTON, self.OnGenRNG, button_gen_rng)
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)

        self.rng_input.write("32")
        self.rng_type.SetSelection(0)
        self.SetSizer(mainsizer)

    def OnClear(self, evt):
        self.command_out.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)

    def OnGenRNG(self, evt):
        no_bytes = self.rng_input.GetValue()
        try:
            no_bytes = abs(int(no_bytes))
        except ValueError:
            self.command_out.AppendText("Number of bytes is not an integer, try again.\n")
            return
        rng_output_type = self.rng_type.GetSelection()
        if (no_bytes > 128):
            no_bytes = 128
            self.command_out.AppendText("Number of bytes restricted to 128 for performance purposes.\n")
        # if output type is hex
        if (rng_output_type == 0):
            command_output = exec_cmd.execCLI([
                "openssl", "rand",
                "-engine", "tpm2tss",
                "-hex", str(no_bytes),
            ])
            split_output = command_output.split("\n")
            for value in split_output:
                if "warning" not in value.lower():
                    self.command_out.AppendText(value + "\n")
            self.command_out.AppendText("'openssl rand -engine tpm2tss -hex " + str(no_bytes) + "' executed \n")
            self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        # if output type is base64
        elif (rng_output_type == 1):
            command_output = exec_cmd.execCLI([
                "openssl", "rand",
                "-engine", "tpm2tss",
                "-base64", str(no_bytes),
            ])
            split_output = command_output.split("\n")
            for value in split_output:
                if "warning" not in value.lower():
                    self.command_out.AppendText(value + "\n")
            self.command_out.AppendText("'openssl rand -engine tpm2tss -base64 " + str(no_bytes) + "' executed \n")
            self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        else:
            self.command_out.AppendText("You need to select the rng output type.\n")


class Tab3Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="OpenSSL Engine", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        main_menu_font = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)

        # Instantiate all objects
        tab_base = wx.Notebook(self, id=wx.ID_ANY, style=wx.NB_TOP)
        self.tab1_rsa_cs = Tab_RSA_CS(tab_base)
        self.tab2_ecc_cs = Tab_ECC_CS(tab_base)
        tab3_rsa_misc = Tab_RSA_MISC(tab_base)
        tab4_rng = Tab_RNG(tab_base)

        # Add tabs
        tab_base.AddPage(self.tab1_rsa_cs, 'RSA (Client/Server)')
        tab_base.AddPage(self.tab2_ecc_cs, 'ECC (Client/Server)')
        tab_base.AddPage(tab3_rsa_misc, 'RSA (Enc/Dec/Sign/Verify)')
        tab_base.AddPage(tab4_rng, 'RNG')

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Show(True)

    def OnCloseWindow(self, evt):
        #checkProcesses()
        self.tab2_ecc_cs.Destroy()
        self.tab1_rsa_cs.Destroy()
        self.Parent.Show()
        self.Destroy()
