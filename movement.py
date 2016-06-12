import cv2
import time

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture(0)
#out = cv2.VideoWriter(time.asctime( time.localtime(time.time())  )+".avi",fourcc, 20.0, (640,480))
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
out = cv2.VideoWriter("output.avi",fourcc, 20.0, (640,480))

winName = "Movement Indicator"
#cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

newImg = diffImg(t_minus, t, t_plus)
tag_min = cv2.mean(newImg)

print(tag_min[0])

while True:
    newImg = diffImg(t_minus, t, t_plus)

    tag = cv2.mean(newImg)

    #if tag[0] < tag_min:
    #    tag_min = tag[0]
    #    print tag_min

    #print (tag[0])

    if( tag[0] > tag_min[0]+0.2 ):
    #if(tag[0] > 2.0):
        ret, frame = cam.read()

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,time.asctime( time.localtime(time.time()) ),(50,50), font, 1,(255,255,255),1,cv2.LINE_AA)
        #cv2.imshow("real", frame)


        out.write(frame)

    else:
        cv2.destroyWindow("real")

    cv2.imshow( winName, newImg)
    #cv2.imshow("real", t)

    time.sleep(0.1)

    # Read next image
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    #key = cv2.waitKey(10)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       cv2.destroyWindow(winName)
       cv2.destroyWindow("real")
       break

print ("Goodbye")



