# Import OpenCV, Time, and Datetime library
import cv2, time, datetime

def main():
    # Grab the current frame and initialize the text
    first_frame = None
    text = "No Objects"
    # Create the video capture
    video = cv2.VideoCapture(0)
    time.sleep(2.0)
    #Create a infinite loop to show the capture video
    while True:
        #Read the video capture
        check, frame = video.read()
        
        # Convert the capture to gray scale and Blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(21,21),0)    

        # If the first frame is None, initialize it    
        if first_frame is None:
            first_frame = gray
            continue

        # Compute the absolute difference between the current frame and first frame        
        delta_frame = cv2.absdiff(first_frame,gray)
        thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        
        # Dilate the thresholded image to fill in holes, then find contour on thresholded image 
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
        (conts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop over the contours
        for countour in conts:
            # If the contour is too small, less than 10000 pxl, ignore it
            if cv2.contourArea(countour) < 10000:
                continue
            # Compute the bounding box for the contour, draw it on the frame, and update the text        
            (x, y, w, h) = cv2.boundingRect(countour)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3)
            text = "Detecting objects"

        # Draw the text and timestamp on the frame
        cv2.putText(frame, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # Display the frames in a window infinitely until press the "Q" key and break the infinite loop
        cv2.imshow("Gray Frame",gray)
        cv2.imshow("Delta Frame",delta_frame)
        cv2.imshow("Threshold Frame",thresh_frame)
        cv2.imshow("Color frame", frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    # Close the video capture window
    video.release()
    # Close the windows when a user press any key
    cv2.destroyAllWindows

if __name__ == '__main__':
    main()