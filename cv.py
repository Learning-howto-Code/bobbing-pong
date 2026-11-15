import cv2 as cv

faceCascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600
rectangleColor = (0, 0, 255)

capture = cv.VideoCapture(0)
if not capture.isOpened():
    raise SystemExit("Could not open camera")
t=0
while True:

    rc, fullSizeBaseImage = capture.read()
    if not rc:
        continue  # skip bad frames (the first few can be empty while the camera warms up)

    baseImage = cv.resize(fullSizeBaseImage, (640, 480))   # was 320x240
    resultImage = baseImage.copy()

    gray = cv.cvtColor(baseImage, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)                           # helps with dim or uneven light

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,     # finer size steps
        minNeighbors=4,      # a bit less strict
        minSize=(20, 20),    # allow small, distant faces
    )

    # find the biggest face
    maxArea = 0
    x = y = w = h = 0
    for (_x, _y, _w, _h) in faces:
        if _w * _h > maxArea:
            x, y, w, h = _x, _y, _w, _h
            maxArea = _w * _h

    # draw once, after the loop
    if maxArea > 0:
        cv.rectangle(resultImage, (x - 10, y - 20), (x + w + 10, y + h + 20), rectangleColor, 2)

    largeResult = cv.resize(resultImage, (OUTPUT_SIZE_WIDTH, OUTPUT_SIZE_HEIGHT))


    if cv.waitKey(1) & 0xFF == ord("q"):  # also redraws the windows
        break
    if maxArea > 0:
        center_y = y + h / 2
        y_norm = center_y / baseImage.shape[0]       # 0 = top, 1 = bottom
        y_norm = max(0.0, min(1.0, y_norm))
        print(round(y_norm, 3))
capture.release()