# ------------------------------
# Import Libraries
# ------------------------------
from ultralytics import YOLO
import math


# --- DEFINE THE MODEL ---
object_model = YOLO("yolov8m.pt")
currency_model = YOLO("currency.pt")

# --- FUNCTION TO DETECT ---
def detection(frame, mode):
    if frame is None: 
        return 0
    
    model = object_model
    if(mode == "currency"):
        model = currency_model

    results = model.predict(frame)
    object_counts = get_objects_count(model, results)

    return object_counts


# --- OBJECTS COUNT ---
def get_objects_count(model, results):
    unique_objects = [] # list of unique objects
    object_counts = {} # list of object and its count

    for result in results:
        if result.boxes:
            for box in result.boxes:
                conf = math.ceil((box.conf[0]*100))
                if conf > 30:
                    ClassInd = int(box.cls)
                    if model.names[ClassInd] not in object_counts:
                        unique_objects.append(model.names[ClassInd])
                        object_counts[model.names[ClassInd]] = 1
                    else:
                        object_counts[model.names[ClassInd]] += 1
                else:
                    return False
        else:
            return False

    return object_counts

# --- Create Text From Object Names ---
def objectNames(object_names_count):
    final_text = ""
    for index, (key, value) in enumerate(object_names_count.items()):
        is_sum = "s" if value > 1 else ""
        is_and = "" if index == len(object_names_count)-1 else "and "
        final_text += f"{value} {key}{is_sum} {is_and}"
    
    return final_text
    


# --- IMAGE DETECTION ---
def image_detection(frame, mode):
    object_counts = detection(frame, mode)
    if(object_counts == False):
        return "No Objects To Detect"
    else:
        return objectNames(object_counts)



def test_detection():
    object_model.predict("static/logo.png")
    currency_model.predict("static/logo.png")