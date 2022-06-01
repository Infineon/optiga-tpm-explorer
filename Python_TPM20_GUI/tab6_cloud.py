import wx
import shell_util as exec_cmd
import misc_dialogs as misc
import info_dialogs as info
import json
import images as img
# from wx.lib.pubsub import setuparg1
# from wx.lib.pubsub import pub as Publisher
from pubsub import pub as Publisher
import threading
from threading import Thread
aws_log = None
aws_region_list = [
    'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ap-south-1',
    'ap-northeast-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2',
    'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1',
    'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1']


class Tab6Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title="AWS: IOT Core", size=(1280, 720), style=(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)))
        self.Centre(wx.BOTH)
        self.SetBackgroundColour(wx.WHITE)
        main_menu_font = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(main_menu_font)

        # Threads related objects
        self.AWS_thread_active_flag=0
        self.aws_proc=None
         
        # declare the sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        imagesizer = wx.BoxSizer(wx.HORIZONTAL)
        self.middlesizer = wx.BoxSizer(wx.HORIZONTAL)
        inside_middlesizer_1 = wx.BoxSizer(wx.VERTICAL)
        inside_middlesizer_2 = wx.BoxSizer(wx.VERTICAL)
        inside_middlesizer_3 = wx.BoxSizer(wx.VERTICAL)
        extrasizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsizer = wx.BoxSizer(wx.VERTICAL)
        aws_sizer = wx.BoxSizer(wx.VERTICAL)
        aws_region_sizer = wx.BoxSizer(wx.HORIZONTAL)
        setawssizer = wx.BoxSizer(wx.HORIZONTAL)
        
        mini_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        publish_sizer = wx.BoxSizer(wx.HORIZONTAL)
        publish_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # instantiate the objects
        self.bottom_txt_display = wx.TextCtrl(self, -1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        self.bottom_txt_display.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.aws_region_box = wx.ComboBox(self, -1, "Pick the AWS Region", choices=aws_region_list, style=wx.CB_READONLY, size=(150, -1))
        # Images
        user = wx.Image('../images/6user.png', wx.BITMAP_TYPE_PNG)
        user = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(user), pos=(250, 10))
        # ~user = wx.StaticBitmap(self, wx.ID_ANY, img._6user.getBitmap(), pos=(180, 10))
        
        product = wx.Image('../images/6products.png', wx.BITMAP_TYPE_PNG)
        product = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(product), pos=(565, 7))
        # ~product = wx.StaticBitmap(self, wx.ID_ANY, img._6products.getBitmap(), pos=(495, 10))
        
        cloud = wx.Image('../images/6cloud.png', wx.BITMAP_TYPE_PNG)
        cloud = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(cloud), pos=(915, 8))
        # ~cloud = wx.StaticBitmap(self, wx.ID_ANY, img._6cloud.getBitmap(), pos=(845, 10))
        
        arrow = wx.Image('../images/6forward.png', wx.BITMAP_TYPE_PNG)
        arrow = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(arrow), pos=(435, 67))
        # ~arrow = wx.StaticBitmap(self, wx.ID_ANY, img._6forward.getBitmap(), pos=(365, 67))
        
        arrow2 = wx.Image('../images/6exchange.png', wx.BITMAP_TYPE_PNG)
        arrow2 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(arrow2), pos=(770, 49))
        # ~arrow2 = wx.StaticBitmap(self, wx.ID_ANY, img._6exchange.getBitmap(), pos=(700, 49))

        # Create Buttons
        button_oneclick = wx.Button(self, -1, '1-click provision (Step 1-6)')
        button_startconnection = wx.Button(self, -1, 'Start publishing')
        button_configureAWS = wx.Button(self, -1, 'Set AWS credentials', size = (256, -1))
        button_openconfigfile = wx.Button(self, -1, 'Open config file')
        button_openpolicyfile = wx.Button(self, -1, 'Open policy file')
        button_createpolicy = wx.Button(self, -1, 'Create Policy (from policy file)')
        # clear image
        clearimage = wx.Image('../images/clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        clearbutton = wx.BitmapButton(self, -1, clearimage)
        # ~clearbutton = wx.BitmapButton(self, -1, img.clear.getBitmap())
        
        # info image button
        infoimage = wx.Image('../images/info.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        infobutton = wx.BitmapButton(self, -1, infoimage)
        # ~infobutton = wx.BitmapButton(self, -1, img.info.getBitmap())

        # back image
        backimage = wx.Image('../images/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        backbutton = wx.BitmapButton(self, -1, backimage)
        # ~backbutton = wx.BitmapButton(self, -1, img.back.getBitmap())
        
        # Create static text boxes for each step
        self.text_step1 = wx.StaticText(self, -1, "Step 1: Create Key Pair")
        self.text_step2 = wx.StaticText(self, -1, "Step 2: Create Certificate Signing Request")
        self.text_step3 = wx.StaticText(self, -1, "Step 3: Create AWS IoT Thing")
        self.text_step4 = wx.StaticText(self, -1, "Step 4: Create Certificate")
        self.text_step5 = wx.StaticText(self, -1, "Step 5: Attach Certificate to Thing")
        self.text_step6 = wx.StaticText(self, -1, "Step 6: Attach Policy to Certificate")
        self.text_step7 = wx.StaticText(self, -1, "Step 7: Connect && start publishing")
        self.aws_key_input = wx.TextCtrl(self, -1)
        self.aws_secret_input = wx.TextCtrl(self, -1)
        self.aws_session_input = wx.TextCtrl(self, -1)
        self.aws_endpoint = wx.TextCtrl(self, -1)
        
        self.text_mqtt_topic = wx.StaticText(self, -1, label="Topic")
        self.text_mqtt_message = wx.StaticText(self, -1, label="Data")
        
        self.publish_input_one = wx.TextCtrl(self, -1,value="SPO2: 96, BPM: 60")
        #~ self.publish_input_two = wx.TextCtrl(self, -1)
        self.publish_topic=wx.TextCtrl(self, -1,value="pulsioximeter")

        # attach the sizers to the main sizer
        mainsizer.Add(imagesizer, 0, wx.EXPAND | wx.ALL, 0)
        mainsizer.Add(self.middlesizer, 0, wx.EXPAND | wx.ALL, 0)
        mainsizer.Add(extrasizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        mainsizer.Add(bottomsizer, 1, wx.EXPAND | wx.ALL, 0)
        self.middlesizer.Add(inside_middlesizer_1, 1, wx.EXPAND | wx.LEFT, 0)
        self.middlesizer.Add(inside_middlesizer_2, 1, wx.EXPAND | wx.ALL, 0)
        self.middlesizer.Add(inside_middlesizer_3, 1, wx.EXPAND | wx.ALL, 0)
        bottomsizer.Add(buttonsizer, 0, wx.EXPAND | wx.ALL, 0)
        bottomsizer.Add(self.bottom_txt_display, 1, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        # attach the ui elements to the internal sizer
        imagesizer.Add((50, 190))

        inside_middlesizer_1.Add(aws_sizer, 0, wx.EXPAND | wx.TOP, 25)
        inside_middlesizer_2.AddSpacer(15)
        inside_middlesizer_2.Add(self.text_step1, 0, wx.EXPAND | wx.RIGHT | wx.LEFT | wx.BOTTOM, 5)
        inside_middlesizer_2.Add(self.text_step2, 0, wx.EXPAND | wx.ALL, 5)
        inside_middlesizer_2.Add(self.text_step7, 0, wx.EXPAND | wx.ALL, 5)
        inside_middlesizer_2.Add(publish_sizer, 0, wx.EXPAND | wx.ALL, 5)
        #inside_middlesizer_2.AddSpacer(1)
        ##inside_middlesizer_2.Add(button_startconnection, 0, wx.ALL, 5)
        
        inside_middlesizer_3.AddSpacer(15)
        inside_middlesizer_3.Add(self.text_step3, 0, wx.EXPAND | wx.RIGHT | wx.LEFT | wx.BOTTOM, 5)
        inside_middlesizer_3.Add(self.text_step4, 0, wx.EXPAND | wx.ALL, 5)
        inside_middlesizer_3.Add(self.text_step5, 0, wx.EXPAND | wx.ALL, 5)
        inside_middlesizer_3.Add(self.text_step6, 0, wx.EXPAND | wx.ALL, 5)
        ##inside_middlesizer_3.Add(self.aws_endpoint, 0, wx.EXPAND | wx.ALL, 5)

        publish_sizer.Add(self.text_mqtt_topic, 0, wx.ALIGN_CENTRE, 5)
        publish_sizer.Add(self.publish_topic, 1,  wx.EXPAND | wx.ALL, 5)
        publish_sizer.Add(self.text_mqtt_message, 0, wx.ALIGN_CENTRE, 5)
        publish_sizer.Add(self.publish_input_one, 1, wx.EXPAND | wx.ALL, 5)
        #~ publish_sizer.Add(self.publish_input_two, 0, wx.EXPAND | wx.ALL, 5)
        
        #~ buttonsizer.Add(button_configureAWS, 1, wx.EXPAND | wx.ALL, 5)

        #~ buttonsizer.Add(button_startconnection, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(button_openconfigfile, 1, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        buttonsizer.Add(button_openpolicyfile, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(button_createpolicy, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(button_oneclick, 1, wx.EXPAND | wx.ALL, 5)
        buttonsizer.Add(mini_button_sizer, 1, wx.EXPAND | wx.ALL, 0)
        mini_button_sizer.Add(clearbutton, 0, wx.ALL, 5)
        mini_button_sizer.Add(infobutton, 0, wx.ALL, 5)
        mini_button_sizer.Add(backbutton, 0, wx.ALL, 5)

        aws_region_sizer.Add(self.aws_region_box, 0, wx.EXPAND | wx.ALL, 5)
        aws_region_sizer.Add(button_configureAWS, 1, wx.EXPAND | wx.ALL, 5)
        
        setawssizer.Add(button_startconnection, 1, wx.EXPAND | wx.ALL, 0)
        
        aws_sizer.Add(self.aws_key_input, 2, wx.EXPAND | wx.ALL, 5)
        aws_sizer.AddSpacer(2)
        aws_sizer.Add(self.aws_secret_input, 2, wx.EXPAND | wx.ALL, 5)
        aws_sizer.AddSpacer(2)
        aws_sizer.Add(self.aws_session_input, 2, wx.EXPAND | wx.ALL, 5)
        
        extrasizer.Add(aws_region_sizer, 0, wx.EXPAND | wx.ALL, 0)
        extrasizer.Add(setawssizer, 0, wx.ALL, 5)
        extrasizer.Add(self.aws_endpoint, 1, wx.EXPAND | wx.ALL, 5)
        #extrasizer.AddSpacer(227)
        extrasizer.AddSpacer(80)
        #~ aws_sizer.Add(self.aws_region_box, 0, wx.EXPAND | wx.ALL, 5)
        ##aws_sizer.Add(self.aws_endpoint, 0, wx.EXPAND | wx.ALL, 5)     

        # Set tooltips
        button_configureAWS.SetToolTip(wx.ToolTip("If your AWS Command Line Interface (CLI) has not been configured, this buttton can do it, but it is highly recommended to do it yourself."))
        button_oneclick.SetToolTip(wx.ToolTip("This button will automatically register this device to your AWS gateway. This might take a while."))
        button_startconnection.SetToolTip(wx.ToolTip("This button will publish the value in the input box to AWS."))
        button_openconfigfile.SetToolTip(wx.ToolTip("This will open a text editor containing values that you may want to edit, if applicable. The values will be used in the 1-click provision."))
        clearbutton.SetToolTip(wx.ToolTip("Clear all textboxes."))

        # declare and bind events
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnOneClick, button_oneclick)
        self.Bind(wx.EVT_BUTTON, self.OnStartConnection, button_startconnection)
        self.Bind(wx.EVT_BUTTON, self.OnConfigureAWS1, button_configureAWS)
        self.Bind(wx.EVT_BUTTON, self.OnOpenConfig, button_openconfigfile)
        self.Bind(wx.EVT_BUTTON, self.OnOpenPolicy, button_openpolicyfile)
        self.Bind(wx.EVT_BUTTON, self.OnCreatePolicy1, button_createpolicy)
        self.Bind(wx.EVT_BUTTON, self.OnClear, clearbutton)
        self.Bind(wx.EVT_BUTTON, self.OnInfo, infobutton)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, backbutton)

       # Setup Publisher for text field update
        Publisher.subscribe(self.Upd_Cloud_Status, "AWS_Cloud_Text")

        # set default values
        self.aws_key_input.SetHint("AWS Access Key here")
        self.aws_secret_input.SetHint("AWS Secret Access Key here")
        self.aws_session_input.SetHint("AWS Session Token for SSO Device here")
        self.aws_endpoint.SetHint("Endpont in Config file")
        
        #~ self.publish_input_one.write("100")
        #~ self.publish_input_two.write("100")
        self.aws_region_box.SetSelection(0)

        self.SetSizer(mainsizer)
        self.Show(True)

    def monitor_process_thread(self):
        
        try:    
            while self.AWS_thread_active_flag==1 :
                line = self.aws_proc.stdout.readline()
                if line.decode() != '':
                    wx.CallAfter(Publisher.sendMessage, "AWS_Cloud_Text", msg=line.decode())
                     
        finally:
            
            self.AWS_thread_active_flag=0
            #~ self.aws_proc=None
            print("Exit process AWS process Thread\n")
            #~ wx.CallAfter(Publisher.sendMessage, "AWS_Cloud_Text", msg=" Exit AWS thread..\n")   
                 
    def Upd_Cloud_Status(self,msg):
        self.bottom_txt_display.AppendText(msg)
                
    def OnOneClick(self, evt):
        self.middlesizer.ShowItems(show=False)
        configfile = json.load(open("config.jsn"))
        thingname = configfile["AmazonIoT"]["ThingName"]
        policyname = configfile["AmazonIoT"]["PolicyName"]
        commonname = configfile["CN"]
        organisation = configfile["O"]
        country = configfile["C"]
        countryfullname = configfile["ST"]

        # Clean up
        self.bottom_txt_display.write("Cleaning up and Setting up variables\n")
        self.Update()
        exec_cmd.execCLI(["rm", "leaf.csr", ])
        exec_cmd.execCLI(["rm", "leafAWS.crt", ])
        exec_cmd.execCLI(["rm", "tsa.tss", ])
        # Generate Key Pair
        self.text_step1.Show()
        self.bottom_txt_display.write("Generating key-pair: 'tpm2tss-genkey -a rsa rsa.tss'\n")
        self.Update()
        if (exec_cmd.ownerAuth !=""):
            command_output = exec_cmd.execCLI([
            "tpm2tss-genkey",
            "-o",exec_cmd.ownerAuth,
            "-a", "rsa",
            "rsa.tss",
            ])
        else:
            command_output = exec_cmd.execCLI([
            "tpm2tss-genkey",
            "-a", "rsa",
            "rsa.tss",
        ])
        
 
        self.bottom_txt_display.WriteText(str(command_output))
        self.bottom_txt_display.WriteText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.bottom_txt_display.Update()
        # Create CSR
        self.text_step2.Show()
        self.Update()
        self.bottom_txt_display.write("Create Certificate Signing Request:\n")
        if (exec_cmd.ownerAuth !=""):
            f = open("temp.conf", "w+")
            f.write(exec_cmd.openssl_cnf)
            f.close()

            command_output = exec_cmd.execCLI([
            "openssl",
            "req", "-new",
            "-config","temp.conf",
            "-engine", "tpm2tss",
            "-key", "rsa.tss",
            "-keyform", "engine",
            "-subj", "/CN=" + commonname + "/O=" + organisation + "/C=" + country + "/ST=" + countryfullname,
            "-out", "leaf.csr",
            ])
            self.bottom_txt_display.WriteText(str(command_output))
            self.bottom_txt_display.write("'openssl req -new -config temp.conf -engine tpm2tss -key rsa.tss -keyform engine -subj /CN=$commonname/O=$organisation/C=$country/ST=$countryfullname -out leaf.csr'\n")
        else:
            command_output = exec_cmd.execCLI([
            "openssl",
            "req", "-new",
            "-engine", "tpm2tss",
            "-key", "rsa.tss",
            "-keyform", "engine",
            "-subj", "/CN=" + commonname + "/O=" + organisation + "/C=" + country + "/ST=" + countryfullname,
            "-out", "leaf.csr",
            ])
            self.bottom_txt_display.WriteText(str(command_output))
            self.bottom_txt_display.write("'openssl req -new -engine tpm2tss -key rsa.tss -keyform engine -subj /CN=$commonname/O=$organisation/C=$country/ST=$countryfullname -out leaf.csr'\n")
                

        self.bottom_txt_display.WriteText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.bottom_txt_display.Update()


        # Create IoT Thing
        self.text_step3.Show()
        self.Update()
        self.bottom_txt_display.write("Create AWS IoT Thing: 'aws iot create-thing --thing-name $thingname'\n")
        command_output = exec_cmd.execCLI([
            "aws",
            "iot", "create-thing",
            "--thing-name", thingname,
        ])
        self.bottom_txt_display.WriteText(str(command_output))
        self.bottom_txt_display.WriteText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.bottom_txt_display.Update()
        # Create Cert
        self.text_step4.Show()
        self.Update()
        self.bottom_txt_display.write("Create Certificate:\n")
        self.bottom_txt_display.write("'aws iot create-certificate-from-csr --certificate-signing-request file://leaf.csr --set-as-active --certificate-pem-outfile leafAWS.crt'\n")
        command_output = exec_cmd.execCLI([
            "aws",
            "iot", "create-certificate-from-csr",
            "--certificate-signing-request", "file://leaf.csr",
            "--set-as-active", "--certificate-pem-outfile",
            "leafAWS.crt",
        ])
        # above command returns a json file with "certificateArn", "certificatePem" and "certificateId"
        temp_json_cert = json.loads(command_output)
        cert_ARN = temp_json_cert["certificateArn"]
        self.bottom_txt_display.WriteText(str(command_output))
        self.bottom_txt_display.WriteText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.bottom_txt_display.Update()
        # Attach cert to thing
        self.text_step5.Show()
        self.Update()
        self.bottom_txt_display.write("Attach Certificate to Thing: 'aws iot attach-thing-principal --thing-name $thingname --principal $certificateArn'\n")
        command_output = exec_cmd.execCLI([
            "aws",
            "iot", "attach-thing-principal",
            "--thing-name", thingname,
            "--principal", cert_ARN,
        ])
        self.bottom_txt_display.WriteText(str(command_output))
        self.bottom_txt_display.WriteText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.bottom_txt_display.Update()
        # Attach policy to cert
        self.text_step6.Show()
        self.Update()
        self.bottom_txt_display.write("Attach Policy to Certificate: 'aws iot attach-principal-policy --policy-name $policyname --principal $certificateArn'\n")
        command_output = exec_cmd.execCLI([
            "aws",
            "iot", "attach-principal-policy",
            "--policy-name", policyname,
            "--principal", cert_ARN,
        ])
        self.bottom_txt_display.WriteText(str(command_output))
        self.bottom_txt_display.WriteText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.middlesizer.ShowItems(show=True)
        self.Update()

    def OnStartConnection(self, evt):
        
        configfile = json.load(open("config.jsn"))
        host_endpoint = configfile["AmazonIoT"]["Endpoint"]
        self.aws_endpoint.SetValue(host_endpoint)
        spo_value = self.publish_input_one.GetValue()
        #~ bpm_value = self.publish_input_two.GetValue()
        topic_value = self.publish_topic.GetValue()
        if (spo_value == "") or (topic_value == ""):
            self.bottom_txt_display.WriteText("Topic or Data Fields can not be empty!\n")
            return
        self.text_step7.Show()
        self.Update()
        #~ command_output = exec_cmd.execCLI([
            #~ "sudo",
            #~ "../eHealthDevice",
            #~ "-m", spo_value,
            #~ "-t", topic_value,
            #~ "-e", host_endpoint,
        #~ ])
        #~ self.bottom_txt_display.WriteText(str(command_output))
        #~ self.bottom_txt_display.WriteText("++++++++++++++++++++++++++++++++++++++++++++\n")

        if (self.aws_proc is not None):
            self.AWS_thread_active_flag=0

            print("Server Thread Active..killing it: %d \n" % self.aws_proc.pid)
            #kill_child_processes(self.aws_proc.pid)

            self.aws_proc.terminate()
            self.aws_proc.wait()
            self.aws_proc = None

            
        aws_cmd="sudo ../eHealthDevice -m \"" +spo_value+ "\" -t " +topic_value+ " -e " + host_endpoint
        #~ print "here:" + aws_cmd
        #~ aws_cmd="sudo ../eHealthDevice -m \"SPO2:96, BPM:60\" -t pulsioximeter -e a26ch0cchp0v7h-ats.iot.us-east-2.amazonaws.com "
        self.aws_proc = exec_cmd.createProcess(aws_cmd, None)
    
        self.AWS_thread_active_flag=1
        s_thread = threading.Thread(name='AWS-daemon', target=self.monitor_process_thread)
        s_thread.setDaemon(True)
        s_thread.start()
        wx.CallAfter(Publisher.sendMessage, "AWS_Cloud_Text", msg="\n\n" + aws_cmd +"\n\n")      

    def OnConfigureAWS1(self, evt):
        self.bottom_txt_display.WriteText("Setting AWS credentials... \n")
        wx.CallLater(10, self.OnConfigureAWS)

    def OnConfigureAWS(self):
        awskey = self.aws_key_input.GetValue()
        awssecretkey = self.aws_secret_input.GetValue()
        awssessiontoken = self.aws_session_input.GetValue()
        awsregion = self.aws_region_box.GetStringSelection()
        #~ if (awsregion != "us-east-1"):
            #~ if (misc.AwsRegionWarning(self, "Warning!").ShowModal() != wx.OK):
                #~ return
        exec_cmd.execCLI([
            "aws", "configure", "set",
            "aws_access_key_id", awskey,
        ])
        exec_cmd.execCLI([
            "aws", "configure", "set",
            "aws_secret_access_key", awssecretkey,
        ])
        exec_cmd.execCLI([
            "aws", "configure", "set",
            "aws_session_token", awssessiontoken,
        ])       
        exec_cmd.execCLI([
            "aws", "configure", "set",
            "default.region", awsregion,
        ])
        self.aws_key_input.Clear()
        self.aws_secret_input.Clear()
        self.aws_session_input.Clear()
        self.bottom_txt_display.WriteText("AWS credentials configured successfully\n")
        self.bottom_txt_display.WriteText("++++++++++++++++++++++++++++++++++++++++++++\n")

    def OnOpenConfig(self, evt):
        self.activetab = misc.EditorFrame(self, "Editing config.jsn", "config.jsn").ShowModal()

    def OnOpenPolicy(self, evt):
        self.activetab = misc.EditorFrame(self, "Editing policy.jsn", "policy.jsn").ShowModal()

    def OnCreatePolicy1(self, evt):
        self.bottom_txt_display.AppendText("Creating AWS IoT Policy... \n")
        wx.CallLater(10, self.OnCreatePolicy)
    
    def OnCreatePolicy(self):
        configfile = json.load(open("config.jsn"))
        policyname = configfile["AmazonIoT"]["PolicyName"]
        # Create IoT Policy
        self.bottom_txt_display.write("'aws iot create-policy --policy-name $policyname --policy-document file://policy.jsn'\n")
        command_output = exec_cmd.execCLI([
            "aws",
            "iot", "create-policy",
            "--policy-name", policyname,
            "--policy-document", "file://policy.jsn",
        ])
        command_output = exec_cmd.execCLI([
            "aws",
            "iot", "create-policy-version",
            "--set-as-default",
            "--policy-name", policyname,
            "--policy-document", "file://policy.jsn",
        ])
        self.bottom_txt_display.WriteText(str(command_output))
        self.bottom_txt_display.WriteText("++++++++++++++++++++++++++++++++++++++++++++\n")
        self.bottom_txt_display.Update()

    def OnClear(self, evt):
        self.bottom_txt_display.Clear()

    def OnInfo(self, evt):
        info.CloudDemoInfoDlg(self, "Cloud Use-Case Information").ShowModal()

    def OnCloseWindow(self, evt):
        self.AWS_thread_active_flag=0    
        self.Parent.Show()
        self.Destroy()
