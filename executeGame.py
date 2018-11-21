import threading
import main
import threadPlayAudio

# I learned about how threading works using an online tutorial 
# https://www.youtube.com/watch?v=PJ4t2U15ACo

displayThread = threading.Thread(target = main.main)
#audioThread = threading.Thread()

displayThread.start()
#audioThread.start()

displayThread.join()
#audioThread.join()
