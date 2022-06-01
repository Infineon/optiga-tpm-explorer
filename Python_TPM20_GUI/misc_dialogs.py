import wx
import shell_util as exec_cmd
import tab1_setup as t1

# The EndModal function returns a -1 or 1. A -1 always indicates a cancel, and the operation will not go through
# Anything else indicates that the user wants to go through with the action.

# Dialog for reset
class RestartApp(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title=title, size=(500, 150))
        self.SetBackgroundColour(wx.WHITE)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        # attach the sizers to the main sizer
        mainsizer.Add(sizer_1, 1, wx.EXPAND | wx.ALL, 5)

        # instantiate the objects
        text_input_blurb = wx.StaticText(self, -1, "The TPM Explorer Application will close now.\n\
        Please restart the application.")
        button_ok = wx.Button(self, -1, 'OK')
        
        # attach the ui elements to the internal sizer
        mainsizer.Add(button_ok, 0, wx.ALL, 5)
        sizer_1.Add(text_input_blurb, 0, wx.ALL, 5)
        
        # set defaults
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnOK, button_ok)
        self.SetSizer(mainsizer)
        self.Show(True)

    def OnCloseWindow(self, evt):
        self.EndModal(-1)
        self.Destroy()

    # this will remove spaces in the user input as it might have problems parsing later
    def OnOK(self, evt):
        self.EndModal(1)
        self.Destroy()



# Dialog for asking user input for ownerAuth
class OwnerDlg(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title=title)
        self.SetBackgroundColour(wx.WHITE)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        # attach the sizers to the main sizer
        mainsizer.Add(sizer_1, 1, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(wx.StaticText(self, -1, "All spaces will be stripped, if any"), 0, wx.ALL, 5)

        # instantiate the objects
        self.ownerAuth_input = wx.TextCtrl(self, -1, size=wx.Size(275, 25))
        ownerAuth_input_blurb = wx.StaticText(self, -1, "Owner Authorisation Value: ")
        button_ok = wx.Button(self, -1, 'OK')

        # attach the ui elements to the internal sizer
        mainsizer.Add(button_ok, 0, wx.ALL, 5)
        sizer_1.Add(ownerAuth_input_blurb, 0, wx.ALL, 5)
        sizer_1.Add(self.ownerAuth_input, 1, wx.ALL, 5)

        # set defaults
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnOK, button_ok)
        self.ownerAuth_input.WriteText(exec_cmd.ownerAuth)
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        self.Centre(wx.BOTH)
        self.Show(True)

    def OnCloseWindow(self, evt):
        self.EndModal(-1)
        self.Destroy()

    # this will remove spaces in the user input as it might have problems parsing later
    def OnOK(self, evt):
        user_owner = self.ownerAuth_input.GetValue()
        if (user_owner != ''):
            exec_cmd.ownerAuth = user_owner.replace(" ", "")
        self.EndModal(1)
        self.Destroy()


# Dialog for asking user input for endorseAuth
class EndorseDlg(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title=title, size=(500, 150))
        self.SetBackgroundColour(wx.WHITE)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        # attach the sizers to the main sizer
        mainsizer.Add(sizer_1, 1, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(wx.StaticText(self, -1, "All spaces will be stripped, if any"), 0, wx.ALL, 5)

        # instantiate the objects
        self.endorseAuth_input = wx.TextCtrl(self, -1)
        endorseAuth_input_blurb = wx.StaticText(self, -1, "Endorsement Authorisation Value: ")
        button_ok = wx.Button(self, -1, 'OK')

        # attach the ui elements to the internal sizer
        mainsizer.Add(button_ok, 0, wx.ALL, 5)
        sizer_1.Add(endorseAuth_input_blurb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer_1.Add(self.endorseAuth_input, 1, wx.ALL, 5)

        # set defaults
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnOK, button_ok)
        self.endorseAuth_input.WriteText(exec_cmd.endorseAuth)
        self.SetSizer(mainsizer)
        self.Show(True)

    def OnCloseWindow(self, evt):
        self.EndModal(-1)
        self.Destroy()

    def OnOK(self, evt):
        user_endorse = self.endorseAuth_input.GetValue()
        if (user_endorse != ''):
            exec_cmd.endorseAuth = user_endorse.replace(" ", "")
        self.EndModal(1)
        self.Destroy()


# Dialog for main menu, for OwnerAuth, EndorseAuth, LockoutAuth value
class CredentialDlg(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title=title)
        self.SetBackgroundColour(wx.WHITE)
        self.parent=parent
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        
        # attach the sizers to the main sizer
        mainsizer.Add(sizer_1, 0, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(sizer_2, 0, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(sizer_3, 0, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(wx.StaticText(self, -1, "You may leave some inputs blank, to set only a specific authorisation. All spaces will be stripped, if any"), 1, wx.ALL, 5)
        mainsizer.Add(sizer_4, 0, wx.EXPAND | wx.ALL, 5)
        # instantiate the objects
        self.ownerAuth_input = wx.TextCtrl(self, -1)
        ownerAuth_input_blurb = wx.StaticText(self, -1, "Owner Authorisation Value: ")
        self.endorseAuth_input = wx.TextCtrl(self, -1)
        endorseAuth_input_blurb = wx.StaticText(self, -1, "Endorsement Authorisation Value: ")
        self.lockoutAuth_input = wx.TextCtrl(self, -1)
        lockoutAuth_input_blurb = wx.StaticText(self, -1, "Lockout Authorisation Value: ")
        button_ok = wx.Button(self, -1, 'SET ALL')
        button_cancel = wx.Button(self, -1, 'EXIT')
        button_clear_owner = wx.Button(self, -1, 'CLEAR')
        button_clear_endorse = wx.Button(self, -1, 'CLEAR')
        button_clear_lockout = wx.Button(self, -1, 'CLEAR')
        
        # attach the ui elements to the internal sizer
        #mainsizer.Add(button_ok, 0, wx.ALL, 5)
    
        
        sizer_1.Add(ownerAuth_input_blurb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer_1.Add(self.ownerAuth_input, 1, wx.EXPAND | wx.ALL, 5)
        sizer_1.Add(button_clear_owner, 0, wx.EXPAND | wx.ALL, 5)
        
        sizer_2.Add(endorseAuth_input_blurb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer_2.Add(self.endorseAuth_input, 1, wx.EXPAND | wx.ALL, 5)
        sizer_2.Add(button_clear_endorse, 0, wx.EXPAND | wx.ALL, 5)
        
        sizer_3.Add(lockoutAuth_input_blurb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer_3.Add(self.lockoutAuth_input, 1, wx.EXPAND | wx.ALL, 5)
        sizer_3.Add(button_clear_lockout, 0, wx.EXPAND | wx.ALL, 5)
        
        sizer_4.Add(button_cancel, 0, wx.ALIGN_CENTRE | wx.ALL , 5)       
        sizer_4.Add(button_ok, 0, wx.ALIGN_CENTRE | wx.ALL , 5)  

        # set defaults
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnOK, button_ok)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, button_cancel)
        self.Bind(wx.EVT_BUTTON, self.OnClearOwnerAuth, button_clear_owner)
        self.Bind(wx.EVT_BUTTON, self.OnClearEndorseAuth, button_clear_endorse)
        self.Bind(wx.EVT_BUTTON, self.OnClearLockoutAuth, button_clear_lockout)
       
        self.ownerAuth_input.WriteText(exec_cmd.ownerAuth)
        self.endorseAuth_input.WriteText(exec_cmd.endorseAuth)
        self.lockoutAuth_input.WriteText(exec_cmd.lockoutAuth)
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        self.Center()
        self.Show(True)

    def OnClearOwnerAuth(self, evt):
        user_owner = self.ownerAuth_input.GetValue()
        exec_cmd.ownerAuth = user_owner.replace(" ", "")

        if (exec_cmd.ownerAuth != ""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_changeauth",
                "-c","o",
                "-p", exec_cmd.ownerAuth,
            ])
            self.parent.text_display.AppendText(str(command_output))
            self.parent.text_display.AppendText("'tpm2_changeauth -c o -p " + exec_cmd.ownerAuth + "' executed \n")
            self.parent.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")
            
    def OnClearEndorseAuth(self, evt):
        user_endorse = self.endorseAuth_input.GetValue()
        exec_cmd.endorseAuth = user_endorse.replace(" ", "")
        if (exec_cmd.endorseAuth != ""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_changeauth",
                "-c", "e",
                "-p", exec_cmd.endorseAuth,
            ])
            self.parent.text_display.AppendText(str(command_output))
            self.parent.text_display.AppendText("'tpm2_changeauth -c e -p " + exec_cmd.endorseAuth + "' executed \n")
            self.parent.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnClearLockoutAuth(self, evt):
        user_lockout = self.lockoutAuth_input.GetValue()
        exec_cmd.lockoutAuth = user_lockout.replace(" ", "")
        if (exec_cmd.lockoutAuth != ""):
            command_output = exec_cmd.execTpmToolsAndCheck([
                "tpm2_changeauth",
                "-c", "l",
                "-p", exec_cmd.lockoutAuth,
            ])
            self.parent.text_display.AppendText(str(command_output))
            self.parent.text_display.AppendText("'tpm2_changeauth -c l -p " + exec_cmd.lockoutAuth + "' executed \n")
            self.parent.text_display.AppendText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnCloseWindow(self, evt):
        self.EndModal(-1)
        self.Destroy()

    def OnOK(self, evt):
        user_owner = self.ownerAuth_input.GetValue()
        user_endorse = self.endorseAuth_input.GetValue()
        user_lockout = self.lockoutAuth_input.GetValue()
        exec_cmd.ownerAuth = user_owner.replace(" ", "")
        exec_cmd.endorseAuth = user_endorse.replace(" ", "")
        exec_cmd.lockoutAuth = user_lockout.replace(" ", "")
        self.EndModal(1)
        self.Destroy()


# Very Specific Dialog for Tab 1, Dictionary Attack Settings
class DictAttackDlg(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title=title)
        self.SetBackgroundColour(wx.WHITE)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        
        # attach the sizers to the main sizer
        mainsizer.Add(sizer_1, 0, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(sizer_2, 0, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(sizer_3, 0, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(sizer_4, 0, wx.EXPAND | wx.ALL, 5)

        # instantiate the objects
        self.maxAuthFail_input = wx.TextCtrl(self, -1)
        maxAuthFail_input_blurb = wx.StaticText(self, -1, "TPM will be in Lockout Mode when failed attempts reaches this number\n (default/max = 0x20, or 32): ")
        self.lockoutInterval_input = wx.TextCtrl(self, -1)
        lockoutInterval_input_blurb = wx.StaticText(self, -1, "No. of seconds it takes to decrement the failed attempts counter\n (2^32-1 prevents exit from Lockout Mode)(Default is 0x1C20, or 7200): ")
        self.lockoutRecovery_input = wx.TextCtrl(self, -1)
        lockoutRecovery_input_blurb = wx.StaticText(self, -1, "Delay in seconds between attempts to use LockoutAuth\n (0 indicates a system reboot is required instead)(Default is 0x15180, or 86400): ")
        button_ok = wx.Button(self, -1, 'OK')
        button_cancel = wx.Button(self, -1, 'CANCEL')
        # attach the ui elements to the internal sizer
        #mainsizer.Add(button_ok, 0, wx.ALL, 5)
        sizer_1.Add(maxAuthFail_input_blurb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer_1.Add(self.maxAuthFail_input, 1, wx.EXPAND | wx.ALL, 5)
        sizer_2.Add(lockoutInterval_input_blurb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer_2.Add(self.lockoutInterval_input, 1, wx.EXPAND | wx.ALL, 5)
        sizer_3.Add(lockoutRecovery_input_blurb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer_3.Add(self.lockoutRecovery_input, 1, wx.EXPAND | wx.ALL, 5)
        sizer_4.Add(button_cancel, 0, wx.EXPAND | wx.ALL, 5)
        sizer_4.Add(button_ok, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        # set defaults
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnOK, button_ok)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, button_cancel)
        
        self.maxAuthFail_input.WriteText("32")
        self.lockoutInterval_input.WriteText("7200")
        self.lockoutRecovery_input.WriteText("86400")
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)

    def OnCloseWindow(self, evt):
        self.EndModal(-1)
        self.Destroy()

    def OnOK(self, evt):
        max_auth_fail = self.maxAuthFail_input.GetValue()
        lockout_interval = self.lockoutInterval_input.GetValue()
        lockout_recovery = self.lockoutRecovery_input.GetValue()
        try:
            int(max_auth_fail)
            t1.tpm2_max_auth_fail = max_auth_fail
        except ValueError:
            t1.tpm2_max_auth_fail = None
            return

        try:
            int(lockout_interval)
            t1.tpm2_lockout_interval = lockout_interval
        except ValueError:
            t1.tpm2_lockout_interval = None
            return

        try:
            int(lockout_recovery)
            t1.tpm2_lockout_recovery = lockout_recovery
        except ValueError:
            t1.tpm2_lockout_recovery = None
            return
        self.EndModal(1)
        self.Destroy()


# Very Specific Warning Dialog for Platform Clear
class ClearWarningDlg(wx.MessageDialog):
    def __init__(self, parent, title):
        wx.MessageDialog.__init__(self, parent, message="", caption=title, style=wx.OK | wx.ICON_WARNING|wx.CANCEL)

        self.SetMessage("WARNING, this command will:\n\n\
        1. Flush ALL objects in persistent and volatile memory in Owner and Endorsement Hierarchies\n\
        2. Set owner/endorse/lockout Authorisations to null\n\n\
        ARE YOU SURE?")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.EndModal(-1)
        self.Destroy()
        
# Message Dialog when IFX TPM not found
class Not_IFX_TPM_Dlg(wx.MessageDialog):
    def __init__(self, parent, title):
        wx.MessageDialog.__init__(self, parent, message="", caption=title, style=wx.OK | wx.ICON_WARNING)
        self.SetMessage("Please insert SLB9670 IRIDIUM board, more infor at:\n https://www.infineon.com/cms/en/product/evaluation-boards/iridium9670-tpm2.0-linux")
       
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.EndModal(-1)
        self.Destroy()




# Generic File Editor for AWS Cloud connectivity (for tab6 use)
class EditorFrame(wx.Dialog):
    def __init__(self, parent, title, filename):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title=title)
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        self.editor = wx.TextCtrl(self, 1, size=wx.Size(800, 600), style=wx.TE_MULTILINE)
        mainsizer.Add(self.editor)
        self.filename = filename
        # Open the file, read the contents and set them into
        # the text edit window
        filehandle = open(self.filename, 'r')
        self.editor.SetValue(filehandle.read())
        filehandle.close()

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        mainsizer.Fit(self)
        self.Centre(wx.BOTH)
        self.Show()

    def OnCloseWindow(self, evt):
        # Save away the edited text
        # Open the file, do a check for an overwrite!
        user_input = wx.MessageDialog(
            self,
            "Yes: Overwrite jsn file. \nNo: No changes shall be made. \n",
            "Warning!",
            wx.YES_NO)
        if (user_input.ShowModal() == wx.ID_YES):
            # Grab the content to be saved
            text_to_overwrite = self.editor.GetValue()

            filehandle = open(self.filename, 'w')
            filehandle.write(text_to_overwrite)
            filehandle.close()
        # Get rid of the dialog to keep things tidy
        user_input.Destroy()
        self.Destroy()


# Dialog for asking user input for ownerAuth for the purpose of removing OwnerAuth for Engine Usage
class EngineDlg(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title=title, size=(500, 250))
        self.SetBackgroundColour(wx.WHITE)

        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        # attach the sizers to the main sizer
        mainsizer.Add(wx.StaticText(self, -1, "ALL TPM Engine features require ownerAuth to be set to NULL.\n\
To set ownerAuth to NULL, fill in the ownerAuth value in the text box.\n\
If the field is left blank, no action will be taken and you will still proceed.\n"), 1, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(sizer_1, 0, wx.ALL, 5)
        mainsizer.Add(wx.StaticText(self, -1, "All spaces will be stripped, if any"), 0, wx.ALL, 5)

        # instantiate the objects
        self.ownerAuth_input = wx.TextCtrl(self, -1)
        ownerAuth_input_blurb = wx.StaticText(self, -1, "Owner Authorisation Value: ")
        button_ok = wx.Button(self, -1, 'OK')

        # attach the ui elements to the internal sizer
        mainsizer.Add(button_ok, 0, wx.ALL, 5)
        sizer_1.Add(ownerAuth_input_blurb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer_1.Add(self.ownerAuth_input, 1, wx.ALL, 5)

        # set defaults
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnOK, button_ok)
        self.SetSizer(mainsizer)
        self.Show(True)

    def OnCloseWindow(self, evt):
        self.EndModal(-1)
        self.Destroy()

    def OnOK(self, evt):
        user_owner = self.ownerAuth_input.GetValue()
        if (user_owner != ""):
            exec_cmd.execTpmToolsAndCheck([
                "tpm2_changeauth",
                "-O", user_owner,
            ])
        self.EndModal(1)
        self.Destroy()


# Warning Dialog for AWS Region mis-match
# Note by default the AWS C application is set to us-east-1.
class AwsRegionWarning(wx.MessageDialog):
    def __init__(self, parent, title):
        wx.MessageDialog.__init__(self, parent, message="", caption=title, style=wx.OK | wx.ICON_WARNING)

        self.SetMessage("WARNING, as you have set the AWS region to a NON us-east-1 region, when attempting to publish to the AWS Cloud, the application will crash.\n\n\
To fix this problem:\n\
    Edit the file, 'aws_iot_config.h' in /aws_tpm20/sample_apps/eHealthTPM3/eHealthDevice, and edit the value AWS_IOT_MQTT_HOST with the correct endpoint.\n\
    Or, just use the AWS region us-east-1.")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.EndModal(-1)
        self.Destroy()
