import wx
import tab1_setup as t1
import tab2_crypto as t2
import tab3_engine as t3
import tab4_policy as t4
import tab5_attest as t5
import tab6_cloud as t6
import misc_dialogs as misc
import shell_util as exec_cmd
import images as img
import subprocess

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="Main Window", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.SetBackgroundColour(wx.WHITE)
        self.Centre(wx.BOTH)
        # Set Font for frame, so all buttons will inherit this, so it saves time
        main_menu_font = wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)

        # Create all the button widgets first
        self.button1 = wx.Button(self, -1, 'Setup and Basic Features')
        self.button2 = wx.Button(self, -1, 'Cryptographic Functions')
        self.button3 = wx.Button(self, -1, 'OpenSSL-Engine')
        self.button4 = wx.Button(self, -1, 'Data Sealing with Policy')
        self.button5 = wx.Button(self, -1, 'Attestation')
        self.button6 = wx.Button(self, -1, 'AWS: IOT Core')
        # Title screen widget setup
        # "\xe2\x84\xa2" represents the Trademark symbol in UTF-8 for Python 2.x, will not display properly on Windows (or Python 3.x)
        title_screen = wx.StaticText(self, -1, style=wx.ALIGN_CENTER, label="OPTIGA\xe2\x84\xa2 TPM 2.0 Explorer")
        font = wx.Font(30, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_screen.SetFont(font)
        # TPM Image
        tpm_image = wx.Image('../images/tpm_slb_9670.png', wx.BITMAP_TYPE_PNG)
        tpm_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tpm_image))
        # ~ tpm_image = wx.StaticBitmap(self, wx.ID_ANY, img.tpm_slb_9670.getBitmap())

        # IFX Logo
        ifx_image = wx.Image('../images/250px-Infineon-Logo.png', wx.BITMAP_TYPE_PNG)
        ifx_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(ifx_image))
        # ~ ifx_image = wx.StaticBitmap(self, wx.ID_ANY, img._250px_Infineon_Logo.getBitmap())    
        
        # Setup logo
        tab1_image = wx.Image('../images/setup.png', wx.BITMAP_TYPE_PNG)
        tab1_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab1_image))
        # ~ tab1_image = wx.StaticBitmap(self, wx.ID_ANY, img.setup.getBitmap())

        # Crypto logo
        tab2_image = wx.Image('../images/crypto.png', wx.BITMAP_TYPE_PNG)
        tab2_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab2_image))
        # ~ tab2_image = wx.StaticBitmap(self, wx.ID_ANY, img.crypto.getBitmap())

        # Engine logo
        tab3_image = wx.Image('../images/engine.png', wx.BITMAP_TYPE_PNG)
        tab3_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab3_image))
        # ~ tab3_image = wx.StaticBitmap(self, wx.ID_ANY, img.engine.getBitmap())

        # Cloud logo
        tab6_image = wx.Image('../images/cloud.png', wx.BITMAP_TYPE_PNG)
        tab6_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab6_image))
        # ~ tab6_image = wx.StaticBitmap(self, wx.ID_ANY, img.cloud.getBitmap())
   
        # Attestation logo
        tab5_image = wx.Image('../images/attest.png', wx.BITMAP_TYPE_PNG)
        tab5_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab5_image))
        # ~ tab5_image = wx.StaticBitmap(self, wx.ID_ANY, img.attest.getBitmap())
        
        # Policy logo
        tab4_image = wx.Image('../images/policy.png', wx.BITMAP_TYPE_PNG)
        tab4_image = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(tab4_image))
        # ~ tab4_image = wx.StaticBitmap(self, wx.ID_ANY, img.policy.getBitmap())

        # declare the sizer
        mainsizer = wx.GridSizer(cols=3, vgap=5, hgap=5)

        # add the widgets to the sizers (add row by row)
        mainsizer.Add(tpm_image, 0, wx.ALIGN_LEFT | wx.ALIGN_TOP, 5)
        mainsizer.Add(title_screen, 0, wx.ALIGN_CENTRE, 0)
        mainsizer.Add(ifx_image, 0, wx.ALIGN_RIGHT | wx.ALIGN_TOP, 5)

        mainsizer.Add(tab1_image, 0, wx.ALIGN_CENTRE | wx.TOP, 50)
        mainsizer.Add(tab2_image, 0, wx.ALIGN_CENTRE | wx.TOP, 50)
        mainsizer.Add(tab3_image, 0, wx.ALIGN_CENTRE | wx.TOP, 50)

        mainsizer.Add(self.button1, 1, wx.EXPAND | wx.ALL, 30)
        mainsizer.Add(self.button2, 1, wx.EXPAND | wx.ALL, 30)
        mainsizer.Add(self.button3, 1, wx.EXPAND | wx.ALL, 30)

        mainsizer.Add(tab4_image, 0, wx.ALIGN_CENTRE | wx.TOP, 50)
        mainsizer.Add(tab5_image, 0, wx.ALIGN_CENTRE | wx.TOP, 50)
        mainsizer.Add(tab6_image, 0, wx.ALIGN_CENTRE | wx.TOP, 50)

        mainsizer.Add(self.button4, 1, wx.EXPAND | wx.ALL, 30)
        mainsizer.Add(self.button5, 1, wx.EXPAND | wx.ALL, 30)
        mainsizer.Add(self.button6, 1, wx.EXPAND | wx.ALL, 30)

        mainsizer.Add((120, 80))
        mainsizer.Add((120, 80))
        mainsizer.Add((120, 80))

        # Bind events
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button2)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button3)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button4)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button5)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button6)

        # Set tooltips
        self.button1.SetToolTip(wx.ToolTip("Take ownership here."))
        self.button2.SetToolTip(wx.ToolTip("Hashing, Encryption, Decryption, Verification & Signing"))
        self.button3.SetToolTip(wx.ToolTip("Using TPM and OpenSSL to establish a client-server connection"))
        self.button4.SetToolTip(wx.ToolTip("Making use of policies to seal and unseal objects"))
        self.button5.SetToolTip(wx.ToolTip("Using endorsement key hierarchies to prove/attest"))
        self.button6.SetToolTip(wx.ToolTip("Example use-case with AWS"))

        self.SetSizer(mainsizer)
        self.Show(True)
        self.Check_IFX_TPM()
        
    def Check_IFX_TPM(self):
            cmd =" ls /dev/tpm0"
            ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            command_output = ps_command.stdout.read()
            retcode = ps_command.wait()
            if( command_output.decode() != "/dev/tpm0\n"):
                misc.Not_IFX_TPM_Dlg(self, "TPM Device Not Found").ShowModal()
                self.Disable_Buttons()              
                return
                        

            cmd =" tpm2_getcap properties-fixed | grep -A2 'MANUFACTURER' | grep value | grep -Eo '[A-Z]*'"
            ps_command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            command_output = ps_command.stdout.read()
            print(command_output)
            retcode = ps_command.wait()
            if (not "IFX" in command_output.decode()):
                misc.Not_IFX_TPM_Dlg(self, "Insert Infineon IRIDIUM Module").ShowModal()
                self.Disable_Buttons()    
                return    
    def Disable_Buttons(self):
            self.button1.Disable()
            self.button2.Disable()
            self.button3.Disable()
            self.button4.Disable()
            self.button5.Disable()
            self.button6.Disable()
                    

    def OnCloseWindow(self, evt):
        self.Destroy()

    # Technically this can be split into 6 different functions but I prefer it this way
    # The EngineDlg is required as the functions in tab3 and tab6 require the ownerAuth of the TPM to be set to NULL.
    def OnButtonClick(self, evt):
        event_obj = evt.GetEventObject()
        if (event_obj == self.FindWindowByLabel(label='Setup and Basic Features')):
            self.activetab = t1.Tab1Frame(self, "Basic")
        elif (event_obj == self.FindWindowByLabel(label='Cryptographic Functions')):
            self.activetab = t2.Tab2Frame(self, "Crypto")
        elif (event_obj == self.FindWindowByLabel(label='OpenSSL-Engine')):
            #~ if (misc.EngineDlg(self, "Warning!").ShowModal() == -1):
                #~ return
            self.activetab = t3.Tab3Frame(self, "Engine")
        elif (event_obj == self.FindWindowByLabel(label='Data Sealing with Policy')):
            self.activetab = t4.Tab4Frame(self, "Data Sealing with Policy")
        elif (event_obj == self.FindWindowByLabel(label='Attestation')):
            self.activetab = t5.Tab5Frame(self, "Attest")
        elif (event_obj == self.FindWindowByLabel(label='AWS: IOT Core')):
            #~ if (misc.EngineDlg(self, "Warning!").ShowModal() == -1):
                #~ return
            self.activetab = t6.Tab6Frame(self, 'Cloud')
        else:
            return
        self.Hide()


class Main(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        dlg = MainFrame(None, title="Main")
        dlg.Show()


# Always executes as this is the main file anyway
# Note: This changes the working directory to /working_space, thus all created objects will be there
# Navigation always starts from the /working_space folder.
if __name__ == "__main__":
    exec_cmd.checkDir()
    app = Main()
    app.MainLoop()
