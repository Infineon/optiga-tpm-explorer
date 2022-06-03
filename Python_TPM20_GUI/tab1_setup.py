import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import info_dialogs as info
import images as img
import binascii
import subprocess
#~ import os
from subprocess import PIPE
# the tpm has 24 banks
pcr_index_list = [str(value) for value in range(0, 24)]
# from TPM 2.0 Part 2 Structures pg 159 of pdf (section 13.1, table 204)
# Note: 0x80020002 is default for ownerwrite|ownerread|read_stclear
nvm_attr_list = [
    'ppwrite', 'ownerwrite', 'authwrite', 'policywrite', 'policy_delete',
    'writelocked', 'writeall', 'writedefine', 'write_stclear', 'globallock', 'ppread',
    'ownerread', 'authread', 'policyread', 'no_da', 'orderly', 'clear_stclear',
    'readlocked', 'written', 'platformcreate', 'read_stclear']

nvm_predefined_index = ['0x1c00002', '0x1c0000a', '0x1c00016'] 

tpm2_max_auth_fail = None
tpm2_lockout_interval = None
tpm2_lockout_recovery = None
client_log = None

class Tab_Setup(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsizer = wx.BoxSizer(wx.VERTICAL)
        iconsizer = wx.BoxSizer(wx.HORIZONTAL)

        # instantiate the objects
        button_start = wx.Button(self, -1, 'Startup')
        button_takeown = wx.Button(self, -1, 'Change Auth')
        button_clear = wx.Button(self, -1, 'TPM Clear')
        button_disablelock = wx.Button(self, -1, 'TPM Clear Enable')
        button_enablelock = wx.Button(self, -1, 'TPM Clear Disable')
        button_dictAtk = wx.Button(self, -1, 'Dictionary Attack Settings')
        button_getCapVar = wx.Button(self, -1, 'Get TPM capability (variable)')
        button_getCapFix = wx.Button(self, -1, 'Get TPM capability (fixed)')
        self.text_display = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        #~ self.text_display.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.text_display.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        # ~ clearbutton = wx.BitmapButton(self, -1, img.clear.getBitmap())

        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~ backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())

        # attach the objects to the sizers
        mainsizer.Add(buttonsizer, 0, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(self.text_display, 1, wx.EXPAND)
        buttonsizer.Add(button_getCapVar, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(button_getCapFix, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(button_takeown, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(button_clear, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(button_enablelock, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(button_disablelock, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(button_dictAtk, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(button_start, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(iconsizer, 0, wx.EXPAND | wx.ALL, 0)
        iconsizer.Add(clearbutton, 0, wx.ALL, 5)
        iconsizer.Add(backbutton, 0, wx.ALL, 5)

        # Set tooltips
        button_start.SetToolTip(wx.ToolTip("TPM2_Startup: Required to be run after pressing the hardware reset. Not doing so will result in the TPM being unresponsive."))
        button_takeown.SetToolTip(wx.ToolTip("TPM2_ChangeAuth: Set Hierarchy Authorisation Passwords"))
        button_clear.SetToolTip(wx.ToolTip("TPM2_Clear: Using Platform Authorisation to reset all TPM settings and contexts."))
        button_dictAtk.SetToolTip(wx.ToolTip("TPM2_DictionaryLockout: Set values dictating how the TPM should handle failed authorisation attempts."))
        button_disablelock.SetToolTip(wx.ToolTip("TPM2_ClearLock: Disable the use of TPM2_Clear"))
        button_enablelock.SetToolTip(wx.ToolTip("TPM2_ClearLock: Enable the use of TPM2_Clear"))
        button_getCapVar.SetToolTip(wx.ToolTip("TPM2_GetCap: Get TPM variables, such as whether hierarchies are enabled, or dictionary attack settings."))
        button_getCapFix.SetToolTip(wx.ToolTip("TPM2_GetCap: Get TPM constants, such as Manufacturer, Vendor, Firmware values."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # declare and bind events
        self.Bind(wx.EVT_BUTTON, self.OnStart, button_start)
        self.Bind(wx.EVT_BUTTON, self.OnChangeAuth, button_takeown)
        self.Bind(wx.EVT_BUTTON, self.OnClear, button_clear)
        self.Bind(wx.EVT_BUTTON, self.OnDictAtk, button_dictAtk)
        self.Bind(wx.EVT_BUTTON, self.OnDisableLock, button_disablelock)
        self.Bind(wx.EVT_BUTTON, self.OnEnableLock, button_enablelock)
        self.Bind(wx.EVT_BUTTON, self.OnGetCapVar, button_getCapVar)
        self.Bind(wx.EVT_BUTTON, self.OnGetCapFix, button_getCapFix)
        self.Bind(wx.EVT_BUTTON, self.OnFlush, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)

        self.SetSizer(mainsizer)

    def OnStart(self, evt):
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_startup",
            "-c",
        ])
        self.text_display.AppendText(str(command_output))
        self.text_display.AppendText("'tpm2_startup -c' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    # Get three authorisation values from the user.
    # If any of the values are null, we do not set that value.
    def OnChangeAuth(self, evt):
        if (misc.CredentialDlg(self, "Enter in the credentials").ShowModal() == -1):
            return
        if (exec_cmd.ownerAuth != ""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_changeauth",
                "-c","owner", exec_cmd.ownerAuth,
            ])
            self.text_display.AppendText(str(command_output))
            self.text_display.AppendText("'tpm2_changeauth -c owner " + exec_cmd.ownerAuth + "' executed \n")
        if (exec_cmd.endorseAuth != ""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_changeauth",
                "-c","endorsement", exec_cmd.endorseAuth,
            ])
            self.text_display.AppendText(str(command_output))
            self.text_display.AppendText("'tpm2_changeauth -c endorsement " + exec_cmd.endorseAuth + "' executed \n")
        if (exec_cmd.lockoutAuth != ""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_changeauth",
                "-c","lockout", exec_cmd.lockoutAuth,
            ])
        
            self.text_display.AppendText(str(command_output))
            self.text_display.AppendText("'tpm2_changeauth -c lockout " + exec_cmd.lockoutAuth + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        #~ f = open("values.txt", "w+")
        #~ f.write('ownerAuth = "')
        #~ f.write(exec_cmd.ownerAuth)
        #~ f.write('"\n')
        #~ f.write('endorseAuth = "')
        #~ f.write(exec_cmd.endorseAuth)
        #~ f.write('"\n')
        #~ f.write('lockoutAuth = "')
        #~ f.write(exec_cmd.lockoutAuth)
        #~ f.write('"\n')
        #~ f.close()
        
        #~ if (misc.RestartApp(self, "NOTICE").ShowModal() == -1):
            #~ return
        #~ command_output = exec_cmd.execTpmToolsAndCheck([
            #~ "./reboot.sh",
        #~ ])
        #~ command_output = exec_cmd.execTpmToolsAndCheck([
            #~ "xkill",
        #~ ])
        
    def OnClear(self, evt):
        if (misc.ClearWarningDlg(self, "Warning!").ShowModal() != wx.ID_OK):
            return
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_clear",
            "-c","p"
        ])
        exec_cmd.createProcess("sudo rm *.tss", None)


        self.text_display.AppendText(str(command_output))
        self.text_display.AppendText("'tpm2_clear -c p' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    # this locks the clear command (above this), i.e. the user cannot platform clear
    def OnEnableLock(self, evt):
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_clearcontrol",
            "-C", "l", "s", "-P", exec_cmd.lockoutAuth,
        ])
        self.text_display.AppendText(str(command_output))
        #self.text_display.AppendText(str(command_output))
        
        self.text_display.AppendText("'tpm2_clearcontrol -C l s -P " + exec_cmd.lockoutAuth + "' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnDisableLock(self, evt):
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_clearcontrol",
            "-C", "p", "c",
        ])
        self.text_display.AppendText(str(command_output))
        self.text_display.AppendText("'tpm2_clearcontrol -C p c' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnDictAtk(self, evt):
        if (misc.DictAttackDlg(self, "Enter in the Values.").ShowModal() == -1):
            return
        if ((tpm2_max_auth_fail, tpm2_lockout_interval, tpm2_lockout_recovery) != (None, None, None)):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_dictionarylockout", "-s",
                "-n", tpm2_max_auth_fail,
                "-t", tpm2_lockout_interval,
                "-l", tpm2_lockout_recovery,
                "-p", exec_cmd.lockoutAuth,
            ])
            self.text_display.AppendText(str(command_output))
            self.text_display.AppendText("tpm2_dictionarylockout executed \n")
            self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
        else:
            self.text_display.AppendText("The values entered in are not integers (in decimal). \n")

    def OnGetCapVar(self, evt):
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_getcap",
            "properties-variable",
        ])
        self.text_display.AppendText(str(command_output))
        self.text_display.AppendText("'tpm2_getcap properties-variable' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnGetCapFix(self, evt):
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_getcap",
            "properties-fixed",
        ])
        self.text_display.AppendText(str(command_output))
        self.text_display.AppendText("'tpm2_getcap properties-fixed' executed \n")
        self.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnFlush(self, evt):
        self.text_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)


class Tab_PCR(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        top_row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        middle_row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_row_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # instantiate the objects
        self.sha_checkbox = wx.CheckBox(self, -1, "For PCR List && Extend: Checked = SHA-2, Unchecked = SHA-1")
        self.sha_checkbox.SetValue(True)
        text_for_pcrbank = wx.StaticText(self, -1, "Choose your PCR Index: ")
        self.pcr_bank_choice = wx.ComboBox(self, -1, "Pick the PCR Index", choices=pcr_index_list, style=wx.CB_READONLY)
        text_for_userinput = wx.StaticText(self, -1, "Input for PCR operations: ")
        self.user_input = wx.TextCtrl(self, -1)
        button_pcrlistall = wx.Button(self, -1, 'PCR List All')
        button_pcrlist = wx.Button(self, -1, 'PCR List')
        button_pcrextend = wx.Button(self, -1, 'PCR Extend')
        button_pcrevent = wx.Button(self, -1, 'PCR Event')
        self.bottom_txt_display = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.bottom_txt_display.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        # ~clearbutton = wx.BitmapButton(self, -1, img.clear.getBitmap())

        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())


        # attach the sizers to the main sizer
        mainsizer.Add(top_row_sizer, 0, wx.TOP, 5)
        mainsizer.Add(middle_row_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        mainsizer.Add(bottom_row_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        mainsizer.Add(self.bottom_txt_display, 1, wx.EXPAND | wx.TOP, 5)

        # attach the ui elements to the internal sizer
        top_row_sizer.Add(self.sha_checkbox, 0, wx.ALL, 5)
        top_row_sizer.Add((200, 10), proportion=1, flag=wx.EXPAND)
        top_row_sizer.AddSpacer(60)
        top_row_sizer.Add(text_for_pcrbank, 0, wx.ALIGN_CENTRE, 5)
        top_row_sizer.Add(self.pcr_bank_choice, 0, wx.ALL, 5)
        middle_row_sizer.AddSpacer(5)
        middle_row_sizer.Add(text_for_userinput, 0, wx.ALIGN_CENTRE, 5)
        middle_row_sizer.Add(self.user_input, 1, wx.ALL, 5)
        bottom_row_sizer.Add(button_pcrlistall, 1, wx.EXPAND | wx.ALL, 5)
        bottom_row_sizer.Add(button_pcrlist, 1, wx.EXPAND | wx.ALL, 5)
        bottom_row_sizer.Add(button_pcrextend, 1, wx.EXPAND | wx.ALL, 5)
        bottom_row_sizer.Add(button_pcrevent, 1, wx.EXPAND | wx.ALL, 5)
        bottom_row_sizer.Add(clearbutton, 0, wx.ALL, 5)
        bottom_row_sizer.Add(backbutton, 0, wx.ALL, 5)

        # Set tooltips
        button_pcrlistall.SetToolTip(wx.ToolTip("TPM2_PCRList: List the value of a specific Platform Configuration Register (PCR) bank."))
        button_pcrlist.SetToolTip(wx.ToolTip("TPM2_PCRList: List the value of a specific Platform Configuration Register (PCR) Index."))
        button_pcrextend.SetToolTip(wx.ToolTip("TPM2_PCRExtend: New PCR Value is the hash of the concatenation of the current PCR bank value and the data input."))
        button_pcrevent.SetToolTip(wx.ToolTip("TPM2_PCREvent: Similar to Extend, but the data input is now hashed before being concatenated with the PCR bank value."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # set defaults
        self.pcr_bank_choice.SetSelection(0)
        self.user_input.Clear()
        self.user_input.AppendText("0123456789ABCDEF")

        # declare and bind events
        self.Bind(wx.EVT_BUTTON, self.OnPCRListAll, button_pcrlistall)
        self.Bind(wx.EVT_BUTTON, self.OnPCRList, button_pcrlist)
        self.Bind(wx.EVT_BUTTON, self.OnPCRExtend, button_pcrextend)
        self.Bind(wx.EVT_BUTTON, self.OnPCREvent, button_pcrevent)
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)

        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        self.Centre()

    def OnPCRListAll(self, evt):
        hash_alg = self.sha_checkbox.GetValue()
        pcr_choice = self.pcr_bank_choice.GetStringSelection()
        hashinput = self.user_input.GetValue()
        if (len(pcr_choice) == 0):
            return
        elif (len(hashinput) == 0):
            return
        if (hash_alg):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_pcrread",
                "sha256",
            ])
        else:
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_pcrread",
                "sha1",
            ])
        self.bottom_txt_display.AppendText(str(command_output))
        self.bottom_txt_display.AppendText("'tpm2_pcrread shaxxx' executed \n")
        self.bottom_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnPCRList(self, evt):
        hash_alg = self.sha_checkbox.GetValue()
        pcr_choice = self.pcr_bank_choice.GetStringSelection()
        hashinput = self.user_input.GetValue()
        if (len(pcr_choice) == 0):
            return
        elif (len(hashinput) == 0):
            return
        if (hash_alg):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_pcrread",
                "sha256:" + pcr_choice,
            ])
        else:
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_pcrread",
                "sha1:" + pcr_choice,
            ])
        self.bottom_txt_display.AppendText(str(command_output))
        self.bottom_txt_display.AppendText("'tpm2_pcrread' executed \n")
        self.bottom_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnPCRExtend(self, evt):
        pcr_choice = self.pcr_bank_choice.GetStringSelection()
        hash_alg = self.sha_checkbox.GetValue()
        hashinput = self.user_input.GetValue()
        if (len(pcr_choice) == 0):
            return
        elif (len(hashinput) == 0):
            return
        if (hash_alg):
            hash_ver = 'sha256'
        else:
            hash_ver = 'sha1'
        # for SHA-1: input MUST BE HEX and len==40
        # for SHA-2: input MUST BE HEX and len==64 characters
        if (hash_alg):
            extend_input = exec_cmd.convertInputToHex(hashinput, 64)
        else:
            extend_input = exec_cmd.convertInputToHex(hashinput, 40)
        if (extend_input == 0):
            self.bottom_txt_display.AppendText("Input must be in HEX please. \n")
            return
        self.bottom_txt_display.AppendText("Input= " + extend_input + "\n")
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_pcrextend",
            pcr_choice + ":" + hash_ver + "=" + extend_input,
        ])
        self.bottom_txt_display.AppendText(str(command_output))
        self.bottom_txt_display.AppendText("'tpm2_pcrextend' executed \n")
        self.bottom_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnPCREvent(self, evt):
        hashinput = self.user_input.GetValue()
        pcr_choice = self.pcr_bank_choice.GetStringSelection()
        if (len(pcr_choice) == 0):
            return
        elif (len(hashinput) == 0):
            return
        data_file = open("pcrevent_data.txt", "w")
        data_file.write(hashinput)
        data_file.close()
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_pcrevent",
            pcr_choice,
            "pcrevent_data.txt",
        ])
        self.bottom_txt_display.AppendText(str(command_output))
        self.bottom_txt_display.AppendText("'tpm2_pcrevent' executed \n")
        self.bottom_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnClear(self, evt):
        self.bottom_txt_display.Clear()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)

class Tab_NVM(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # instantiate the objects for left
        text_for_nvm_attr = wx.StaticText(self, -1, "NVM attributes:")
        self.nvm_attr = wx.CheckListBox(self, -1, choices=nvm_attr_list)
        
        # instantiate the objects for middle
        text_for_nvm_index = wx.StaticText(self, -1, "NVM index (in hex): ")
        self.nvm_index = wx.TextCtrl(self, -1, size=(212, 33))
        text_for_nvm_size = wx.StaticText(self, -1, "NVM size (in bytes): ")
        self.nvm_size = wx.TextCtrl(self, -1)
        text_for_nvm_offset = wx.StaticText(self, -1, "NVM offset: ")
        self.nvm_offset = wx.TextCtrl(self, -1, size=(292, 33))
        text_for_read_amt = wx.StaticText(self, -1, "Read size: ")
        self.read_amt = wx.TextCtrl(self, -1)
        text_for_nvm_data = wx.StaticText(self, -1, "NVM data: ")
        self.nvm_data = wx.TextCtrl(self, -1)
        text_for_owner_auth = wx.StaticText(self, -1, "Owner Authorisation: ")
        self.owner_input = wx.TextCtrl(self, -1, size=(201, 33))
        text_for_nv_auth = wx.StaticText(self, -1, "NV Authorisation: ")
        self.nv_auth_input = wx.TextCtrl(self, -1)
        button_nvdefine = wx.Button(self, -1, 'NV Define', size=(201, 33))
        button_nvwrite = wx.Button(self, -1, 'NV Write')
        button_nvwrite_file = wx.Button(self, -1, 'NV Write File', size=(201, 33))
        self.filename_input = wx.TextCtrl(self, -1, value="ifx_ecc_cert.crt", style=(wx.TE_CHARWRAP|wx.TE_MULTILINE), size=(201, 70))
        # Create open file dialog
        button_nvrelease = wx.Button(self, -1, 'NV Release')
        button_reset_attr = wx.Button(self, -1, 'Reset to Default')
        button_nvread = wx.Button(self, -1, 'NV Read')
        button_nvrelock = wx.Button(self, -1, 'NV Read Lock')
        button_nvlist = wx.Button(self, -1, 'NV List')
        button_nv_read_rsa_cert = wx.Button(self, -1, 'Read RSA Cert')
        self.rsa_cert_index = wx.TextCtrl(self, -1,value="0x1c00002")
        button_nv_read_ecc_cert = wx.Button(self, -1, 'Read ECC Cert')
        self.ecc_cert_index = wx.TextCtrl(self, -1,value="0x1c0000a")
        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        # ~clearbutton = wx.BitmapButton(self, -1, img.clear.getBitmap())
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())
        
        #instantiate the objects for right
        self.right_txt_display = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.right_txt_display.SetFont(wx.Font(11, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
 
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        left_nvm_attr_sizer = wx.BoxSizer(wx.VERTICAL)
        middle_input_sizer = wx.BoxSizer(wx.VERTICAL)
        right_display_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # declare sizers inside middle_input_sizer
        fgs1 = wx.FlexGridSizer(rows=2, cols=2, vgap=9, hgap=0)
        fgs2 = wx.FlexGridSizer(rows=3, cols=2, vgap=9, hgap=0)
        fgs3 = wx.FlexGridSizer(rows=2, cols=2, vgap=9, hgap=0)
        gs1 = wx.GridSizer(rows=3, cols=2, vgap=9, hgap=10)
        hori_sizer = wx.BoxSizer(wx.HORIZONTAL)
        gs2 = wx.GridSizer(rows=2, cols=2, vgap=9, hgap=10)
        icon_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # declare sizers inside hori_sizer and attach to hori_sizer
        inside_hori_sizer1 = wx.BoxSizer(wx.VERTICAL)
        inside_hori_sizer2 = wx.BoxSizer(wx.VERTICAL)
        hori_sizer.Add(inside_hori_sizer1, 0, wx.EXPAND | wx.RIGHT, 9)
        hori_sizer.Add(inside_hori_sizer2, 1, wx.EXPAND)
        
        # attach the sizers to the main sizer
        mainsizer.Add(left_nvm_attr_sizer, 0, wx.EXPAND | wx.ALL, 9)
        mainsizer.Add(middle_input_sizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 9)
        mainsizer.Add(right_display_sizer, 1, wx.EXPAND | wx.ALL, 0)
        
        # attach the sizers to the middle sizer
        middle_input_sizer.Add(fgs1, 0, wx.EXPAND | wx.BOTTOM, 9)
        middle_input_sizer.Add(fgs2, 0, wx.EXPAND | wx.BOTTOM, 9)
        middle_input_sizer.Add(fgs3, 0, wx.EXPAND | wx.BOTTOM, 12)
        middle_input_sizer.Add(gs1, 0, wx.EXPAND | wx.BOTTOM, 9)
        middle_input_sizer.Add(hori_sizer, 0, wx.EXPAND | wx.BOTTOM, 9)
        middle_input_sizer.Add(gs2, 0, wx.EXPAND | wx.BOTTOM, 9)
        middle_input_sizer.Add(icon_sizer, 0, wx.EXPAND | wx.ALL, 0)
        
        # attach the object to the right sizer
        right_display_sizer.Add(self.right_txt_display, 1, wx.EXPAND | wx.ALL, 0)
        
        # attach the objects to the left sizer
        left_nvm_attr_sizer.Add(text_for_nvm_attr, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        left_nvm_attr_sizer.Add(self.nvm_attr, 1, wx.EXPAND | wx.ALL, 0)
        left_nvm_attr_sizer.Add(button_reset_attr, 0, wx.EXPAND | wx.TOP, 9)
        
        # attach the objects to the middle sizer
        fgs1.Add(text_for_nvm_index, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        fgs1.Add(self.nvm_index, 0, wx.EXPAND, 0)
        fgs1.Add(text_for_nvm_size, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        fgs1.Add(self.nvm_size, 0, wx.EXPAND, 0)
        fgs2.Add(text_for_nvm_offset, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        fgs2.Add(self.nvm_offset, 0, wx.EXPAND, 0)
        fgs2.Add(text_for_nvm_data, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        fgs2.Add(self.nvm_data, 0, wx.EXPAND, 0)
        fgs2.Add(text_for_read_amt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        fgs2.Add(self.read_amt, 0, wx.EXPAND, 0)
        fgs3.Add(text_for_owner_auth, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        fgs3.Add(self.owner_input, 0, wx.EXPAND, 0)
        fgs3.Add(text_for_nv_auth, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        fgs3.Add(self.nv_auth_input, 0, wx.EXPAND, 0)
        gs1.Add(button_nvdefine, 0, wx.EXPAND, 0)
        gs1.Add(button_nvwrite, 0, wx.EXPAND, 0)
        gs1.Add(button_nvrelease, 0, wx.EXPAND, 0)
        gs1.Add(button_nvread, 0, wx.EXPAND, 0)
        gs1.Add(button_nvrelock, 0, wx.EXPAND, 0)
        gs1.Add(button_nvlist, 0, wx.EXPAND, 0)
        inside_hori_sizer1.Add(button_nvwrite_file, 0, wx.EXPAND, 0)
        inside_hori_sizer2.Add(self.filename_input, 0, wx.EXPAND, 0)
        gs2.Add(button_nv_read_rsa_cert, 0, wx.EXPAND, 0)
        gs2.Add(self.rsa_cert_index, 0, wx.EXPAND, 0)
        gs2.Add(button_nv_read_ecc_cert, 0, wx.EXPAND, 0)
        gs2.Add(self.ecc_cert_index, 0, wx.EXPAND, 0)
        icon_sizer.Add(clearbutton, 0, wx.RIGHT, 9)
        icon_sizer.Add(backbutton, 0)

        # Set tooltips
        button_nvdefine.SetToolTip(wx.ToolTip("TPM2_NVDefine: Cause the TPM to reserve space and associate that space with the NV index and attributes."))
        button_nvwrite.SetToolTip(wx.ToolTip("TPM2_NVWrite: Write to an area in NVM that is defined in TPM2_NVList. (if allowed by attributes)"))
        button_nvrelease.SetToolTip(wx.ToolTip("TPM2_NVRelease: Removes an index from the TPM and release the associated space"))
        button_nvread.SetToolTip(wx.ToolTip("TPM2_NVRead: Read from an area in NVM that is defined in TPM2_NVList. (if allowed by attributes)"))
        button_nvrelock.SetToolTip(wx.ToolTip("TPM2_NVReadLock: If READ_STCLEAR is an attribute set in the NV index, this will prevent further reads of the index, until the next TPM2_Startup."))
        button_nvlist.SetToolTip(wx.ToolTip("TPM2_NVList: List all defined areas in the TPM"))
        button_reset_attr.SetToolTip(wx.ToolTip("Reset attributes to OwnerRead, OwnerWrite and Read_STClear."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # declare and bind events
        self.Bind(wx.EVT_BUTTON, self.OnNVDefine, button_nvdefine)
        self.Bind(wx.EVT_BUTTON, self.OnNVWrite, button_nvwrite)
        
        self.Bind(wx.EVT_BUTTON, self.OnNVWriteFile, button_nvwrite_file)
        
        self.Bind(wx.EVT_BUTTON, self.OnNVRelease, button_nvrelease)
        self.Bind(wx.EVT_BUTTON, self.OnNVRead, button_nvread)
        self.Bind(wx.EVT_BUTTON, self.OnNVReadLock, button_nvrelock)
        self.Bind(wx.EVT_BUTTON, self.OnNVList, button_nvlist)
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)
        self.Bind(wx.EVT_BUTTON, self.OnResetAttr, button_reset_attr)
        self.Bind(wx.EVT_BUTTON, self.OnReadRSACert, button_nv_read_rsa_cert)
        self.Bind(wx.EVT_BUTTON, self.OnReadECCCert, button_nv_read_ecc_cert)
        #~ self.Bind(wx.EVT_SET_FOCUS, self.OnClickFileName, self.filename_input)
        self.filename_input.Bind(wx.EVT_LEFT_DOWN,self.OnClickFileName)
        # Set default values
        self.nvm_index.write("0x1500016")
        self.nvm_size.write("900")
        self.nvm_offset.write("0")
        self.read_amt.write("32")
        self.nvm_data.write("Hello World!")
        self.owner_input.write(exec_cmd.ownerAuth)
        self.nv_auth_input.write(exec_cmd.nvAuth)
        self.nvm_attr.SetCheckedStrings(["authread", "authwrite", "read_stclear"])
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        self.Show(True)
 
    def OnClickFileName(self, evt):
        frame = wx.Frame(None, -1, '*.*')
        frame.SetSize(0,0,200,50)
            
        openFileDialog = wx.FileDialog(frame, "Open", "", "","All|*.bin;*.crt;*.der|Binary|*.bin|Certificate|*.crt;*.der", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() ==wx.ID_CANCEL:
                return
        print((openFileDialog.GetPath()))
        self.filename_input.SetValue(openFileDialog.GetPath())
        
        openFileDialog.Destroy()

    def OnReadECCCert(self, evt):
        cert_index = self.ecc_cert_index.GetValue()
        owner_val = self.owner_input.GetValue()
        nv_auth_val = self.nv_auth_input.GetValue()
        
        #~ cmd ="tpm2_nvreadpublic | grep -A8 '0x1c0000a' | grep -A1 'size' | grep -Eo '[0-9]*'"
        cmd ="tpm2_nvreadpublic | grep -A8 '%s' | grep -A1 'size' | grep -Eo '[0-9]*'" % cert_index
        
        ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        read_size = ps_command.stdout.read()
        retcode = ps_command.wait()

        try:
            int(read_size)
        except ValueError:
            self.right_txt_display.write("Offset or size is an invalid value (not an integer).\n")
            return
        if (int(read_size) == 0):
            return
        
        if (cert_index in nvm_predefined_index or nv_auth_val==""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvread",
                cert_index,
                "-C", "o",
                "-s", str(int(read_size)),
                "--offset", "0",
                "-P", owner_val,
                "-o", "ifx_ecc_cert.crt",
            ])
             #~ command_output = exec_cmd.execTpmToolsAndCheck([
                #~ "tpm2_nvread",
                #~ nvm_index,
                #~ "-C", "o",
                #~ "-s", str(read_size),
                #~ "-o", nvm_offset,
                #~ "-P", owner_val,
                #~ "-o","nvdata.txt",
            #~ ])
       
        elif (nv_auth_val!=""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvread",
                cert_index,
                "-s", str(int(read_size)),
                "--offset", "0",
                "-P", nv_auth_val,
                "-o", "ifx_ecc_cert.crt",
            ])
        
        if (command_output.find("ERROR") != -1):
            self.right_txt_display.AppendText(str(command_output)+"\n")
            return
                
        #~ f = open("ifx_ecc_cert.crt", "w+")
        #~ f.write(command_output)
        #~ f.close()
        #~ command_output = exec_cmd.execTpmToolsAndCheck([
            #~ "xxd", "ifx_ecc_cert.crt",
        #~ ]) 

        cmd ="openssl x509 -inform der -in ifx_ecc_cert.crt -out ifx_ecc_cert.pem"
        ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        #~ read_size = ps_command.stdout.read()
        retcode = ps_command.wait()

        cmd ="openssl x509 -in ifx_ecc_cert.pem -text -noout"
        ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        command_output = ps_command.stdout.read()
        retcode = ps_command.wait()

        self.right_txt_display.AppendText(str(command_output.decode()))
        self.right_txt_display.AppendText("\n")
        #~ self.right_txt_display.AppendText("%s executed \n")
        self.right_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnReadRSACert(self, evt):
        cert_index = self.rsa_cert_index.GetValue()
        owner_val = self.owner_input.GetValue()
        nv_auth_val = self.nv_auth_input.GetValue()
        
        cmd ="tpm2_nvreadpublic | grep -A8 '%s' | grep -A1 'size' | grep -Eo '[0-9]*'" % cert_index
        
        ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        read_size = ps_command.stdout.read()
        retcode = ps_command.wait()

        try:
            int(read_size)
        except ValueError:
            self.right_txt_display.write("Offset or size is an invalid value (not an integer).\n")
            return
        if (int(read_size) == 0):
            return
    
        if (cert_index in nvm_predefined_index or nv_auth_val==""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvread",
                cert_index,
                "-C", "o",
                "-s", str(int(read_size)),
                "--offset", "0",
                "-P", owner_val,
                "-o", "ifx_rsa_cert.crt"
            ])
         
        elif (nv_auth_val!=""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvread",
                cert_index,
                "-s", str(int(read_size)),
                "--offset", "0",
                "-P", nv_auth_val,
                "-o", "ifx_rsa_cert.crt"
            ])
            
        if (command_output.find("ERROR") != -1):
            self.right_txt_display.AppendText(str(command_output)+"\n")
            return
                
        #~ f = open("ifx_rsa_cert.crt", "w+")
        #~ f.write(command_output)
        #~ f.close()
        #~ command_output = exec_cmd.execTpmToolsAndCheck([
            #~ "xxd", "ifx_rsa_cert.crt",
        #~ ]) 

        cmd ="openssl x509 -inform der -in ifx_rsa_cert.crt -out ifx_rsa_cert.pem"
        ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        #~ read_size = ps_command.stdout.read()
        retcode = ps_command.wait()

        cmd ="openssl x509 -in ifx_rsa_cert.pem -text -noout"
        ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        command_output = ps_command.stdout.read()
        retcode = ps_command.wait()
        
        self.right_txt_display.AppendText(str(command_output.decode()))
        self.right_txt_display.AppendText("\n")
        #~ self.right_txt_display.AppendText("%s executed \n")
        self.right_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnResetAttr(self, evt):
        self.nvm_attr.SetCheckedStrings(["authread", "authwrite"])

    def OnClear(self, evt):
        self.right_txt_display.Clear()

    # nvm_attr is derived from temp_attr. However, the command may not support all attributes and may return an error.
    # this is the tpm2_tools limitation
    def OnNVDefine(self, evt):
        nvm_index = self.nvm_index.GetValue()
        owner_val = self.owner_input.GetValue()
        nv_auth_val = self.nv_auth_input.GetValue()
        nvm_size = self.nvm_size.GetValue()
        temp_attr = []
        nvm_attr = ""
        try:
            int(nvm_size)
        except ValueError:
            return
        if (int(nvm_size) > 2048):
            self.right_txt_display.AppendText("Maximum NVM size is 2048. Input Again.\n")
            return
        for value in (self.nvm_attr.GetCheckedStrings()):
            temp_attr.append(value)
        if ((nvm_index == 0) | (nvm_size == 0)):
            return
        nvm_attr = "|".join(temp_attr)
        self.right_txt_display.AppendText("Attributes are: " + nvm_attr + "\n")
        if (self.owner_input.GetValue()=="" and self.nv_auth_input.GetValue()==""):
            self.right_txt_display.AppendText("Owner Authorisation and NV Authorisation Empty. Input Again.\n")
            return
        
        #if NV field is empty
        if (nv_auth_val==""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvdefine",
                nvm_index,
                "-C", "o",
                "-s", nvm_size,
                "-a", nvm_attr,
                "-P", owner_val,
            ])
        
        #if NV field is specified
        elif (nv_auth_val!=""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvdefine",
                nvm_index,
                "-C", "o",
                "-s", nvm_size,
                "-a", nvm_attr,
                "-P", owner_val,
                "-p", nv_auth_val,
            ])
        
        self.right_txt_display.AppendText(str(command_output))
        self.right_txt_display.AppendText("'tpm2_nvdefine' executed \n")
        self.right_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnNVWriteFile(self, evt):
        nvm_index = self.nvm_index.GetValue()
        owner_val = self.owner_input.GetValue()
        nvm_data = self.nvm_data.GetValue()
        binary_file = self.filename_input.GetValue()
        nv_auth_val = self.nv_auth_input.GetValue()
        if ((nvm_index == 0) | (nvm_data == 0)):
            return
        #~ data_file = open("nvm_data.txt", "w")
        #~ data_file.write(nvm_data)
        #~ data_file.close()
        
        #if NV auth field is empty
        if (nv_auth_val==""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvwrite",
                nvm_index,
                "-C", "o",
                "-P", owner_val,
                "-i",binary_file,
            ])
        
        #if NV auth field is specified
        elif (nv_auth_val!=""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvwrite",
                nvm_index,
                "-P", nv_auth_val,
                "-i",binary_file,
            ])
            
        self.right_txt_display.AppendText(str(command_output))
        self.right_txt_display.AppendText("'tpm2_nvwrite' executed \n")
        self.right_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnNVWrite(self, evt):
        nvm_index = self.nvm_index.GetValue()
        owner_val = self.owner_input.GetValue()
        nv_auth_val = self.nv_auth_input.GetValue()
        nvm_data = self.nvm_data.GetValue()
        if ((nvm_index == 0) | (nvm_data == 0)):
            return
        data_file = open("nvm_data.txt", "w")
        data_file.write(nvm_data)
        data_file.close()
        
        #if NV auth field is empty
        if (nv_auth_val==""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvwrite",
                nvm_index,
                "-C", "o",
                "-i","nvm_data.txt",
                "-P", owner_val,
            ])
        
        #if NV auth field is specified
        elif (nv_auth_val!=""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvwrite",
                nvm_index,
                "-i","nvm_data.txt",
                "-P", nv_auth_val,
            ])
            
        self.right_txt_display.AppendText(str(command_output))
        self.right_txt_display.AppendText("'tpm2_nvwrite' executed \n")
        self.right_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnNVRelease(self, evt):
        nvm_index = self.nvm_index.GetValue()
        owner_val = self.owner_input.GetValue()
        if (nvm_index == 0):
            return
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_nvundefine",
            "-C", "o",
            "-P", owner_val,
            nvm_index,
        ])
        self.right_txt_display.AppendText(str(command_output))
        self.right_txt_display.AppendText("'tpm2_nvrelease' executed \n")
        self.right_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnNVRead(self, evt):
        nvm_index = self.nvm_index.GetValue()
        nvm_size = self.nvm_size.GetValue()
        owner_val = self.owner_input.GetValue()
        nv_auth_val = self.nv_auth_input.GetValue()
        nvm_offset = self.nvm_offset.GetValue()
        read_size = self.read_amt.GetValue()
        
        try:
            int(nvm_size)
            int(nvm_offset)
            int(read_size)
        except ValueError:
            self.right_txt_display.write("Offset or size is an invalid value (not an integer).\n")
            return
        if (int(read_size) == 0):
            return
        
        #if NV auth field is empty
        if (nv_auth_val==""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvread",
                nvm_index,
                "-C", "o",
                "-s", str(read_size),
                "-o", nvm_offset,
                "-P", owner_val,
                "-o","nvdata.txt",
            ])
        
        #if NV auth field is specified
        elif (nv_auth_val!=""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvread",
                nvm_index,
                "-s", str(read_size),
                "-o", nvm_offset,
                "-P", nv_auth_val,
                "-o","nvdata.txt",
            ])
        
        if (command_output.find("ERROR") != -1):
            self.right_txt_display.AppendText(str(command_output)+"\n")
            return
                
        #~ f = open("nvdata.txt", "w+")
        #~ f.write(command_output)
        #~ f.close()
        command_output = exec_cmd.execTpmToolsAndCheck([
            "xxd", "nvdata.txt",
        ]) 
        
        #~ global client_log
        #~ command_output = exec_cmd.createProcess("tpm2_nvread -x" + nvm_index + " -a o -s "+ read_size+ " -o 0 -P "+ owner_val+" |  xxd > nvdata.txt", client_log)
        #~ f = open("nvdata.txt", "r")
        #~ text=f.read()  
        
        self.right_txt_display.AppendText(str(command_output))
        self.right_txt_display.AppendText("\n")
        self.right_txt_display.AppendText("'tpm2_nvread' executed \n")
        self.right_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnNVReadLock(self, evt):
        nvm_index = self.nvm_index.GetValue()
        owner_val = self.owner_input.GetValue()
        nv_auth_val = self.nv_auth_input.GetValue()
        if (nvm_index == 0):
            return
        
        if (nv_auth_val==""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvreadlock",
                nvm_index,
                "-C", "o",
                "-P", owner_val,
            ])
            
        elif (nv_auth_val!=""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_nvreadlock",
                nvm_index,
                "-P", nv_auth_val,
            ])
            
        self.right_txt_display.AppendText(str(command_output))
        self.right_txt_display.AppendText("'tpm2_nvreadlock' executed \n")
        self.right_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnNVList(self, evt):
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_nvreadpublic",
        ])
        self.right_txt_display.AppendText(str(command_output))
        self.right_txt_display.AppendText("'tpm2_nvreadpublic' executed \n")
        self.right_txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)

class Tab_Handles(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        element_sizer = wx.BoxSizer(wx.HORIZONTAL)
        handle_sizer = wx.BoxSizer(wx.HORIZONTAL)
        handle_blurb_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # instantiate the objects
        input_handle_blurb = wx.StaticText(self, -1, "Handle: ")
        self.input_handle = wx.TextCtrl(self, -1)
        button_listpersistent = wx.Button(self, -1, 'List all')
        button_readpersistent = wx.Button(self, -1, 'Read Persistent')
        button_evict_persistent = wx.Button(self, -1, 'Evict persistent')
        #~ button_flushSpecific = wx.Button(self, -1, 'Flush specific transient')
        self.txt_display = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.txt_display.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
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
        mainsizer.Add(handle_sizer, 0, wx.EXPAND | wx.TOP, 5)
        mainsizer.Add(element_sizer, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)
        mainsizer.Add(self.txt_display, 1, wx.EXPAND | wx.TOP, 5)

        # Add elements to the element sizer
        handle_blurb_sizer.Add(input_handle_blurb, 0, wx.CENTRE | wx.LEFT, 10)
        
        element_sizer.Add(button_listpersistent, 1, wx.EXPAND | wx.ALL, 5)
        element_sizer.Add(button_readpersistent, 1, wx.EXPAND | wx.ALL, 5)
        element_sizer.Add(button_evict_persistent, 1, wx.EXPAND | wx.ALL, 5)
        #~ element_sizer.Add(button_flushSpecific, 1, wx.EXPAND | wx.ALL, 5)
        element_sizer.Add(infobutton, 0, wx.EXPAND | wx.ALL, 5)
        element_sizer.Add(clearbutton, 0, wx.EXPAND | wx.ALL, 5)
        element_sizer.Add(backbutton, 0, wx.EXPAND | wx.ALL, 5)

        # Attach UI elements to the internal sizers
        handle_sizer.Add(handle_blurb_sizer, 0, wx.EXPAND | wx.ALL, 0)
        handle_sizer.Add(self.input_handle, 1, wx.EXPAND | wx.ALL, 5)
        handle_sizer.AddSpacer(5)

        # Set tooltips
        button_listpersistent.SetToolTip(wx.ToolTip("List what handles exists in the persistent store."))
        button_readpersistent.SetToolTip(wx.ToolTip("List what context exists in the specific persistent handle."))
        button_evict_persistent.SetToolTip(wx.ToolTip("TPM2_EvictControl: Remove specified handle from the persistent store."))
        #~ button_flushSpecific.SetToolTip(wx.ToolTip("TPM2_FlushContext: Remove ALL transient objects."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # declare and bind events
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnList, button_listpersistent)
        self.Bind(wx.EVT_BUTTON, self.OnEvict, button_evict_persistent)
        self.Bind(wx.EVT_BUTTON, self.OnReadPersistent, button_readpersistent)
        #~ self.Bind(wx.EVT_BUTTON, self.OnFlushSpecific, button_flushSpecific)
        self.Bind(wx.EVT_BUTTON, self.OnMoreInfo, infobutton)
        self.Bind(wx.EVT_BUTTON, self.OnBack, backbutton)

        self.input_handle.SetHint("Handle starts with 0x81 (Persistent) or 0x80 (Transient)")
        self.SetSizer(mainsizer)

    def OnClear(self, evt):
        self.txt_display.Clear()

    def OnList(self, evt):
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_getcap",
            "handles-persistent",
        ])
        self.txt_display.AppendText(str(command_output))
        self.txt_display.AppendText("'tpm2_getcap handles-persistent' executed \n")
        self.txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnEvict(self, evt):
        specific_handle = self.input_handle.GetValue()
        if (misc.OwnerDlg(self, "Enter Owner Authorisation").ShowModal() == -1):
            return
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_evictcontrol",
            "-C", "o",
            "-c", specific_handle,
            "-P", exec_cmd.ownerAuth,
        ])
        self.txt_display.AppendText(str(command_output))
        self.txt_display.AppendText("'tpm2_evictcontrol -C o -c " + specific_handle + " -P " + exec_cmd.ownerAuth + "' executed \n")
        self.txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
                                        
    def OnReadPersistent(self, evt):
        specific_handle = self.input_handle.GetValue()
        command_output = exec_cmd.execTpmToolsAndCheck([
            "tpm2_readpublic",
            "-c", specific_handle,
        ])
        self.txt_display.AppendText(str(command_output))
        self.txt_display.AppendText("'tpm2_readpublic -c " + specific_handle + "' executed \n")
        self.txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    #~ def OnFlushSpecific(self, evt):
        #~ specific_handle = self.input_handle.GetValue()
        #~ command_output = exec_cmd.execTpmToolsAndCheck([
            #~ "tpm2_flushcontext",
            #~ specific_handle,
        #~ ])
        #~ self.txt_display.AppendText(str(command_output))
        #~ self.txt_display.AppendText("'tpm2_flushcontext -c " + specific_handle + "' executed \n")
        #~ self.txt_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnMoreInfo(self, evt):
        info.HandlesInfoDlg(self, "Handle Information").ShowModal()

    # Calling parent of the parent, as direct parent is the notebook,
    # then the second parent is the frame, from which we call the destruction
    def OnBack(self, evt):
        self.Parent.Parent.OnCloseWindow(None)


class Tab1Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="TPM Setup", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        main_menu_font = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        #~ main_menu_font = wx.Font(16, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Instantiate all objects
        tab_base = wx.Notebook(self, id=wx.ID_ANY, style=wx.NB_TOP)
        tab1_setup = Tab_Setup(tab_base)
        tab2_pcr = Tab_PCR(tab_base)
        tab3_nvm = Tab_NVM(tab_base)
        tab4_context = Tab_Handles(tab_base)

        # Add tabs
        tab_base.AddPage(tab1_setup, 'Setup')
        tab_base.AddPage(tab2_pcr, 'Platform Configuration Registers')
        tab_base.AddPage(tab3_nvm, 'NVM and Certificate Management')
        tab_base.AddPage(tab4_context, 'Handle Management')

        self.Show(True)

    def OnCloseWindow(self, evt):
        self.Parent.Show()
        self.Destroy()
