import cv2
import numpy as np


NO_ACTIVE = "NO ACTIVE"
HCHO = "HCHO"
CO = "CO"
CO2 = "CO2"

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


def draw_ROI(img, roi:dict, active=False):
    if active:
        border_color = (0, 250, 0)
    else:
        border_color = roi["color"]
    cv2.rectangle(img, (roi["x"], roi["y"]), (roi["x"] + roi["w"], roi["y"] + roi["h"]), border_color, 2)
    textSize, baseline = cv2.getTextSize(roi["title"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.putText(img, roi["title"], (roi["x"] - textSize[0] - 2, roi["y"] + textSize[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, border_color, 1, cv2.LINE_AA)


def liveview():
    liveview_w = 800
    liveview_h = 600

    test_frame = build_test_frame(liveview_w, liveview_h)

    step = 1
    width = 120
    height = 54
    activeROI = NO_ACTIVE
    roi = {
        HCHO: {"x": 50, "y": 50, "w": width, "h": height, "color": (200, 60, 150), "title": HCHO},
        CO: {"x": 50, "y": 250, "w": width, "h": height, "color": (50, 60, 200), "title": CO},
        CO2: {"x": 50, "y": 375, "w": width, "h": height, "color": (200, 100, 50), "title": CO2},
        NO_ACTIVE: {"x": 0, "y":0, "w": width, "h": height}
    }

    while True:
        # read frame from camera lib
        frame = test_frame.copy()
        
        disp = frame.copy()
        
        # Draw the ROI of HCHO
        draw_ROI(disp, roi[HCHO], activeROI == HCHO)
        draw_ROI(disp, roi[CO], activeROI == CO)
        draw_ROI(disp, roi[CO2], activeROI == CO2)
        
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
        elif key != 0xff:
            print(f'key = {key}')
        
    cv2.destroyAllWindows()


if __name__ == "__main__":
    liveview()