import cv2
import numpy as np
import json
import time


NO_ACTIVE = "NO ACTIVE"
HCHO = "HCHO"
CO = "CO"
CO2 = "CO2"
DEFAULT_W = 120
DEFAULT_H = 54
DEFAULT_ROI = {
    HCHO: {"x": 50, "y": 50,  "w": DEFAULT_W, "h": DEFAULT_H, "color": (200, 60, 150), "title": HCHO},
    CO:   {"x": 50, "y": 250, "w": DEFAULT_W, "h": DEFAULT_H, "color":  (50, 60, 200), "title": CO},
    CO2:  {"x": 50, "y": 375, "w": DEFAULT_W, "h": DEFAULT_H, "color": (200, 100, 50), "title": CO2},
    NO_ACTIVE: {"x": 0, "y":0, "w": DEFAULT_W, "h": DEFAULT_H, "color": (128, 128, 128), "title": NO_ACTIVE}
}
DEFAULT_WARNING_THRES = {HCHO: 0.098, CO: 35, CO2: 1000}


def build_test_frame(width, height):
    frame = np.zeros([height, width, 3], dtype=np.uint8)
    b, g, r = 0, 0, 0
    for _iw in range(0, width):
        b = int((_iw / width) * 200)
        for _ih in range(0, height):
            r = int((_ih / height) * 200)
            g = 160 - int((_iw / width) * (_ih / height) * 160)
            frame[_ih][_iw] = [b, g, r]
    return frame


def save_config(config):
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def load_config():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        config = {
            "version": 1.0,
            "warning threshold": DEFAULT_WARNING_THRES,
            "roi": DEFAULT_ROI }

    try:
        roi = config["roi"]
    except KeyError:
        config["roi"] = DEFAULT_ROI

    try:
        warning_thres = config["warning threshold"]
    except KeyError:
        config["warning threshold"] = DEFAULT_WARNING_THRES

    return config


def draw_ROI(img, roi:dict, active=False):
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    if active:
        border_color = (0, 250, 0)
    else:
        border_color = roi["color"]
    cv2.rectangle(img, (roi["x"], roi["y"]), (roi["x"] + roi["w"], roi["y"] + roi["h"]), border_color, 2)
    (text_w, text_h), baseline = cv2.getTextSize(roi["title"], fontFace, fontScale, 1)
    x = roi["x"] - text_w - 2
    y = roi["y"] + text_h
    cv2.putText(img, roi["title"], (x, y), fontFace, fontScale, border_color, 1, cv2.LINE_AA)


def draw_elapsed(img, elapsed):
    PADDING = 8
    fontFace = cv2.FONT_HERSHEY_PLAIN
    fontScale = 1.6
    _sec = int(elapsed % 60)
    _min = int((elapsed / 60) % 60)
    _hour = int(elapsed / 3600)
    _time_str = f"{_hour}:{_min:02}:{_sec:02}"
    (text_w, text_h), baseline = cv2.getTextSize(_time_str, fontFace, fontScale, 1)
    _h, _w, _ = img.shape
    x = _w - text_w - PADDING
    y = text_h + PADDING
    x2 = x + text_w
    y1 = y - text_h - 2
    cv2.rectangle(img, (x, y1), (x2, y), (32, 32, 32), -1)
    cv2.putText(img, _time_str, (x, y), fontFace, fontScale, (0, 200, 0), 1, cv2.LINE_AA)


def liveview():
    hcho = 0.0
    co = 0
    co2 = 592

    liveview_w = 800
    liveview_h = 600

    start_time = time.time()
    event1_start_time = time.time()
    test_frame = build_test_frame(liveview_w, liveview_h)

    step = 1
    activeROI = NO_ACTIVE
    config = load_config()
    roi = config["roi"]
    warning_thres = config["warning threshold"]

    while True:
        elapsed = time.time() - start_time

        # read frame from camera lib
        frame = test_frame.copy()
        
        disp = frame.copy()
        
        # Iterative action
        if (time.time() - event1_start_time) >= 10.0:
            # do OCR every 10 seconds
            try:
                # Convert OCR result to float value
                concentration = {
                    HCHO: float(hcho),
                    CO: float(co),
                    CO2: float(co2)
                }

                # send a log to the Google Sheet
                
                # check warning threshold here
                for key in concentration:
                    if concentration[key] > warning_thres[key]:
                        notify_msg = f"WARNING!\n{key} ({concentration[key]}) exceed the limit.\n"
                        #send telegram message
            except ValueError as e:
                print("Error: OCR failed")
            # get the start time for next event
            event1_start_time = time.time()

        # Draw the ROIs 
        draw_ROI(disp, roi[HCHO], activeROI == HCHO)
        draw_ROI(disp, roi[CO], activeROI == CO)
        draw_ROI(disp, roi[CO2], activeROI == CO2)

        draw_elapsed(disp, elapsed)
       
        cv2.imshow("Live view", disp)

        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break
        elif key == ord('w'):            
            if roi[activeROI]["y"] > 1:
               roi[activeROI]["y"] -= step
        elif key == ord('s'):
            if roi[activeROI]["y"] < liveview_h - roi[activeROI]["h"] - 1:
                roi[activeROI]["y"] += step
        elif key == ord('a'):
            if roi[activeROI]["x"] > 1:
                roi[activeROI]["x"] -= step
        elif key == ord('d'):
            if roi[activeROI]["x"] < liveview_w - roi[activeROI]["w"] - 1:
                roi[activeROI]["x"] += step
        elif key == ord('e'):
            if (activeROI != NO_ACTIVE):
                x, y = roi[activeROI]["x"], roi[activeROI]["y"]
                w, h = roi[activeROI]["w"], roi[activeROI]["h"]
                roi_img = frame[y:y+h, x:x+w]
                cv2.imshow('ROI', roi_img)
        elif key == ord('t'):
            if step == 1:
                step = 4
            elif step == 4:
                step = 10
            else:
                step = 1
        elif key == ord('0'):
            activeROI = NO_ACTIVE
        elif key == ord('1'):
            activeROI = HCHO
        elif key == ord('2'):
            activeROI = CO
        elif key == ord('3'):
            activeROI = CO2
        elif key == ord('o'):
            config["roi"] = roi
            config["warning threshold"] = warning_thres
            save_config(config)
        elif key != 0xff:
            print(f'key = {key}')
        
    cv2.destroyAllWindows()


if __name__ == "__main__":
    liveview()