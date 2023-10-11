# How to call:
# Initialize the object:
# detector = ObjectDetection.ObjectDetection("./Database/best.pt", 0)

# To check for a food item, e.g., "onion":
# detector.check_items("onion")
# return:
# [False]

# To check for more than one food item, e.g., "onion" and "carrot":
# detector.check_items(["onion", "carrot"])
# return:
# [False,False]

# Once all detecting have finished:
# detector.end()


import DetectionAI
import GetCamare


class ObjectDetection:
    def __init__(self, model, camareID):
        self.AI = DetectionAI.DetectionAI(model)
        self.camare = GetCamare.GetCamare([1280, 720], camareID)

    # Will set everything up to check the frame for any objects that is passed in to it
    def check_items(self, items):
        _, frame = self.camare.cap.read()
        _, frame = self.camare.cap.read()
        self.camare.show(frame)
        return self.AI.process_frame(frame, items)

    # To be called at the end

    def end(self):
        self.camare.release()