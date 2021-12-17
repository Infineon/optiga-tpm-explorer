import wx


# Info for tab1_handles
class HandlesInfoDlg(wx.MessageDialog):
    def __init__(self, parent, title):
        wx.MessageDialog.__init__(self, parent, message="", caption=title, style=wx.OK | wx.ICON_INFORMATION)
        self.SetMessage("Object Handles are in hex, and are 4 bytes (32 bits) long. E.g. 0x8100000F\n\nTransient Object Handles:\n\
Any TPM Object is assigned a handle when it is loaded or when evicted from the TPM Persistent store.\n\
All transient objects are stored in TPM RAM, and are flushed on TPM2_Startup.\n\
Transient Objects Handles always start with the hex value 0x80.\n\nPersistent Object Handles:\n\
TPM2_EvictControl can make a Persistent TPM Object into a Transient one, and vice versa.\n\
A Persistent Object is stored in the TPM's Non-volatile Memory, and is NOT cleared by TPM2_Startup.\n\
Persistent Object Handles always start with the hex value 0x81.\n\
Note that converting a Transient handle to a Persistent one, can be done in the Attestation tab, where you can create multiple Attestation keys with different handles.\n\
NOTE: Performing this operation (TPM2_EvictControl) requires either Owner or Platform Authorisation.\n\nFrom Trusted Computing Group TPM 2.0 Part 1: Architecture, Section 15.6, 15.7, 16.")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.Destroy()


# Info for tab4_policy
class PolicyInfoDlg(wx.MessageDialog):
    def __init__(self, parent, title):
        wx.MessageDialog.__init__(self, parent, message="", caption=title, style=wx.OK | wx.ICON_INFORMATION)
        self.SetMessage("Enhanced Authorisation(EA):\n\
EA allows users to require specific tests or actions to be performed before an action can be done.\n\
Step 1: In this case, the policy is created. To fulfil the policy, the specified PCR bank has to have a certain value at the time of policy creation.\n\
Step 2: Creation of a primary (if not already done) is required for a creation of a leaf key to be used in sealing and unsealing.\n\
Step 3: The sealing step involves the creation of a keypair under the Owner Hierarchy. That keypair is immediately used in sealing the secret values.\n\
Step 4: The key-pair then cannot be used (to unseal) until the Policy is fulfilled, which requires a PCR bank to the specific value.\n\
A policy defines the conditions for use of an entity, and can be very complex:\n\
    a) A policy can only have 1 condition (e.g. in this case, a specific value in a specific PCR bank)\n\
    b) Multiple conditions which ALL must be fulfilled (Policy AND)\n\
    c) Multiple conditions which only ONE is enough to be fulfilled (Policy OR)\n\
    d) Or a complex chain of conditions (e.g. OR->AND->OR)\n\
Policy conditions can vary, some are here:\n\
    a) TPM2_PolicyPCR: Fulfilled if a PCR bank has a specific value (this use case)\n\
    b) TPM2_PolicyAuthorise: Fulfilled if the policy is signed by a designated authority's signing key.\n\
    c) TPM2_PolicyAuthoriseNV: Fulfilled if the designated NV index contains a digest value that matches.\n\
    d) TPM2_PolicyAuthValue: Fulfilled if the correct authorisation value is given (i.e. Owner, Endorsement, Platform).\n\
    e) TPM2_PolicyPassword: Fulfilled if the correct password is given.(NOT Owner, Endorse, Platform)\n\n\
From Trusted Computing Group TPM 2.0 Part 1: Architecture, Section 19.7.")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.Destroy()


# Info for tab1_setup
class SetupInfoDlg(wx.MessageDialog):
    def __init__(self, parent, title):
        wx.MessageDialog.__init__(self, parent, message="", caption=title, style=wx.OK | wx.ICON_INFORMATION)
        self.SetMessage("From Trusted Computing Group TPM 2.0 Part 1: Architecture, Section 15.6, 15.7, 16.")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.Destroy()


# Info for tab5_attest
class AttestationInfoDlg(wx.MessageDialog):
    def __init__(self, parent, title):
        wx.MessageDialog.__init__(self, parent, message="", caption=title, style=wx.OK | wx.ICON_INFORMATION)
        self.SetMessage("Attestation:\n\
Attestation is act of having the TPM sign some internal TPM data.\n\
Setup: Pick a PCR bank that the TPM will sign upon. Create an Endorsement Key (EK) if not already done so.\n\
Step 1: Create an Attestation Key (AK) from the EK. The user may enter in any appropriate handle, or use the default one.\n\
Step 2: Generate a quote, which uses the AK to sign the hashed value in the specified PCR bank. The signing algorithm used in this example is RSASSA.\n\
Step 3: The generated signature, with the quote, can be verified elsewhere using OpenSSL or with another TPM.\n\n\
The key that used to sign can be:\n\
    a) an key under the Endorsement Hierachy (Attestation keys)\n\
    b) any external key\n\
    c) a restricted signing key created on the TPM (with the corresponding certificate from the manufacturer).\n\n\
The TPM can sign:\n\
    a) PCR data (TPM2_Quote)(Used in this test case)\n\
    b) Clock/Time data\n\
    c) Other TPM objects (TPM2_Certify)\n\n\
From Trusted Computing Group TPM 2.0 Part 1: Architecture, Section 31.")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.Destroy()


# Info for tab6_cloud
class CloudDemoInfoDlg(wx.MessageDialog):
    def __init__(self, parent, title):
        wx.MessageDialog.__init__(self, parent, message="", caption=title, style=wx.OK | wx.ICON_INFORMATION)
        self.SetMessage("TPM Use Case with Amazon Web Services Internet-of-Things (AWS IoT):\n\
This tab is where the usage of the TPM is shown, in a use-case involving the AWS IoT service.\n\n\
Setting up:\n\
Users are required to login or setup their AWS credentials through the AWS Command Line Interface or in this tab.\n\
After setting up, the user can click the '1-click provision' button to register this device to AWS.\n\
After provisioning, the user can now publish data to the AWS Cloud. In this case the data is a value from 1 to 200.")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        self.Destroy()
