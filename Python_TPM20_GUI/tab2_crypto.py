import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import images as img
from binascii import unhexlify
""" NOTE: All the tpm2_evictcontrol commands, the context is hardcoded. Also, all the files created are fixed in their naming.
Thus if not removed from persistent store, the newly created key will be 'lost',
as the old one still resides at the same context. To fix this, the context value will have to be cleared in tab1, context management.
It may be possible to implement a dynamic context, i.e. whenever a new key is created,
it will be assigned another free context value.
"""


class Tab_Hash(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # create UI elements
        hashbutton = wx.Button(self, -1, 'Hash (SHA-2)', size = (-1, 47))
        inputtext = wx.StaticText(self, -1, label="Input:")
        self.input_display = wx.TextCtrl(self,value="12345")
        self.command_display = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.command_display.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        # ~clearbutton = wx.BitmapButton(self, -1, img.clear.getBitmap())
        
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the objects to the sizers
        mainsizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(self.command_display, 1, wx.EXPAND | wx.ALL, 0)
        input_sizer.Add(inputtext, 0, wx.ALIGN_CENTRE, 5)
        input_sizer.Add(self.input_display, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        input_sizer.Add(hashbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        input_sizer.Add(clearbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        input_sizer.Add(backbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        # create tooltips
        hashbutton.SetToolTip(wx.ToolTip("TPM2_Hash: Hash the value using SHA-256 algorithm."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # bind events
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, hashbutton)
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)
        self.SetSizer(mainsizer)

    def OnButtonClick(self, evt):
        input_message = self.input_display.GetValue()
        if (input_message == ""):
            self.command_display.AppendText("Hash data cannot be left empty.\n")
            return
        input_message_hex = exec_cmd.convertInputToHex(input_message, 64)
        print(input_message_hex) 
        if (input_message_hex == 0):
            self.command_display.AppendText("Input must be in HEX please. \n")
            return
        data_file = open("data_for_hash.data", "wb")
        data_file.write(unhexlify(input_message_hex))
        data_file.close()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_hash",
            "-C", "o",
            "-g", "sha256",
            "-o", "hash.data",
            "-t", "ticketfile",
            "data_for_hash.data"
        ])
        #self.command_display.Clear()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "xxd", "hash.data",
        ]) 

        self.command_display.AppendText(str(output_message) + "\n")
        self.command_display.AppendText("Hashing it...\nExecuting: tpm2_hash -C o -g sha256 -o hash.data -t ticketfile data_for_hash.data\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnClear(self, evt):
        self.command_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)


class Tab_RSA(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # create UI elements
        createprimary = wx.Button(self, -1, 'Create Primary', size=(-1, 48))
        createkeypairbutton = wx.Button(self, -1, 'Create RSA Keypair', size=(-1, 48))
        encbutton = wx.Button(self, -1, 'RSA Encrypt', size=(-1, 48))
        decbutton = wx.Button(self, -1, 'RSA Decrypt', size=(-1, 48))
        signbutton = wx.Button(self, -1, 'RSA Sign', size=(-1, 48))
        opensslverifybutton = wx.Button(self, -1, 'RSA Verify\n(By OpenSSL)')
        tpmverifybutton = wx.Button(self, -1, 'RSA Verify\n(By TPM2-Tools)')
        inputtext = wx.StaticText(self, -1, label="Data Input: ")
        self.input_display = wx.TextCtrl(self,value="168168")
        self.command_display = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.command_display.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        # ~clearbutton = wx.BitmapButton(self, -1, img.clear.getBitmap())
        
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the objects to the sizers
        mainsizer.AddSpacer(10)
        mainsizer.Add(input_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        mainsizer.AddSpacer(5)
        mainsizer.Add(button_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        mainsizer.Add(self.command_display, 1, wx.EXPAND | wx.TOP, 5)
        input_sizer.Add(inputtext, 0, wx.ALIGN_CENTRE, 5)
        input_sizer.Add(self.input_display, 1, wx.ALIGN_CENTRE, 0)
        # ~ button_sizer.Add(createprimary, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(createkeypairbutton, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(encbutton, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(decbutton, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(signbutton, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(opensslverifybutton, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(tpmverifybutton, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        
        button_sizer.Add(createprimary, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        button_sizer.Add(createkeypairbutton, 1, wx.ALIGN_CENTRE  | wx.ALL, 5)
        button_sizer.Add(encbutton, 1, wx.ALIGN_CENTRE  | wx.ALL, 5)
        button_sizer.Add(decbutton, 1, wx.ALIGN_CENTRE  | wx.ALL, 5)
        button_sizer.Add(signbutton, 1, wx.ALIGN_CENTRE  | wx.ALL, 5)
        button_sizer.Add(opensslverifybutton, 1, wx.ALIGN_CENTRE  | wx.ALL, 5)
        button_sizer.Add(tpmverifybutton, 1, wx.ALIGN_CENTRE  | wx.ALL, 5)

        button_sizer.Add(clearbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        button_sizer.Add(backbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        # set colours for UI elements
#         createkeypairbutton.SetBackgroundColour((255, 92, 51))
#         encbutton.SetBackgroundColour((255, 153, 0))
#         decbutton.SetBackgroundColour((255, 255, 0))
#         signbutton.SetBackgroundColour((255, 204, 255))
#         opensslverifybutton.SetBackgroundColour((0, 204, 255))
#         tpmverifybutton.SetBackgroundColour((0, 204, 102))

        # create tooltips
        createprimary.SetToolTip(wx.ToolTip("TPM2_CreatePrimary: Create a Primary Key Pair under the Owner Authorisation. Handle = 0x81000004"))
        createkeypairbutton.SetToolTip(wx.ToolTip("TPM2_Create: Create a RSA Key Pair under the Primary key (that you should have generated already). Handle = 0x81000005"))
        encbutton.SetToolTip(wx.ToolTip("TPM2_RSAEncrypt: Encrypt data input using the RSA public key"))
        decbutton.SetToolTip(wx.ToolTip("TPM2_RSADecrypt: Decrypt data using the RSA private key"))
        signbutton.SetToolTip(wx.ToolTip("TPM2_Sign: Sign the data input with the private key"))
        opensslverifybutton.SetToolTip(wx.ToolTip("Using OpenSSL, verify the signature with the public key"))
        tpmverifybutton.SetToolTip(wx.ToolTip("TPM2_VerifySignature: Using the TPM, verify the signature with the public key"))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # bind events
        self.Bind(wx.EVT_BUTTON, self.OnCreatePrimary2, createprimary)
        self.Bind(wx.EVT_BUTTON, self.OnCreateKeyPair2, createkeypairbutton)
        self.Bind(wx.EVT_BUTTON, self.OnEnc, encbutton)
        self.Bind(wx.EVT_BUTTON, self.OnDec, decbutton)
        self.Bind(wx.EVT_BUTTON, self.OnSign1, signbutton)
        self.Bind(wx.EVT_BUTTON, self.OnVerifySSL, opensslverifybutton)
        self.Bind(wx.EVT_BUTTON, self.OnVerifyTPM1, tpmverifybutton)
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)
        self.SetSizer(mainsizer)

    def OnCreatePrimary2(self, evt):
        if (misc.OwnerDlg(self, "Enter Owner Authorisation").ShowModal() == -1):
            return
        self.OnCreatePrimary1()
    
    def OnCreatePrimary1(self):
        self.command_display.AppendText("Creating RSA Primary Key (may take a while)...\n")
        wx.CallLater(150, self.OnCreatePrimary)
    
    # note: this function/command runs for quite a while as compared to ECC.
    def OnCreatePrimary(self):
        exec_cmd.execTpmToolsAndCheck(["rm", "RSAprimary.ctx"])
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_createprimary",
            "-C", "o",
            "-P", exec_cmd.ownerAuth,
            "-g", "sha256",
            "-G", "rsa",
            "-c", "RSAprimary.ctx"
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_evictcontrol",
            "-C", "o",
            "-c", "RSAprimary.ctx",
            "-P", exec_cmd.ownerAuth,
            "0x81000004",
        ])
        self.command_display.AppendText(str(output_message) + "\n")
        self.command_display.AppendText("tpm2_createprimary -C o -P " + exec_cmd.ownerAuth + " -g sha256 -G rsa -c RSAprimary.ctx\n")
        self.command_display.AppendText("tpm2_evictcontrol -C o -c RSAprimary.ctx -P " + exec_cmd.ownerAuth + " 0x81000004\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnCreateKeyPair2(self, evt):
        if (misc.OwnerDlg(self, "Enter Owner Authorisation").ShowModal() == -1):
            return
        self.OnCreateKeyPair1()
    
    def OnCreateKeyPair1(self):
        self.command_display.AppendText("Creating RSA Key Pair... \n")
        wx.CallLater(150, self.OnCreateKeyPair)
    
    def OnCreateKeyPair(self):
        exec_cmd.execTpmToolsAndCheck(["rm", "RSAkeycontext.ctx"])
        exec_cmd.execTpmToolsAndCheck(["rm", "RSAPriv.key"])
        exec_cmd.execTpmToolsAndCheck(["rm", "RSAPub.key"])
        exec_cmd.execTpmToolsAndCheck(["rm", "RSAkey_name_structure.data"])
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_create",
            "-C", "0x81000004",
            "-p", "RSAleaf123",
            "-g", "sha256",
            "-G", "rsa",
            "-r", "RSAPriv.key",
            "-u", "RSAPub.key",
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_load",
            "-C", "0x81000004",
            "-u", "RSAPub.key",
            "-r", "RSAPriv.key",
            "-n", "RSAkey_name_structure.data",
            "-c", "RSAkeycontext.ctx",
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_evictcontrol",
            "-C", "o",
            "-c", "RSAkeycontext.ctx",
            "-P", exec_cmd.ownerAuth,
            "0x81000005",
        ])
        self.command_display.AppendText(str(output_message) + "\n")
        self.command_display.AppendText("tpm2_create -C 0x81000004 -g sha256 -G rsa -r RSAPriv.key -u RSAPub.key\n")
        self.command_display.AppendText("tpm2_load -C 0x81000004 -u RSAPub.key -r RSAPriv.key -n RSAkey_name_structure.data -c RSAkeycontext.ctx\n")
        self.command_display.AppendText("tpm2_evictcontrol -a o -c RSAkeycontext.ctx -p 0x81000005 -P " + exec_cmd.ownerAuth + "\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnEnc(self, evt):
        exec_cmd.execTpmToolsAndCheck(["rm", "data_encrypted.txt"])
        input_message = self.input_display.GetValue()
        if (input_message == ""):
            self.command_display.AppendText("Input cannot be left empty.\n")
            return
        data_file = open("datain.txt", "w")
        data_file.write(input_message)
        data_file.close()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_rsaencrypt",
            "-c", "0x81000005",
            "-o", "data_encrypted.txt",
            "datain.txt"
        ])
        self.command_display.AppendText(str(output_message) + "\n")
        self.command_display.AppendText("tpm2_rsaencrypt -c 0x81000005 -o data_encrypted.txt datain.txt\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnDec(self, evt):
        exec_cmd.execTpmToolsAndCheck(["rm", "dataout.txt"])
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_rsadecrypt",
            "-c", "0x81000005",
            "-p", "RSAleaf123",
            "-o", "dataout.txt",
            "data_encrypted.txt",
        ])
        data_file = open("dataout.txt", "r")
        data_out = data_file.read()
        data_file.close()
        self.command_display.AppendText(str(output_message))
        self.command_display.AppendText("Your message is:\n" + str(data_out) + "\n")
        self.Update()
        self.command_display.AppendText("tpm2_rsadecrypt -c 0x81000005 -p RSAleaf123 -o dataout.txt data_encrypted.txt\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnSign1(self, evt):
        self.command_display.AppendText("Signing Data Input with RSA Private Key... \n")
        wx.CallLater(10, self.OnSign)
    
    def OnSign(self):
        exec_cmd.execTpmToolsAndCheck(["rm", "hash.bin"])
        exec_cmd.execTpmToolsAndCheck(["rm", "ticket.bin"])
        exec_cmd.execTpmToolsAndCheck(["rm", "signature_blob"])
        exec_cmd.execTpmToolsAndCheck(["rm", "signature_data"])
        
        input_message = self.input_display.GetValue()
        if (input_message == ""):
            self.command_display.AppendText("Input cannot be left empty.\n")
            return
        data_file = open("datain.txt", "w")
        data_file.write(input_message)
        data_file.close()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_hash",
            "-C", "o",
            "-g", "sha256",
            "-o", "hash.bin",
            "-t", "ticket.bin",
            "datain.txt"
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_sign",
            "-c", "0x81000005",
            "-p", "RSAleaf123",
            "-g", "sha256",
            "-o", "signature_blob",
            "-t", "ticket.bin",
            "datain.txt",
        ])
        self.command_display.AppendText(str(output_message) + "\n")
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_sign",
            "-c", "0x81000005",
            "-p", "RSAleaf123",
            "-g", "sha256",
            "-o", "signature_data",
            "-f", "plain",
            "datain.txt",
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()        
        
        self.command_display.AppendText("tpm2_hash -C o -g 0x00B -o hash.bin -t ticket.bin datain.txt\n")
        self.command_display.AppendText("tpm2_sign -c 0x81000005 -p RSAleaf123 -g sha256 -o signature_blob -t ticket.bin  datain.txt\n")
        self.command_display.AppendText("tpm2_sign -c 0x81000005 -p RSAleaf123 -g sha256 -o signature_data -f plain datain.txt\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnVerifySSL(self, evt):
        exec_cmd.execTpmToolsAndCheck(["rm", "RSAkey.pem"])
        #exec_cmd.execTpmToolsAndCheck(["rm", "signature_data"])

        input_message = self.input_display.GetValue()
        if (input_message == ""):
            self.command_display.AppendText("Input cannot be left empty.\n")
            return
        data_file = open("datain.txt", "w")
        data_file.write(input_message)
        data_file.close()
        
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_readpublic",
            "-c", "0x81000005",
            "-f", "pem",
            "-o", "RSAkey.pem"
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()

        output_message = exec_cmd.execTpmToolsAndCheck([
            "openssl", "rsa",
            "-in", "RSAkey.pem",
            "-pubin",
            "-noout",
            "-text"
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "openssl", "dgst",
            "-verify", "RSAkey.pem",
            "-keyform", "pem",
            "-sha256",
            "-signature", "signature_data",
            "datain.txt"
        ])
        self.command_display.AppendText(str(output_message) + "\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnVerifyTPM1(self, evt):
        self.command_display.AppendText("Verifying signature using RSA Public Key... \n")
        wx.CallLater(10, self.OnVerifyTPM)
    
    def OnVerifyTPM(self):
        exec_cmd.execTpmToolsAndCheck(["rm", "RSAverifyleaf.ctx"])
 
        input_message = self.input_display.GetValue()
        if (input_message == ""):
            self.command_display.AppendText("Input cannot be left empty.\n")
            return
        data_file = open("datain.txt", "w")
        data_file.write(input_message)
        data_file.close()
                
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_loadexternal",
            "-C", "o",
            "-u", "RSAPub.key",
            "-c", "RSAverifyleaf.ctx"
        ])
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_verifysignature",
            "-c", "RSAverifyleaf.ctx",
            "-g", "sha256",
            "-m", "datain.txt",
            "-s", "signature_blob",
            "-t", "ticket.bin"
        ])
        self.command_display.AppendText("tpm2_loadexternal -C o -u RSAPub.key -c RSAverifyleaf.ctx\n")
        self.command_display.AppendText("tpm2_verifysignature -c RSAverifyleaf.ctx -g sha256 -m datain.txt -s signature_blob -t ticket.bin\n")
        self.command_display.AppendText(str(output_message) + "\nVerification Successful Unless Error Message Is Shown\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnClear(self, evt):
        self.command_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)


class Tab_ECC(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # create UI elements
        createprimary = wx.Button(self, -1, 'Create Primary', size = (-1, 48))
        createkeypairbutton = wx.Button(self, -1, 'Create ECC Keypair', size =(-1, 48))
        signbutton = wx.Button(self, -1, 'ECC Sign', size = (-1, 48))
        opensslverifybutton = wx.Button(self, -1, 'ECC Verify\n(By Openssl)')
        tpmverifybutton = wx.Button(self, -1, 'ECC Verify\n(By TPM2-Tools)')
        inputtext = wx.StaticText(self, -1, label="Data Input: ")
        self.input_display = wx.TextCtrl(self,value="138831")
        self.command_display = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.command_display.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        # ~clearbutton = wx.BitmapButton(self, -1, img.clear.getBitmap())

        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the objects to the sizers
        mainsizer.AddSpacer(10)
        mainsizer.Add(input_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        mainsizer.AddSpacer(5)
        mainsizer.Add(button_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        mainsizer.Add(self.command_display, 1, wx.EXPAND | wx.TOP, 5)
        input_sizer.Add(inputtext, 0, wx.ALIGN_CENTRE, 5)
        input_sizer.Add(self.input_display, 1, wx.ALIGN_CENTRE, 0)
        button_sizer.Add(createprimary, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        button_sizer.Add(createkeypairbutton, 1, wx.ALIGN_CENTRE  | wx.ALL, 5)
        button_sizer.Add(signbutton, 1, wx.ALIGN_CENTRE  | wx.ALL, 5)
        button_sizer.Add(opensslverifybutton, 1, wx.ALIGN_CENTRE  | wx.ALL, 5)
        button_sizer.Add(tpmverifybutton, 1, wx.ALIGN_CENTRE  | wx.ALL, 5)
        button_sizer.Add(clearbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        button_sizer.Add(backbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        # ~ button_sizer.Add(createprimary, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(createkeypairbutton, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(signbutton, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(opensslverifybutton, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(tpmverifybutton, 1, wx.ALIGN_CENTRE | wx.EXPAND | wx.ALL, 5)
        # ~ button_sizer.Add(clearbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        # ~ button_sizer.Add(backbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 5)


        # set colours for UI elements
#         createkeypairbutton.SetBackgroundColour((255, 153, 204))
#         signbutton.SetBackgroundColour((204, 255, 204))
#         openssdlverifybutton.SetBackgroundColour((102, 255, 255))
#         tpmverifybutton.SetBackgroundColour((204, 255, 51))

        # create tooltips
        createprimary.SetToolTip(wx.ToolTip("TPM2_CreatePrimary: Create a Primary Key Pair under the Owner Authorisation. Handle = 0x81000006"))
        createkeypairbutton.SetToolTip(wx.ToolTip("TPM2_Create: Create an ECC Key Pair under the Primary key (that you should have generated already). Handle = 0x81000007"))
        signbutton.SetToolTip(wx.ToolTip("TPM2_Sign: Sign the data input with the private key"))
        opensslverifybutton.SetToolTip(wx.ToolTip("Using OpenSSL, verify the signature with the public key"))
        tpmverifybutton.SetToolTip(wx.ToolTip("TPM2_VerifySignature: Using the TPM, verify the signature with the public key"))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # bind events
        self.Bind(wx.EVT_BUTTON, self.OnCreatePrimary2, createprimary)
        self.Bind(wx.EVT_BUTTON, self.OnCreateKeyPair2, createkeypairbutton)
        self.Bind(wx.EVT_BUTTON, self.OnSign1, signbutton)
        self.Bind(wx.EVT_BUTTON, self.OnVerifySSL1, opensslverifybutton)
        self.Bind(wx.EVT_BUTTON, self.OnVerifyTPM1, tpmverifybutton)
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)
        self.SetSizer(mainsizer)

    def OnCreatePrimary2(self, evt):
        if (misc.OwnerDlg(self, "Enter Owner Authorisation").ShowModal() == -1):
            return
        self.OnCreatePrimary1()
    
    def OnCreatePrimary1(self):
        self.command_display.AppendText("Creating ECC Primary Key... \n")
        wx.CallLater(150, self.OnCreatePrimary)
    
    def OnCreatePrimary(self):
        exec_cmd.execTpmToolsAndCheck(["rm", "ECCprimary.ctx"])
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_createprimary",
            "-C", "o",
            "-P", exec_cmd.ownerAuth,
            "-g", "sha256",
            "-G", "ecc",
            "-c", "ECCprimary.ctx"
        ])
        
        self.command_display.AppendText(str(output_message))
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_evictcontrol",
            "-C", "o",
            "-c", "ECCprimary.ctx",
            "-P", exec_cmd.ownerAuth,
            "0x81000006"
        ])
        self.command_display.AppendText(str(output_message) + "\n")
        self.command_display.AppendText("tpm2_createprimary -C o -P " + exec_cmd.ownerAuth + " -g sha256 -G 0x0023 -c ECCprimary.ctx\n")
        self.command_display.AppendText("tpm2_evictcontrol -C o -c ECCprimary.ctx -p 0x81000006 -P " + exec_cmd.ownerAuth + "\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnCreateKeyPair2(self, evt):
        if (misc.OwnerDlg(self, "Enter Owner Authorisation").ShowModal() == -1):
            return
        self.OnCreateKeyPair1()
    
    def OnCreateKeyPair1(self):
        self.command_display.AppendText("Creating ECC Key Pair... \n")
        wx.CallLater(150, self.OnCreateKeyPair)
    
    def OnCreateKeyPair(self):
        exec_cmd.execTpmToolsAndCheck(["rm", "ECCkeycontext.ctx"])
        exec_cmd.execTpmToolsAndCheck(["rm", "ECCpri.key"])
        exec_cmd.execTpmToolsAndCheck(["rm", "ECCpub.key"])
        exec_cmd.execTpmToolsAndCheck(["rm", "ECCname.data"])
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_create",
            "-C", "0x81000006",
            "-p", "ECCleaf123",
            "-g", "sha256",
            "-G", "ecc",
            "-r", "ECCpri.key",
            "-u", "ECCpub.key"
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_load",
            "-C", "0x81000006",
            "-u", "ECCpub.key",
            "-r", "ECCpri.key",
            "-n", "ECCname.data",
            "-c", "ECCkeycontext.ctx"
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_evictcontrol",
            "-C", "o",
            "-c", "ECCkeycontext.ctx",
            "-P", exec_cmd.ownerAuth,
            "0x81000007",
        ])
        self.command_display.AppendText(str(output_message) + "\n")
        self.command_display.AppendText("tpm2_create -C 0x81000006 -p ECCleaf123 -g sha256 -G ecc -r ECCpri.key -u ECCpub.key\n")
        self.command_display.AppendText("tpm2_load -C 0x81000006 -u ECCpub.key -r ECCpri.key -n ECCname.data -c ECCkeycontext.ctx\n")
        self.command_display.AppendText("tpm2_evictcontrol -C o -c ECCkeycontext.ctx -P " + exec_cmd.ownerAuth + " 0x81000007\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnSign1(self, evt):
        self.command_display.AppendText("Signing Data with ECC Private Key... \n")
        wx.CallLater(10, self.OnSign)
    
    def OnSign(self):
        exec_cmd.execTpmToolsAndCheck(["rm", "secret.data"])
        exec_cmd.execTpmToolsAndCheck(["rm", "signature_data"])
        exec_cmd.execTpmToolsAndCheck(["rm", "signature_blob"])
        input_message = self.input_display.GetValue()
        if (input_message == ""):
            self.command_display.AppendText("Input cannot be left empty.\n")
            return
        data_file = open("secret.data", "w")
        data_file.write(input_message)
        data_file.close()
        self.command_display.AppendText("Signing using ECC key, with SHA256 algo...\n")
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_sign",
            "-c", "0x81000007",
            "-p", "ECCleaf123",
            "-g", "sha256",
            "-o", "signature_data",
            "-f", "plain",
            "secret.data",
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_sign",
            "-c", "0x81000007",
            "-p", "ECCleaf123",
            "-g", "sha256",
            "-o", "signature_blob",
            "secret.data",
        ])
        self.command_display.AppendText(str(output_message) + "\n")
        self.Update()
        self.command_display.AppendText("tpm2_sign -c 0x81000007 -p ECCleaf123 -g sha256 -o signature_data -f plain secret.data\n")
        self.command_display.AppendText("tpm2_sign -c 0x81000007 -p ECCleaf123 -g sha256 -o signature_blob secret.data\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnVerifySSL1(self, evt):
        self.command_display.AppendText("Verifying Data with ECC Public Key using Openssl... \n")
        wx.CallLater(10, self.OnVerifySSL)
    
    def OnVerifySSL(self):
        exec_cmd.execTpmToolsAndCheck(["rm", "ECCkey.pem"])
        input_message = self.input_display.GetValue()
        if (input_message == ""):
            self.command_display.AppendText("Input cannot be left empty.\n")
            return
        data_file = open("secret.data", "w")
        data_file.write(input_message)
        data_file.close()        
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_readpublic",
            "-c", "0x81000007",
            "-f", "pem",
            "-o", "ECCkey.pem"
        ])
        self.command_display.AppendText(str(output_message))
        self.Update()
        output_message = exec_cmd.execTpmToolsAndCheck([
            "openssl", "dgst",
            "-verify", "ECCkey.pem",
            "-keyform", "pem",
            "-sha256",
            "-signature", "signature_data",
            "secret.data"
        ])
        self.command_display.AppendText(str(output_message) + "\n")
        self.Update()
        self.command_display.AppendText("tpm2_readpublic -c 0x81000007 -f pem -o ECCkey.pem\n")
        self.command_display.AppendText("openssl dgst -verify ECCkey.pem -keyform pem -sha256 -signature signature_data secret.data\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnVerifyTPM1(self, evt):
        self.command_display.AppendText("Verifying Data with ECC Public Key using TPM2-Tools...\n")
        wx.CallLater(10, self.OnVerifyTPM)
    
    def OnVerifyTPM(self):
        exec_cmd.execTpmToolsAndCheck(["rm", "ECCverifyleaf.ctx"])
        input_message = self.input_display.GetValue()
        if (input_message == ""):
            self.command_display.AppendText("Input cannot be left empty.\n")
            return
        data_file = open("secret.data", "w")
        data_file.write(input_message)
        data_file.close()        
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_loadexternal",
            "-C", "o",
            "-u", "ECCpub.key",
            "-c", "ECCverifyleaf.ctx"
        ])
        output_message = exec_cmd.execTpmToolsAndCheck([
            "tpm2_verifysignature",
            "-c", "ECCverifyleaf.ctx",
            "-g", "sha256",
            "-m", "secret.data",
            "-s", "signature_blob"
        ])
        self.command_display.AppendText("tpm2_loadexternal -C o -u ECCpub.key -c ECCverifyleaf.ctx\n")
        self.command_display.AppendText("tpm2_verifysignature -c ECCverifyleaf.ctx -g sha256 -m secret.data -s signature_blob\n")
        self.command_display.AppendText(str(output_message) + "\nVerification Successful Unless Error Message Is Shown\n")
        self.command_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnClear(self, evt):
        self.command_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)


class Tab2Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="Cryptographic Functions", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        main_menu_font = wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Instantiate all objects
        tab_base = wx.Notebook(self, id=wx.ID_ANY, style=wx.NB_TOP)
        tab1_hash = Tab_Hash(tab_base)
        tab2_rsa = Tab_RSA(tab_base)
        tab3_ecc = Tab_ECC(tab_base)

        # Add tabs
        tab_base.AddPage(tab1_hash, 'Hash')
        tab_base.AddPage(tab2_rsa, 'RSA')
        tab_base.AddPage(tab3_ecc, 'ECC')

        self.Show(True)

    def OnCloseWindow(self, evt):
        self.Parent.Show()
        self.Destroy()
