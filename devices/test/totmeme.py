import computer_control
import time
import urequests
import machine

def rout():
    try:
        r = urequests.get('https://totmeme-161806.appspot.com/get_routines?controller=test')
        text = r.text
        r.close()
        try:
            r = text.split('\n')
            text = None
            for i in range(1, int(r[0]) + 1):
                r[i] = r[i].split('; ')
                task = r[i][0]
                pin = int(r[i][1])
                action = r[i][2]
                note = 'may be error'
                try:
                    if action == 'start':
                        computer_control.power_on(pin)
                        note = 'started ' + str(pin)
                        print(note)
                    elif action == 'stop':
                        computer_control.force_stop(pin)
                        note = 'forced stop of ' + str(pin)
                        print(note)
                except Exception as e:
                    note = 'Exeption: ' + str(e)
                    print(note)
                    machine.reset()
                try:
                    op = urequests.get('https://totmeme-161806.appspot.com/callback?action=done&id='+task+'&note='+note.replace(' ', '%20'))
                    print(op.text)
                    op.close()
                except Exception:
                    print('Error set status')
                    machine.reset()
        except Exception:
            print('not good answ')
            machine.reset()
    except Exception:
        print('Error get')
        machine.reset()

def main(timer=120):
    while True:
        time.sleep(timer)
        try:
            rout()
        except Exception:
            machine.reset()