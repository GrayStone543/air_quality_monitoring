import cv2


def liveview():
    test_frame = cv2.imread('./20-36-38.png')

    liveview_w = 800
    liveview_h = 600
    x = 50
    y = 50
    width = 110
    height = 54
    border_color = (0, 255, 0)

    while True:
    #     # read frame from camera lib
        frame = test_frame.copy()
        
        disp = frame.copy()
        # 畫上綠色方框
        cv2.rectangle(disp, (x, y), (x + width, y + height), border_color, 2)
        # 標上方框左上角的座標
        cv2.putText(disp, f"{x},{y}", (x + 4, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 232, 0), 1, cv2.LINE_AA)

        cv2.imshow("Live view", disp)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break
        elif key == ord('w'):
            if y > 1:
               y -= 1
        elif key == ord('s'):
            if y < liveview_h - height - 1:
                y += 1
        elif key == ord('a'):
            if x > 1:
                x -= 1
        elif key == ord('d'):
            if x < liveview_w - width - 1:
                x += 1
        elif key == ord('e'):
            roi = frame[y:y+height, x:x+width]
            cv2.imshow('ROI', roi)
        elif key != 0xff:
            print(f'key = {key}')
        
    cv2.destroyAllWindows()


if __name__ == "__main__":
    liveview()