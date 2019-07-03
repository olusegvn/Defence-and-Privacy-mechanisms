# Defence mechanisms

import ctypes
import datetime
import os
import psutil
import subprocess
import time
import win32api as wapi
import win32gui
# import re
from AI_FacialRecognition import FacialClassifier
from pynput.keyboard import Key, Controller
keyboard = Controller()

# Global Variables
all_keys = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm 1234567890 ,. @#$%^&*()?><\':_+;-=\'APS$/\\"
user32 = ctypes.windll.User32
WGUI = win32gui


def key_pressed(keys):
    if all(wapi.GetAsyncKeyState(ord(key)) for key in keys):
        return True
    return False


class Log:
    def __init__(self):
        self.log_filename = "systemlogs.my"
        self.log_location = "C:\\Users\\Public\\Libraries"

    def write(self, data):
        with open(self.log_location + "\\" + self.log_filename, 'a') as w:
            w.writelines(data + '\n')
        return data

    def log(self):
        string = WGUI.GetWindowText(WGUI.GetForegroundWindow()) + " accessed at " + str(datetime.datetime.now())
        self.write(string)
        return string

    def log_intrusion(self):
        string = "\nintruder detected at " + str(datetime.datetime.now())
        self.write(string)
        return string

    def log_deactivation(self, app):
        string = app + " trap deactivated at " + str(datetime.datetime.now())+'\n'
        self.write(string)
        return string

    def kLog(self, string):
        for key in all_keys:
            if wapi.GetAsyncKeyState(ord(key)):
                self.write(string + " key logged : " + key)

    def raise_error(self, command, err_str):
        print('unable to alter source code : ' + err_str + '\n')
        Command = ' '.join(command)
        self.write('\ncommand ' + Command + 'failed to execute :  at ' + str(datetime.datetime.now()))
        return '\ncommand ' + Command + 'failed to execute :  at ' + str(datetime.datetime.now())


class SystemMechanisms(Log):
    def __init__(self, code_str):  # Hibernate_String|
        super().__init__()
        self.code_str = code_str
        self.current_window_text = "Window"
        self.window = 50
        self.trap_state = "active"
        self.window_dict = {
            'Explorer': [['documents', 'music', 'this pc', 'libraries', 'file explorer', 'startup'], 'exp'],
            'Videos': [['videos', 'movies & tv'], 'exp'], 'Instagram': [['instagram'], 'exp'],
            'Command Shell': [['command prompt', 'cmd', 'System32'], 'cmd', 'in'],
            'Browser': [['opera', 'uc-browser'], 'exp', 'in']}
        self.allowed_start_files = ['Windows.bat', 'Windows.exe', 'Windows.lnk']
        self.allowed_processes = ['audiodg.exe', 'vx360ce_x64.exe', 'x360ce_x64.exe', 'NSUNS4.exe', 'vNSUNS4.exe', 'vfifaconfig.exe', 'vFIFA19.exe', 'fifaconfig.exe', 'FIFA19.exe', 'WindowsInternal.ComposableShell.Experiences.TextInput.InputApp.exe', 'System Idle Process', 'IDMIntegrator64.exe', 'System', 'svchost.exe', 'svchost.exe', 'fontdrvhost.exe', 'fontdrvhost.exe', 'smss.exe', 'svchost.exe', 'csrss.exe', 'wininit.exe', 'csrss.exe', 'DSAPI.exe', 'WavesSvc64.exe', 'services.exe', 'winlogon.exe', 'lsass.exe', 'svchost.exe', 'svchost.exe', 'fsnotifier64.exe', 'dwm.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'Memory Compression', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'opera.exe', 'quickset.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'igfxCUIService.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'opera.exe', 'svchost.exe', 'RtkAudioService64.exe', 'ShellExperienceHost.exe', 'svchost.exe', 'svchost.exe', 'conhost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'plugin_host.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'RAVBg64.exe', 'RAVBg64.exe', 'svchost.exe', 'pcdrwi.exe', 'spoolsv.exe', 'NisSrv.exe', 'svchost.exe', 'IntelCpHDCPSvc.exe', 'WavesSysSvc64.exe', 'svchost.exe', 'ibtsiva.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'taskhostw.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'DiskInternals.Preview.dll', 'SecurityHealthService.exe', 'svchost.exe', 'IntelCpHeciSvc.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'svchost.exe', 'opera.exe', 'sedsvc.exe', 'opera.exe', 'DDVCollectorSvcApi.exe', 'IAStorDataMgrSvc.exe', 'svchost.exe', 'conhost.exe', 'svchost.exe', 'DDVDataCollector.exe', 'SupportAssistAgent.exe', 'DDVRulesProcessor.exe', 'svchost.exe', 'sihost.exe', 'svchost.exe', 'RAVBg64.exe', 'opera_crashreporter.exe', 'WmiPrvSE.exe', 'MsMpEng.exe', 'SearchFilterHost.exe', 'jhi_service.exe', 'SearchIndexer.exe', 'cmd.exe', 'opera.exe', 'WmiPrvSE.exe', 'LMS.exe', 'opera.exe', 'ctfmon.exe', 'explorer.exe', 'SearchProtocolHost.exe', 'igfxEM.exe', 'SearchUI.exe', 'RuntimeBroker.exe', 'wermgr.exe', 'MSASCuiL.exe', 'pycharm64.exe', 'LockApp.exe', 'RuntimeBroker.exe', 'RtkNGUI64.exe', 'LinuxReader64.exe', 'BitTorrent.exe', 'RAVBg64.exe', 'unsecapp.exe', 'dllhost.exe', 'SkypeBackgroundHost.exe', 'RuntimeBroker.exe', 'opera.exe', 'opera.exe', 'dllhost.exe', 'opera.exe', 'opera.exe', 'svchost.exe', 'svchost.exe', 'conhost.exe', 'OfficeClickToRun.exe', 'opera.exe', 'opera.exe', 'SystemSettingsBroker.exe', 'opera.exe', 'RuntimeBroker.exe', 'svchost.exe', 'opera.exe', 'bittorrentie.exe', 'DiskInternals.Preview.dll', 'svchost.exe', 'bittorrentie.exe', 'svchost.exe', 'python.exe', 'sublime_text.exe', 'Music.UI.exe', 'uc-browser', 'MortalKombat.exe', 'wuauclt.exe', 'TiWorker.exe', '', 'WUDFHost.exe', 'SystemIdleCheck.exe', 'IpOverUsbSvc.exe', 'MusNotification.exe', 'Video.UI.exe', 'ApplicationFrameHost.exe', 'LogonUI.exe', 'ngen.exe', 'ngentask.exe', 'mscorsvw.exe', 'Taskmgr.exe', 'WmiApSrv.exe', 'OfficeC2RClient.exe', 'UsoClient.exe', 'sppsvc.exe', 'POWERPNT.EXE', 'WinUAPEntry.exe', 'PickerHost.exe', 'vlc.exe', 'test1.exe', 'test3.exe', 'Scheduler.exe', 'goat', 'SystemSettings.exe', 'powershell.exe', 'TrustedInstaller.exe', 'DismHost.exe']

    def hibernate_mechanism(self):
        hyb_key_list = list(self.code_str['hyb'])
        lck_key_list = list(self.code_str['lck'])
        if key_pressed(hyb_key_list):
            String = "hibernation Combination Detected at " + str(datetime.datetime.now())
            self.write(String)
            print(String)
            subprocess.call("shutdown -h", shell=True)

        if key_pressed(lck_key_list):
            user32.LockWorkStation()

    def detected_window(self):
        # for Process in psutil.process_iter():
        #    if 'cmd' in Process.name():
        #       print("Command shell open")
        # window = user32.GetForegroundWindow()
        self.current_window_text = WGUI.GetWindowText(WGUI.GetForegroundWindow())
        for Category in self.window_dict:
            if any(self.window in str(self.current_window_text).lower() for self.window in
                   self.window_dict[Category][0]):
                # print(self.window_dict[self.window])
                # print(user32.GetForegroundWindow())
                return self.current_window_text, Category
        return '', ''

    def face_unlock(self):
        FC = FacialClassifier()
        FC.pick('eigenFrames.pickle')
        if FC.recognize() == 'm':
            return True
        else:
            self.write("intruder Frame : " + FC.return_face())
        return False

    def Trap(self):
        detected_window, category = self.detected_window()
        for Category in self.window_dict:
            for app in self.window_dict[Category][0]:
                if (app == str(detected_window).lower()) or \
                        (app in str(detected_window).lower() and self.window_dict[Category][2] == 'in'):
                    self.log()
                    key_list = self.code_str[self.window_dict[Category][1]]
                    trap_start_time = time.time()
                    print(Category)

                    while True:
                        if round(time.time() - trap_start_time, 1) == 2.2:
                            print(self.log_intrusion())
                            user32.LockWorkStation()
                            break
                        if key_pressed(key_list) or self.face_unlock():
                            print(self.log_deactivation(Category + ": " + detected_window))
                            self.trap_state = "deactivated"
                            while Category in self.detected_window():
                                pass
                                # print("Permitting ...")
                            break


    def virus_disrupt(self):
        start_path = 'C:\\Users\\DELL\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
        for file in os.listdir(start_path):
            if file not in self.allowed_start_files:
                os.remove(start_path + '\\' + file)
        for program in psutil.process_iter():
            if program.name() not in self.allowed_processes:
                try:
                    print("Terminating unallowed program : " + program.name())
                    subprocess.call("wmic process where name='" + program.name() + "' delete")
                    self.write("Terminating unallowed program : " + program.name())
                except psutil.NoSuchProcess:
                    print("Process no longer exists ")
                except:
                    pass


super_dict = {'exp': 'M', 'inp': 'INP', 'cmd': 'N', 'lck': 'POK', 'hyb': 'QWER'}


class EnhanceSourceCode(SystemMechanisms):
    def __init__(self):
        super().__init__(super_dict)
        self.source_code = open(__file__, 'r').read()
        #         JUST in case
        #         self.write('\n' * 5 + self.source_code + '\n' * 5)
        self.enhance_list = {'start_files': self.allowed_start_files, 'allowed_processes': self.allowed_processes}
        self.enhance_dict = {'super_dict': super_dict}
        self.command = ''

    def enhance_List(self, item, command, *args):
        r = str(self.enhance_list[item][:])
        for arg in args:
            for items in arg:
                if command == 'add':
                    self.enhance_list[item].append(items)
                elif command == 'remove':
                    self.enhance_list[item].remove(items)
                else:
                    self.raise_error(self.command, "unknown command")
                    break
        repl = str(self.enhance_list[item][:])
        out_string = self.source_code.replace(r, repl, 2)
        with open(__file__, 'w') as f:
            f.write(out_string)

    def enhance_Dict(self, Dict, item, rpl):  # super_dict exp
        r = str("'" + item + "': '" + self.enhance_dict[Dict][item] + "'")
        print(r)
        self.enhance_dict[Dict][item] = rpl
        repl = str("'" + item + "': '" + rpl + "'")
        out_string = self.source_code.replace(r, repl, 2)
        # out_string, count  = re.subn(r, repl, self.source_code)
        print("\n\n\n\n" + out_string)
        with open(__file__, 'w') as f:
            f.write(out_string)


class XRAMechanisms(EnhanceSourceCode):
    def __init__(self):
        super().__init__()
        self.XRM_state = 'activated'
        self.command = ''

    def mp_detector(self):
        # detected_window, Category = self.detected_window()
        # while WGUI.GetForegroundWindow() == 0:
        #     self.kLog("pw-key")
        if WGUI.GetForegroundWindow() == 0:
            if self.face_unlock():
                keyboard.press('a')

    def enhance_source_code(self):
        self.command = param = input("\n Alter source item >> ").split(' ')
        try:
            if param[0] in self.enhance_list:
                self.enhance_List(param[0], param[1], param[2:])
            elif param[0] in self.enhance_dict:
                self.enhance_Dict(param[0], param[1], param[2])
            else:
                self.raise_error(self.command, "unknown item")
        except KeyError:
            self.raise_error(param, "key Error\n")
            self.enhance_source_code()
        except IndexError:
            self.raise_error(param, "invalid syntax\n")
            self.enhance_source_code()


def main():
    # pinL = Log()pin
    SM = SystemMechanisms(super_dict)
    XRM = XRAMechanisms()
    while True:
        SM.virus_disrupt()
        SM.Trap()
        SM.hibernate_mechanism()
        # XRM.mp_detector()
        if key_pressed(list(super_dict['inp'])):
            XRM.enhance_source_code()

    main()


if __name__ == '__main__':
    main()

# @C0Scripts : DM
