import mediapipe as mp

class PointsDetect():

    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=2,
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def recognized(self,frame):
        return self.pose.process(frame)

