import multiprocessing
from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return "Virtual Assistant is Running"


def startFlask():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

def startJarvis():
    print("Process 1 is running.")
    from main import start
    start()


def listenHotword():
    print("Process 2 is running.")
    from engine.features import hotword
    hotword()


if __name__ == '__main__':

    p1 = multiprocessing.Process(target=startFlask)
    p1.start()

    p2 = multiprocessing.Process(target=startJarvis)
    p3 = multiprocessing.Process(target=listenHotword)
    
    p2.start()
    p3.start()

    p2.join()
    p3.join()


    if p1.is_alive():
        p1.terminate()
        p1.join()

    print("System stopped.")
