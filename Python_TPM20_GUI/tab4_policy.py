import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import info_dialogs as info
import os
import images as img
pcr_index_list = [str(value) for value in range(0, 24)]
""" Note that the steps CANNOT be done out of order. Technically they should be done all in one shot,
but we have split up the steps for better understanding.
"""


class Tab4Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="Enhanced Authorisation", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        self.SetBackgroundColour(wx.WHITE)
        main_menu_font = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        choices_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_plus_txtbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        mini_button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # instantiate the objects
        pcr_bank_blurb = wx.StaticText(self, -1, "Pick the PCR Index:")
        self.pcr_bank_choice = wx.ComboBox(self, -1, "Pick the PCR Index", choices=pcr_index_list, style=wx.CB_READONLY)
        data_blurb = wx.StaticText(self, -1, "Data to be sealed:")
        self.data_input = wx.TextCtrl(self, -1)
        button_create_policy = wx.Button(self, -1, 'Generate Policy from selected PCR', size = (-1, 48))
        button_create_primary = wx.Button(self, -1, 'Generate Primary (Owner)', size = (-1, 48))
        button_seal_data = wx.Button(self, -1, 'Seal Data', size = (-1, 48))
        button_satisfy_unseal = wx.Button(self, -1, 'Satisfy Policy and Unseal', size = (-1, 48))
        self.command_out = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.command_out.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        # ~clearbutton = wx.BitmapButton(self, -1, img.clear.getBitmap())
        
        infoimage = wx.Image('../images/info.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        infobutton = wx.BitmapButton(self, -1, infoimage)
        # ~infobutton = wx.BitmapButton(self, -1, img.info.getBitmap())
                
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the sizers to the main sizer
        mainsizer.AddSpacer(5)
        mainsizer.Add(choices_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        mainsizer.Add(buttons_plus_txtbox_sizer, 1, wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, 5)
        buttons_plus_txtbox_sizer.Add(button_sizer, 0, wx.EXPAND)
        buttons_plus_txtbox_sizer.Add(self.command_out, 1, wx.EXPAND | wx.ALL, 5)

        # attach the ui elements to the internal sizer
        choices_sizer.Add(pcr_bank_blurb, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        choices_sizer.Add(self.pcr_bank_choice, 0, wx.EXPAND | wx.ALL, 5)
        choices_sizer.AddSpacer(5)
        choices_sizer.Add(data_blurb, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        choices_sizer.Add(self.data_input, 1, wx.EXPAND | wx.ALL, 5)
        button_sizer.Add(button_create_policy, 0, wx.EXPAND | wx.ALL, 5)
        button_sizer.Add(button_create_primary, 0, wx.EXPAND | wx.ALL, 5)
        button_sizer.Add(button_seal_data, 0, wx.EXPAND | wx.ALL, 5)
        button_sizer.Add(button_satisfy_unseal, 0, wx.EXPAND | wx.ALL, 5)
        button_sizer.AddSpacer(348)
        button_sizer.Add(mini_button_sizer, 0, wx.EXPAND | wx.ALL, 0)
        mini_button_sizer.Add(infobutton, 0, wx.ALL, 5)
        mini_button_sizer.Add(clearbutton, 0, wx.ALL, 5)
        mini_button_sizer.Add(backbutton, 0, wx.ALL, 5)

        # Set tooltips
        button_create_policy.SetToolTip(wx.ToolTip("TPM2_PolicyPCR: Create a policy based on a PCR index, using a trial policy session."))
        button_create_primary.SetToolTip(wx.ToolTip("TPM2_CreatePrimary: Create a Primary Key Pair under the Owner Authorisation. Handle: 0x81000001"))
        button_seal_data.SetToolTip(wx.ToolTip("TPM2_Create: Create a file containing data input to be sealed into the TPM"))
        button_satisfy_unseal.SetToolTip(wx.ToolTip("TPM2_PolicyPCR: Using a non-trial policy session, check if the PCR index satisfies the policy. TPM2_Unseal: Returns data in a loaded sealed TPM object, provided the policy is satisfied."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # declare and bind events
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnNewPolicy1, button_create_policy)
        self.Bind(wx.EVT_BUTTON, self.OnNewPrimary1, button_create_primary)
        self.Bind(wx.EVT_BUTTON, self.OnSealData, button_seal_data)
        self.Bind(wx.EVT_BUTTON, self.OnSatisfyPolicy_UnsealData1, button_satisfy_unseal)
        self.Bind(wx.EVT_BUTTON, self.OnMoreInfo, infobutton)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, backbutton)

        # set default values
        self.pcr_bank_choice.SetSelection(5)
        self.data_input.write("My secret")
        self.SetSizer(mainsizer)
        self.Show(True)
    
    def OnNewPolicy1(self, evt):
        self.command_out.AppendText("Generating Policy... \n")
        wx.CallLater(10, self.OnNewPolicy)
        
    def OnNewPolicy(self):
        pcr_choice = self.pcr_bank_choice.GetStringSelection()
        
        os.system('rm *.dat')
        os.system('rm unseal.key*.*')
        os.system('rm key.*')
        
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_pcrread",
            "sha256:" + pcr_choice,
            "-o", "pcr.dat",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_pcrread sha256:" + pcr_choice + " -o pcr.dat' executed \n")
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_startauthsession",
            "-S", "session.dat",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_startauthsession -S session.dat' executed \n")
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_policypcr",
            "-S", "session.dat",
            "-l", "sha256:" + pcr_choice,
            "-f", "pcr.dat",
            "-L", "policy.dat",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_policypcr -S session.dat -l sha256:" + pcr_choice + " -f pcr.dat -L policy.dat' executed \n")
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_flushcontext",
            "session.dat",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_flushcontext session.dat' executed \n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        exec_cmd.execCLI(["rm", "session.dat", ])

    def OnNewPrimary1(self, evt):
        self.command_out.AppendText("Creating Primary Key Pair... \n")
        wx.CallLater(10, self.OnNewPrimary)
    
    def OnNewPrimary(self):
        if (misc.OwnerDlg(self, "Enter Owner Authorisation").ShowModal() == -1):
            return
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_createprimary",
            "-C", "o",
            "-P", exec_cmd.ownerAuth,
            "-g", "sha256",
            "-G", "ecc",
            "-c", "primary.ctx",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_createprimary -C o -P " + exec_cmd.ownerAuth + " -g sha256 -G ecc -c primary.ctx' executed \n")
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_evictcontrol",
            "-C", "o",
            "-c", "primary.ctx",
            "-P", exec_cmd.ownerAuth,
            "0x81000001",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_evictcontrol -a o -c primary.ctx -P " + exec_cmd.ownerAuth + " 0x81000001' executed \n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnSealData(self, evt):
        seal_data = self.data_input.GetValue()
        if (seal_data == ""):
            self.bottom_txt_display.AppendText("Data to be sealed cannot be left empty.\n")
            return
        data_file = open("data_to_be_sealed.txt", "w")
        data_file.write(seal_data)
        data_file.close()
        self.command_out.AppendText("Sealing data_to_be_sealed.txt...\n")
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_create",
            "-C", "0x81000001",
            "-g", "sha256",
            "-u", "key.pub",
            "-r", "key.priv",
            "-L", "policy.dat",
            "-i", "data_to_be_sealed.txt",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_create -C 0x81000001 -g sha256 -u key.pub -r key.priv -L policy.dat -i data_to_be_sealed.txt' executed \n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnSatisfyPolicy_UnsealData1(self, evt):
        self.command_out.AppendText("Checking if the PCR index satisfies the policy... \n")
        wx.CallLater(10, self.OnSatisfyPolicy_UnsealData)
    
    def OnSatisfyPolicy_UnsealData(self):
        pcr_choice = self.pcr_bank_choice.GetStringSelection()
        os.system('rm unseal.key*.*')
        os.system('rm session*.dat')
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_load",
            "-C", "0x81000001",
            "-u", "key.pub",
            "-r", "key.priv",
            "-n", "unseal.key.name",
            "-c", "unseal.key.ctx",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_load -C 0x81000001 -u key.pub -r key.priv -n unseal.key.name -c unseal.key.ctx' executed \n")

        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_startauthsession",
            "--policy-session",
            "-S", "session.dat",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_startauthsession -S session.dat' executed \n")
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_policypcr",
            "-S", "session.dat",
            "-l", "sha256:" + pcr_choice,
            "-f", "pcr.dat",
            "-L", "policy.dat",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_policypcr -S session.dat -l sha256:" + pcr_choice + " -f pcr.dat -L policy.dat' executed \n")
        self.command_out.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        exec_cmd.execTpmToolsAndCheck(["rm", "unsealed_data.txt"])
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_unseal",
            "-psession:session.dat",
            "-c", "unseal.key.ctx",
            "-o", "unsealed_data.txt",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_unseal -psession:session.dat -c unseal.key.ctx -o unsealed_data' executed \n")
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_flushcontext",
            "session.dat",
        ])
        self.command_out.AppendText(str(command_output))
        self.command_out.AppendText("'tpm2_flushcontext session.dat' executed \n")
        data_file = open("unsealed_data.txt", "r")
        unsealed_data = data_file.read()
        data_file.close()
        self.command_out.AppendText(str(unsealed_data))
        self.command_out.AppendText("\n++++++++++++++++++++++++++++++++++++++++++++\n")
        exec_cmd.execCLI(["rm", "session.dat", ])

    def OnMoreInfo(self, evt):
        info.PolicyInfoDlg(self, "Enhanced Authorisation Information").ShowModal()

    def OnClear(self, evt):
        self.command_out.Clear()

    def OnCloseWindow(self, evt):
        self.Parent.Show()
        self.Destroy()
