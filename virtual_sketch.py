"""
Virtual Sketch using OpenCV

Draw on a virtual canvas by moving a colored object
(e.g., a blue marker cap) in front of your webcam.
"""

import cv2
import numpy as np


class VirtualSketch:
    def __init__(self, camera_index: int = 0):
        self.cap = cv2.VideoCapture(camera_index)
        self.canvas = None
        self.previous_point = None

        # HSV range for blue color (you can adjust)
        self.lower_hsv = np.array([100, 120, 70], dtype=np.uint8)
        self.upper_hsv = np.array([140, 255, 255], dtype=np.uint8)

    def _prepare_canvas(self, frame):
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

    def _get_marker_center(self, mask):
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(largest)
        if radius < 8:  # ignore tiny noise
            return None

        return int(x), int(y)

    def _create_mask(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        raw_mask = cv2.inRange(self.lower_hsv, self.upper_hsv)

        # Reduce noise: open then dilate
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(raw_mask, cv2.MORPH_OPEN, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=1)
        return mask

    def run(self):
        if not self.cap.isOpened():
            print("Could not open webcam.")
            return

        print("Virtual Sketch started.")
        print("Press 'c' to clear canvas, 'q' to quit.")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read from camera. Exiting.")
                break

            frame = cv2.flip(frame, 1)  # mirror view
            self._prepare_canvas(frame)

            mask = self._create_mask(frame)
            center = self._get_marker_center(mask)

            if center is not None:
                cv2.circle(frame, center, 6, (0, 255, 0), -1)

                if self.previous_point is not None:
                    cv2.line(
                        self.canvas,
                        self.previous_point,
                        center,
                        (0, 0, 255),
                        thickness=5,
                        lineType=cv2.LINE_AA,
                    )

                self.previous_point = center
            else:
                self.previous_point = None

            combined = cv2.addWeighted(frame, 0.6, self.canvas, 0.8, 0)

            cv2.imshow("Virtual Sketch - View", combined)
            cv2.imshow("Mask (Debug)", mask)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("c"):
                self.canvas[:] = 0

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    sketch = VirtualSketch()
    sketch.run()
