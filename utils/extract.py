from library import *


def extract_images(pathIn,pathOut):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    list_ts = [second for second in range(int(frames/fps))]
    choic_ts = random.choice(list_ts)

    success,image = vidcap.read()
    success = True
    while success:

        success,image = vidcap.read()
        ts = float(vidcap.get(cv2.CAP_PROP_POS_MSEC))

        if int(ts/1000)==choic_ts:

            cv2.imwrite(pathOut,image[:, :] )
        count = count + 1
