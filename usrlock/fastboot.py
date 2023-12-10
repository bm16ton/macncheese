import time
import traceback
from adb.fastboot import FastbootCommands
from . import ui


def handle_exception(e: Exception, message: str):
    ui.error(message)
    traceback.print_exc()
    exit(1)

def poo(self):
    ui.error("Failed to unlock bootloader, already unlocked?", critical=False)
    time.sleep(3)
    self.fb_dev.Oem(b'hwdog certify set 0')
    ui.success("flock unlocked")
    time.sleep(2)
    ui.info("Rebooting device...")
    self.fb_dev.Reboot()
    self.fb_dev.Close()
    exit(1)       

class Fastboot:
    def connect(self):
        self.fb_dev = FastbootCommands()
        while True:
            devs = self.fb_dev.Devices()
            if len(list(devs)):
                time.sleep(1)
                break
        self.fb_dev.ConnectDevice()
        time.sleep(2)

    def write_nvme(self, prop: str, data: bytes):
        try:
            self.fb_dev._protocol.SendCommand(b'getvar', b'nve:' + prop + b'@' + data)
            time.sleep(2)
        except Exception as e:
            handle_exception(e, 'Failed to write NVME prop')

    def reboot(self):
        try:
            self.fb_dev.Reboot()
            self.fb_dev.Close()
        except Exception as e:
            handle_exception(e, 'Failed to reboot device')

    def reboot_bootloader(self):
        try:
            self.fb_dev.RebootBootloader()
            self.fb_dev.Close()
        except Exception as e:
            handle_exception(e, 'Failed to reboot device')

    def unlock(self, code: str):
        try:
            self.fb_dev.Oem('unlock %s' % code)
            time.sleep(1)
        except Exception:
            pass
            ui.error("Failed to unlock bootloader, already unlocked?", critical=False)
            try:
                self.fb_dev.Oem(b'hwdog certify set 0')
            except Exception:
                pass
                ui.error("flock unlocking error, is fastboot already unlocked?")
                ui.info("Rebooting device...")
                self.fb_dev.Reboot()
                self.fb_dev.Close()
                exit(1)  
            else:
                ui.success("flock unlocked")
        else:
            ui.success("bootloader unlocked")
    

    def fblock(self):
        try:
            self.fb_dev.Oem(b'hwdog certify set 0')
            time.sleep(2)
        except Exception:
            pass
            ui.error("Failed to unlock fastboot, is fastboot already unlocked?", critical=False)
            self.fb_dev.Reboot()
            self.fb_dev.Close()
        else:
            ui.success("flock unlocked")
