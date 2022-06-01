import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import info_dialogs as info
import images as img
pcr_index_list = [str(value) for value in range(0, 24)]


class Tab5Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="Attestation", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        self.SetBackgroundColour(wx.WHITE)
        main_menu_font = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        column_sizer = wx.BoxSizer(wx.HORIZONTAL)
        output_and_settings_sizer = wx.BoxSizer(wx.HORIZONTAL)
        settings_sizer = wx.BoxSizer(wx.VERTICAL)
        first_column = wx.BoxSizer(wx.VERTICAL)
        ak_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ek_sizer = wx.BoxSizer(wx.HORIZONTAL)
        list_persist_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pcr_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mini_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        nonce_sizer = wx.BoxSizer(wx.HORIZONTAL)
        second_column = wx.BoxSizer(wx.VERTICAL)
        third_column = wx.BoxSizer(wx.VERTICAL)

        # instantiate the objects
        pcr_bank_blurb = wx.StaticText(self, -1, "PCR 256 Index: ")
        self.pcr_bank_choice = wx.ComboBox(self, -1, "Pick the PCR Index", choices=pcr_index_list, style=wx.CB_READONLY)
        nonce_blurb = wx.StaticText(self, -1, "Nonce (Even no of hex char/digits): ")
        self.nonce_input = wx.TextCtrl(self, -1)
        ek_blurb = wx.StaticText(self, -1, "EK Handle: 0x81010001")
        ak_blurb = wx.StaticText(self, -1, "AK/EK handle: ")
        settings_blurb = wx.StaticText(self, -1, "Settings: ")
        settings_blurb.SetFont(wx.Font(20, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.ak_handle_input = wx.TextCtrl(self, -1)
        button_gen_ek = wx.Button(self, -1, 'Generate EK, if not created yet', size = (350, -1))
        button_gen_ak = wx.Button(self, -1, 'Generate AK from EK', size = (350 ,48))
        button_gen_quote = wx.Button(self, -1, 'Generate Quote', size = (350, 48))
        button_evictak = wx.Button(self, -1, 'Evict AK/EK handle')
#         button_verify_quote_ssl = wx.Button(self, -1, 'Step 3: Verify Quote (OpenSSL)')
        button_verify_quote_tpm = wx.Button(self, -1, 'Verify Quote (By TPM2-Tools)', size = (350, 48))
        self.command_out = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.command_out.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        button_listpersist = wx.Button(self, -1, 'List Persistent', size = (270, -1))
        # server logo
        server_image = wx.Image('../images/server.png', wx.BITMAP_TYPE_PNG)
        server_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(server_image))
        # ~server_image = wx.StaticBitmap(self, wx.ID_ANY, img.server.getBitmap())

        # TPM Image
        tpm_image = wx.Image('../images/tpm_slb_9670.png', wx.BITMAP_TYPE_PNG)
        tpm_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tpm_image))
        # ~tpm_image = wx.StaticBitmap(self, wx.ID_ANY, img.tpm_slb_9670.getBitmap())

        # Clear icon
        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        button_clear = wx.BitmapButton(self, -1, clearimage)
        # ~button_clear = wx.BitmapButton(self, -1, img.clear.getBitmap())
        
        # attest combined image
        combimage = wx.Image('../images/attest_comb.png', wx.BITMAP_TYPE_PNG)
        combimage = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(combimage))
        # ~combimage = wx.StaticBitmap(self, wx.ID_ANY, img.attest_comb.getBitmap())

        # info image button
        infoimage = wx.Image('../images/info.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        infobutton = wx.BitmapButton(self, -1, infoimage)
        # ~infobutton = wx.BitmapButton(self, -1, img.info.getBitmap())
        
        # back image
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the sizers to the main sizer
        mainsizer.Add(column_sizer, 0, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(output_and_settings_sizer, 1, wx.EXPAND | wx.ALL, 0)
        output_and_settings_sizer.Add(settings_sizer, 0, wx.EXPAND | wx.ALL, 5)
        output_and_settings_sizer.Add(self.command_out, 1, wx.EXPAND | wx.ALL, 5)
        column_sizer.Add(first_column, 1, wx.EXPAND | wx.ALL, 5)
        column_sizer.Add(second_column, 1, wx.EXPAND | wx.ALL, 5)
        column_sizer.Add(third_column, 1, wx.EXPAND | wx.ALL, 5)

        # attach the ui elements to the internal sizer
        first_column.Add((5, 42))
        first_column.Add(server_image, 0, wx.EXPAND | wx.ALL, 10)
#         first_column.Add(button_verify_quote_ssl, 0, wx.EXPAND | wx.ALL, 5)
        first_column.Add(button_verify_quote_tpm, 0, wx.CENTRE | wx.ALL, 5)
        second_column.AddSpacer(50)
        second_column.Add(combimage, 0, wx.CENTRE)
        third_column.Add(button_gen_ak, 0, wx.CENTRE| wx.TOP, 5)
        third_column.Add((5, 5))
        third_column.Add(tpm_image, 0, wx.EXPAND | wx.ALL, 5)
        third_column.Add((5, 5))
        third_column.Add(button_gen_quote, 0, wx.CENTRE | wx.TOP, 5)

        # settings sizer
        settings_sizer.Add(settings_blurb, 0, wx.EXPAND | wx.ALL, 5)
        settings_sizer.Add(pcr_sizer, 0, wx.EXPAND | wx.ALL, 5)
        pcr_sizer.Add(pcr_bank_blurb, 0, wx.ALIGN_CENTRE | wx.LEFT, 0)
        pcr_sizer.Add(self.pcr_bank_choice, 0, wx.EXPAND | wx.ALL, 5)
        settings_sizer.Add(nonce_sizer, 0, wx.EXPAND | wx.ALL, 0)
        nonce_sizer.Add(nonce_blurb, 0, wx.ALIGN_CENTRE | wx.LEFT, 5)
        nonce_sizer.Add(self.nonce_input, 0, wx.EXPAND | wx.ALL, 5)
        settings_sizer.Add(ek_sizer, 0, wx.EXPAND | wx.TOP, 10)
        ek_sizer.Add(ek_blurb, 0, wx.ALIGN_CENTRE | wx.LEFT, 5)
        ek_sizer.Add(button_gen_ek, 0, wx.EXPAND | wx.LEFT, 15)
        settings_sizer.Add(ak_sizer, 0, wx.EXPAND | wx.TOP, 10)
        ak_sizer.Add(ak_blurb, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.TOP, 5)
        ak_sizer.Add(self.ak_handle_input, 1, wx.EXPAND | wx.ALL, 5)
        ak_sizer.Add(button_evictak, 1, wx.EXPAND | wx.ALL, 5)

        settings_sizer.Add(list_persist_sizer, 0, wx.EXPAND | wx.TOP, 5)
        list_persist_sizer.Add(button_listpersist, 0, wx.EXPAND | wx.LEFT | wx.TOP, 5)

        settings_sizer.AddSpacer(55)
        settings_sizer.Add(mini_button_sizer, 1, wx.EXPAND | wx.ALL, 0)
        mini_button_sizer.Add(button_clear, 0, wx.ALL, 5)
        mini_button_sizer.Add(infobutton, 0, wx.ALL, 5)
        mini_button_sizer.Add(backbutton, 0, wx.ALL, 5)

        # Set tooltips
        button_gen_ak.SetToolTip(wx.ToolTip("TPM2_GenEK/GenAK: Generate an Endorsement Key Pair, and then the Attestation Key Pair from it."))
        button_gen_quote.SetToolTip(wx.ToolTip("TPM2_Quote: Generate a quote of a PCR index, signed by the TPM's Attestation Key."))
#         button_verify_quote_ssl.SetToolTip(wx.ToolTip("Verify the quote using OpenSSL and the Attestation Public Key."))
        button_verify_quote_tpm.SetToolTip(wx.ToolTip("TPM2_CheckQuote: Verify the quote using TPM functions."))
        button_clear.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # declare and bind events
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnClear, button_clear)
        self.Bind(wx.EVT_BUTTON, self.OnInfo, infobutton)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, backbutton)
        self.Bind(wx.EVT_BUTTON, self.OnGenEK, button_gen_ek)
        self.Bind(wx.EVT_BUTTON, self.OnGenAK2, button_gen_ak)
        self.Bind(wx.EVT_BUTTON, self.OnEvict, button_evictak)
        self.Bind(wx.EVT_BUTTON, self.OnGenQuote1, button_gen_quote)
#         self.Bind(wx.EVT_BUTTON, self.OnVerifyQSSL, button_verify_quote_ssl)
        self.Bind(wx.EVT_BUTTON, self.OnVerifyQTPM, button_verify_quote_tpm)
        self.Bind(wx.EVT_BUTTON, self.OnListPersist, button_listpersist)

        self.ak_handle_input.write("0x81010002")
        self.pcr_bank_choice.SetSelection(5)
        self.nonce_input.write("aaaaaa")
        self.SetSizer(mainsizer)
        self.Show(True)

    def OnListPersist(self, evt):
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_getcap",
            "handles-persistent",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("\n")
        self.command_out.AppendText("'tpm2_getcap handles-persistent\n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")


    def OnGenEK(self, evt):
        if (misc.OwnerDlg(self, "Enter Owner Authorisation").ShowModal() == -1):
            return
        if (misc.EndorseDlg(self, "Enter Endorsement Authorisation").ShowModal() == -1):
            return
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_createek",
            "-P", exec_cmd.endorseAuth,
            "-w", exec_cmd.ownerAuth,
            "-c", "0x81010001",
            "-G", "rsa",
            "-u", "ek.pub",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("\n")
        self.command_out.AppendText("'tpm2_createek -P " + exec_cmd.endorseAuth + " -w " + exec_cmd.ownerAuth + " -c 0x81010001 -G rsa -u ek.pub' executed \n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnGenAK2(self, evt):
        if (misc.OwnerDlg(self, "Enter Owner Authorisation").ShowModal() == -1):
            return
        if (misc.EndorseDlg(self, "Enter Endorsement Authorisation").ShowModal() == -1):
            return
        self.OnGenAK1()
    
    def OnGenAK1(self):
        self.command_out.AppendText("Generating Attestation Key Pair... \n")
        wx.CallLater(150, self.OnGenAK)
    
    def OnGenAK(self):
        specific_handle = self.ak_handle_input.GetValue()
        exec_cmd.execCLI(["rm", "ak*", ])
        exec_cmd.execCLI(["rm", "ek*", ])
        exec_cmd.execCLI(["rm", "quote_sign_data", ])
        exec_cmd.execCLI(["rm", "tpmquote.data", ])
#         if (misc.OwnerDlg(self, "Enter Owner Authorisation").ShowModal() == -1):
#             return
#         if (misc.EndorseDlg(self, "Enter Endorsement Authorisation").ShowModal() == -1):
#             return
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_createak",
            "-P", exec_cmd.endorseAuth,
            #~ "-w", exec_cmd.ownerAuth,
            "-C", "0x81010001",
            "-G", "rsa",
            "-u", "ak_pub.bin",
            "-n", "ak.name",
            "-c", "ak.ctx",
        ])
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_evictcontrol",
            "-C", "o",
            "-P", exec_cmd.ownerAuth,
            "-c", "ak.ctx",
            specific_handle
        ])


        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("\n")
        self.command_out.AppendText("'tpm2_createak -P " + exec_cmd.endorseAuth + " -C 0x81010001 -G rsa -u ak_pub.bin -n ak.name -c ak.ctx' executed \n")
        self.command_out.AppendText("'tpm2_evictcontrol -C o -P " + exec_cmd.ownerAuth + " -c ak.ctx " + specific_handle + " executed \n")

        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnGenQuote1(self, evt):
        self.command_out.AppendText("Generating Quote of the PCR Index... \n")
        wx.CallLater(10, self.OnGenQuote)
    
    def OnGenQuote(self):
        pcr_choice = self.pcr_bank_choice.GetStringSelection()
        specific_handle = self.ak_handle_input.GetValue()
        input_nonce = self.nonce_input.GetValue()
        if (input_nonce == ""):
            return
        elif (len(input_nonce) % 2 != 0):
            self.command_out.AppendText("Error! Nonce must be of even length as it will be converted to a byte array.\n")
            return
        input_nonce = exec_cmd.convertInputToHex(input_nonce, len(input_nonce))
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_quote",
            "-c", specific_handle,
            "-g", "sha256",
            "-l", "sha256:"+pcr_choice,
            "-m", "tpmquote.data",
            "-q", input_nonce,
            "-f", "plain",
            "-s", "quote_sign_data",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("\n")
        self.command_out.AppendText("'tpm2_quote -c " + specific_handle+ " -g sha256 -l sha256:" + pcr_choice + " -m tpmquote.data -q " + input_nonce + " -f plain -s quote_sign_data' executed \n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_readpublic",
            "-c", specific_handle,
            "-f", "pem",
            "-o", "ak_pub.pem",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("\n")
        self.command_out.AppendText("'tpm2_readpublic -c "+specific_handle+" -f pem -o ak_pub.pem' executed \n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

#     def OnVerifyQSSL(self, evt):
#         command_output = exec_cmd.execCLI([
#             "openssl", "dgst",
#             "-verify", "ak_pub.pem",
#             "-keyform", "pem",
#             "-sha256",
#             "-signature", "quote_sign_data",
#             "tpmquote.data",
#         ])
#         self.command_out.AppendText(str(command_output))
#         self.command_out.AppendText("'openssl dgst -verify ak_pub.pem -keyform pem -sha256 -signature quote_sign_data tpmquote.data' executed \n")
#         self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnVerifyQTPM(self, evt):
        input_nonce = self.nonce_input.GetValue()
        if (input_nonce == ""):
            return
        input_nonce = exec_cmd.convertInputToHex(input_nonce, len(input_nonce))
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_checkquote",
            "-u", "ak_pub.pem",
            "-m", "tpmquote.data",
            "-s", "quote_sign_data",
            "-g", "sha256",
            "-q", input_nonce,
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_checkquote -c ak_pub.pem -m tpmquote.data -s quote_sign_data -G sha256 -q " + input_nonce + "' executed \n")
        self.command_out.AppendText("Verification Successful Unless Error Message Is Shown\n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnEvict(self, evt):
        specific_handle = self.ak_handle_input.GetValue()
        if (misc.OwnerDlg(self, "Enter Owner Authorisation").ShowModal() == -1):
            return
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_evictcontrol",
            "-C", "o",
            "-c", specific_handle,
            "-P", exec_cmd.ownerAuth,
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_evictcontrol -C o -c " + specific_handle + " -P " + exec_cmd.ownerAuth + "' executed \n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnInfo(self, evt):
        info.AttestationInfoDlg(self, "Attestation Information").ShowModal()

    def OnClear(self, evt):
        self.command_out.Clear()

    def OnCloseWindow(self, evt):
        self.Parent.Show()
        self.Destroy()
