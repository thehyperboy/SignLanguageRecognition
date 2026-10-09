import pyttsx3
import threading

def init_in_main():
    try:
        eng = pyttsx3.init()
        print("Main thread pyttsx3.init() SUCCESS:", eng)
        eng.say("Main thread test")
        eng.runAndWait()
        eng.stop()
    except Exception as e:
        print("Main thread pyttsx3.init() FAILED:", e)

def init_in_thread():
    try:
        import pythoncom
        pythoncom.CoInitialize()
    except Exception as e:
        print("pythoncom CoInitialize error:", e)
    try:
        eng = pyttsx3.init()
        print("Worker thread pyttsx3.init() SUCCESS:", eng)
        eng.say("Worker thread test")
        eng.runAndWait()
        eng.stop()
    except Exception as e:
        print("Worker thread pyttsx3.init() FAILED:", e)

print("--- MAIN THREAD TEST ---")
init_in_main()

print("\n--- THREAD TEST WITHOUT COINITIALIZE ---")
def thread_func_no_com():
    try:
        eng = pyttsx3.init()
        print("No com thread pyttsx3.init() SUCCESS:", eng)
    except Exception as e:
        print("No com thread pyttsx3.init() FAILED:", e)

t = threading.Thread(target=thread_func_no_com)
t.start()
t.join()

print("\n--- THREAD TEST WITH COINITIALIZE ---")
t2 = threading.Thread(target=init_in_thread)
t2.start()
t2.join()
