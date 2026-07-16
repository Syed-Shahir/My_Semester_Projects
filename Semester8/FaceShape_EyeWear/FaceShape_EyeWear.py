import sys
import os
import cv2
import mediapipe as mp
import numpy as np
import math
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
    QPushButton, QComboBox, QTextEdit, QHBoxLayout, QMessageBox,
    QDialog, QLineEdit, QFormLayout, QFileDialog
)
from PyQt5.QtGui import QImage, QPixmap, QDoubleValidator
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# === Setup Logging ===
logging.basicConfig(
    filename='eyewear_recommender.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suppress TensorFlow/MediaPipe warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# === Configuration ===
FIXED_MM_PER_PIXEL = 0.4
AVG_IPD_MM = 65.0

# === Resource Path Handling for PyInstaller ===
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# === MediaPipe Utility Modules ===
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

# === Utility Functions ===
def calculate_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def get_landmark_coords(landmarks, indices, w, h):
    return [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices]

def compute_measurements(frame, face_landmarks, mm_per_pixel):
    try:
        h, w, _ = frame.shape
        lm = face_landmarks.landmark

        def lp(i): return (lm[i].x * w, lm[i].y * h)

        left_pupil = lp(468)
        right_pupil = lp(473)
        left_temple = lp(127)
        right_temple = lp(356)
        bridge_left = lp(168)
        bridge_right = lp(6)
        forehead_top = lp(10)
        chin_bottom = lp(152)
        left_eye_outer = lp(33)
        left_eye_inner = lp(133)
        right_eye_outer = lp(263)
        right_eye_inner = lp(362)
        left_eye_top = lp(159)
        left_eye_bottom = lp(145)
        right_eye_top = lp(386)
        right_eye_bottom = lp(374)
        left_ear = lp(234)
        right_ear = lp(454)
        jaw_left_angle = lp(58)
        jaw_right_angle = lp(288)
        cheekbone_left = lp(93)
        cheekbone_right = lp(323)
        forehead_left = lp(68)
        forehead_right = lp(298)

        pd_px = calculate_distance(left_pupil, right_pupil)
        face_width_px = calculate_distance(left_temple, right_temple)
        jaw_width_px = calculate_distance(jaw_left_angle, jaw_right_angle)
        cheekbone_width_px = calculate_distance(cheekbone_left, cheekbone_right)
        forehead_width_px = calculate_distance(forehead_left, forehead_right)
        face_length_px = calculate_distance(forehead_top, chin_bottom)
        bridge_width_px = calculate_distance(bridge_left, bridge_right)
        
        left_lens_width_px = calculate_distance(left_eye_outer, left_eye_inner)
        right_lens_width_px = calculate_distance(right_eye_outer, right_eye_inner)
        lens_width_px = (left_lens_width_px + right_lens_width_px) / 2

        left_lens_height_px = calculate_distance(left_eye_top, left_eye_bottom)
        right_lens_height_px = calculate_distance(right_eye_top, right_eye_bottom)
        lens_height_px = (left_lens_height_px + right_lens_height_px) / 2

        temple_length_px = (calculate_distance(left_temple, left_ear) +
                            calculate_distance(right_temple, right_ear)) / 2

        left_eye_center = ((lm[468].x + lm[470].x)/2 * w, (lm[468].y + lm[470].y)/2 * h)
        right_eye_center = ((lm[473].x + lm[475].x)/2 * w, (lm[473].y + lm[475].y)/2 * h)
        avg_eye_center_px = (int((left_eye_center[0] + right_eye_center[0]) / 2),
                             int((left_eye_center[1] + right_eye_center[1]) / 2))

        return {
            'face_width_px': face_width_px,
            'pd_px': pd_px,
            'avg_eye_center_px': avg_eye_center_px,
            'face_width_mm': face_width_px * mm_per_pixel,
            'face_length_mm': face_length_px * mm_per_pixel,
            'jaw_width_mm': jaw_width_px * mm_per_pixel,
            'cheekbone_width_mm': cheekbone_width_px * mm_per_pixel,
            'forehead_width_mm': forehead_width_px * mm_per_pixel,
            'bridge_width_mm': bridge_width_px * mm_per_pixel,
            'lens_width_mm': lens_width_px * mm_per_pixel,
            'lens_height_mm': lens_height_px * mm_per_pixel,
            'temple_arm_length_mm': temple_length_px * mm_per_pixel,
            'pd_mm': pd_px * mm_per_pixel,
            'left_pupil': left_pupil,
            'right_pupil': right_pupil,
            'nose_bridge': lp(6),
            'left_eye_outer': left_eye_outer,
            'right_eye_outer': right_eye_outer
        }
    except Exception as e:
        logger.error(f"Error in compute_measurements: {str(e)}")
        return None

def classify_face_shape(params):
    try:
        face_width = params['face_width_mm']
        face_length = params['face_length_mm']
        jaw_width = params['jaw_width_mm']
        cheekbone_width = params['cheekbone_width_mm']
        forehead_width = params['forehead_width_mm']

        aspect_ratio = face_length / face_width if face_width else 1.0
        jaw_to_cheek_ratio = jaw_width / cheekbone_width if cheekbone_width else 1.0
        forehead_to_jaw_ratio = forehead_width / jaw_width if jaw_width else 1.0
        forehead_to_cheek_ratio = forehead_width / cheekbone_width if cheekbone_width else 1.0

        logger.info(f"Face Shape Ratios: aspect_ratio={aspect_ratio:.2f}, "
                    f"jaw_to_cheek={jaw_to_cheek_ratio:.2f}, "
                    f"forehead_to_jaw={forehead_to_jaw_ratio:.2f}, "
                    f"forehead_to_cheek={forehead_to_cheek_ratio:.2f}")

        shapes = {
            "Oval": {
                "aspect_range": (1.0, 1.5),
                "jaw_to_cheek_range": (0.8, 1.2),
                "forehead_to_cheek_range": (0.8, 1.2),
                "score": 0
            },
            "Round": {
                "aspect_range": (0.8, 1.2),
                "jaw_to_cheek_range": (0.9, 1.1),
                "forehead_to_cheek_range": (0.9, 1.1),
                "score": 0
            },
            "Square": {
                "aspect_range": (0.8, 1.2),
                "jaw_to_cheek_range": (0.7, 0.95),
                "forehead_to_jaw_range": (0.9, 1.2),
                "score": 0
            },
            "Oblong": {
                "aspect_range": (1.3, 1.8),
                "jaw_to_cheek_range": (0.8, 1.2),
                "forehead_to_cheek_range": (0.8, 1.2),
                "score": 0
            },
            "Heart": {
                "aspect_range": (1.0, 1.5),
                "forehead_to_cheek_range": (1.0, 1.3),
                "jaw_to_cheek_range": (0.6, 0.9),
                "score": 0
            },
            "Diamond": {
                "aspect_range": (1.0, 1.5),
                "cheekbone_to_forehead": (1.05, 1.3),
                "cheekbone_to_jaw": (1.05, 1.3),
                "score": 0
            },
            "Triangle": {
                "aspect_range": (1.0, 1.5),
                "jaw_to_forehead": (1.05, 1.3),
                "jaw_to_cheek": (1.05, 1.3),
                "score": 0
            }
        }

        for shape, criteria in shapes.items():
            score = 0
            if criteria.get("aspect_range") and criteria["aspect_range"][0] <= aspect_ratio <= criteria["aspect_range"][1]:
                score += 1
            if criteria.get("jaw_to_cheek_range") and criteria["jaw_to_cheek_range"][0] <= jaw_to_cheek_ratio <= criteria["jaw_to_cheek_range"][1]:
                score += 1
            if criteria.get("forehead_to_cheek_range") and criteria["forehead_to_cheek_range"][0] <= forehead_to_cheek_ratio <= criteria["forehead_to_cheek_range"][1]:
                score += 1
            if criteria.get("forehead_to_jaw_range") and criteria["forehead_to_jaw_range"][0] <= forehead_to_jaw_ratio <= criteria["forehead_to_jaw_range"][1]:
                score += 1
            if criteria.get("cheekbone_to_forehead") and cheekbone_width / forehead_width >= criteria["cheekbone_to_forehead"][0]:
                score += 1
            if criteria.get("cheekbone_to_jaw") and cheekbone_width / jaw_width >= criteria["cheekbone_to_jaw"][0]:
                score += 1
            if criteria.get("jaw_to_forehead") and jaw_width / forehead_width >= criteria["jaw_to_forehead"][0]:
                score += 1
            if criteria.get("jaw_to_cheek") and jaw_width / cheekbone_width >= criteria["jaw_to_cheek"][0]:
                score += 1
            shapes[shape]["score"] = score

        max_score = max(shape["score"] for shape in shapes.values())
        if max_score >= 2:
            best_shape = max(shapes, key=lambda s: shapes[s]["score"])
            logger.info(f"Classified face shape: {best_shape} (score={max_score})")
            return best_shape
        else:
            logger.info("Classified face shape: Standard (no strong match)")
            return "Standard"
    except Exception as e:
        logger.error(f"Error in classify_face_shape: {str(e)}")
        return "Standard"

def recommend_frame_type(face_shape):
    frame_map = {
        "Round": {
            "primary": "Rectangle",
            "secondary": ["Square", "Wayfarer", "Cat-Eye"],
            "why": "Angular frames like Rectangle contrast with rounded features for a balanced look."
        },
        "Square": {
            "primary": "Round",
            "secondary": ["Oval", "Aviator", "Cat-Eye"],
            "why": "Round frames soften strong jawlines and add curvature to angular faces."
        },
        "Oval": {
            "primary": "Wayfarer",
            "secondary": ["Round", "Rectangle", "Aviator"],
            "why": "Versatile shapes like Wayfarer complement balanced proportions."
        },
        "Oblong": {
            "primary": "Oval",
            "secondary": ["Round", "Aviator"],
            "why": "Wider frames like Oval add width to longer faces for better proportion."
        },
        "Heart": {
            "primary": "Oval",
            "secondary": ["Round", "Cat-Eye", "Rimless"],
            "why": "Oval frames balance wider cheekbones and narrower chins."
        },
        "Diamond": {
            "primary": "Cat-Eye",
            "secondary": ["Oval", "Rimless"],
            "why": "Cat-Eye frames highlight cheekbones and soften narrow foreheads."
        },
        "Triangle": {
            "primary": "Browline",
            "secondary": ["Cat-Eye", "Aviator"],
            "why": "Browline frames emphasize the upper face to balance wider jaws."
        },
        "Standard": {
            "primary": "Oval",
            "secondary": ["Rectangle", "Wayfarer"],
            "why": "Versatile shapes like Oval suit most face proportions comfortably."
        }
    }
    return frame_map.get(face_shape, {
        "primary": "Oval",
        "secondary": ["Rectangle", "Wayfarer"],
        "why": "Versatile shapes like Oval suit most face proportions comfortably."
    })

def recommend_frame_size(measurements):
    try:
        face_width_mm = measurements['face_width_mm']
        pd_mm = measurements['pd_mm']
        bridge_width_mm = measurements['bridge_width_mm']
        temple_arm_length_mm = measurements['temple_arm_length_mm']
        lens_height_mm = measurements['lens_height_mm']

        # Lens Width
        if face_width_mm < 125:
            rec_lens_width = "40-48mm"
            lens_width_desc = "Small lenses suit narrower faces."
        elif 125 <= face_width_mm <= 135:
            rec_lens_width = "48-54mm"
            lens_width_desc = "Medium lenses fit average face widths."
        else:
            rec_lens_width = "54-60mm"
            lens_width_desc = "Larger lenses complement wider faces."

        # Bridge Width
        if bridge_width_mm < 15:
            rec_bridge_width = "14-16mm (Narrow)"
            bridge_width_desc = "Narrow bridge for closer-set noses."
        elif 15 <= bridge_width_mm <= 19:
            rec_bridge_width = "17-20mm (Standard)"
            bridge_width_desc = "Standard bridge fits most nose shapes."
        else:
            rec_bridge_width = "21-24mm (Wide)"
            bridge_width_desc = "Wide bridge for broader noses."

        # Temple Length
        if temple_arm_length_mm < 135:
            rec_temple_length = "130-135mm (Short)"
            temple_length_desc = "Short temples for smaller heads."
        elif 135 <= temple_arm_length_mm <= 145:
            rec_temple_length = "140-145mm (Standard)"
            temple_length_desc = "Standard temples fit most head sizes."
        else:
            rec_temple_length = "150mm+ (Long)"
            temple_length_desc = "Long temples for larger heads."

        # Lens Height
        if lens_height_mm < 20:
            rec_lens_height = "28-34mm (Small)"
            lens_height_desc = "Smaller lenses for compact frames."
        elif 20 <= lens_height_mm <= 25:
            rec_lens_height = "34-40mm (Standard)"
            lens_height_desc = "Standard lenses for balanced proportions."
        else:
            rec_lens_height = "40-46mm (Large)"
            lens_height_desc = "Larger lenses for bold styles."

        # Frame Width
        frame_width_mm = face_width_mm + 10
        rec_frame_width = f"{frame_width_mm:.0f}-{frame_width_mm + 10:.0f}mm"
        frame_width_desc = "Slightly wider than your face for comfort."

        # Overall Size
        overall_size = "Medium"
        if face_width_mm < 128:
            overall_size = "Small"
            overall_size_desc = "Small frames suit petite faces."
        elif face_width_mm > 142:
            overall_size = "Large"
            overall_size_desc = "Large frames fit broader faces."
        else:
            overall_size_desc = "Medium frames are versatile for most faces."

        # Fit Preferences
        fit_notes = [
            "For a snug fit, choose a narrower bridge and shorter temples.",
            "For a bold look, opt for slightly larger lens widths and heights.",
            "Ensure frame width is 10-20mm wider than your face for comfort."
        ]

        return {
            'overall_size': overall_size,
            'overall_size_desc': overall_size_desc,
            'recommended_lens_width': rec_lens_width,
            'lens_width_desc': lens_width_desc,
            'recommended_bridge_width': rec_bridge_width,
            'bridge_width_desc': bridge_width_desc,
            'recommended_temple_length': rec_temple_length,
            'temple_length_desc': temple_length_desc,
            'recommended_lens_height': rec_lens_height,
            'lens_height_desc': lens_height_desc,
            'recommended_frame_width': rec_frame_width,
            'frame_width_desc': frame_width_desc,
            'fit_notes': fit_notes,
            'general_notes': "These measurements are guidelines. Try on frames to confirm comfort and style. Frame dimensions are typically listed as: Lens Width - Bridge Width - Temple Length (e.g., 52-18-140)."
        }
    except Exception as e:
        logger.error(f"Error in recommend_frame_size: {str(e)}")
        return {
            'overall_size': "Medium",
            'overall_size_desc': "Medium frames are versatile for most faces.",
            'recommended_lens_width': "48-54mm",
            'lens_width_desc': "Medium lenses fit average face widths.",
            'recommended_bridge_width': "17-20mm (Standard)",
            'bridge_width_desc': "Standard bridge fits most nose shapes.",
            'recommended_temple_length': "140-145mm (Standard)",
            'temple_length_desc': "Standard temples fit most head sizes.",
            'recommended_lens_height': "34-40mm (Standard)",
            'lens_height_desc': "Standard lenses for balanced proportions.",
            'recommended_frame_width': "130-140mm",
            'frame_width_desc': "Slightly wider than your face for comfort.",
            'fit_notes': [
                "For a snug fit, choose a narrower bridge and shorter temples.",
                "For a bold look, opt for slightly larger lens widths and heights.",
                "Ensure frame width is 10-20mm wider than your face for comfort."
            ],
            'general_notes': "These measurements are guidelines. Try on frames to confirm comfort and style."
        }

class VideoWorker(QThread):
    frame_ready = pyqtSignal(np.ndarray, dict)
    no_face_detected = pyqtSignal(np.ndarray)
    camera_error = pyqtSignal(str)
    status_update = pyqtSignal(str, str)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False
        self.cap = None
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1,
            min_detection_confidence=0.4,  # Lowered for performance
            min_tracking_confidence=0.4    # Lowered for performance
        )
        self.mm_per_pixel = FIXED_MM_PER_PIXEL
        self.current_params = None
        self.frame_image_path = None
        self.glasses_img = None
        self.glasses_target_ipd_px = 140
        self.last_pd_px = None
        self.stable_counter = 0
        self.STABILITY_THRESHOLD = 5
        self.PD_CHANGE_TOLERANCE = 5
        self.draw_mesh = True
        logger.info("VideoWorker initialized.")

    def set_camera_index(self, index):
        self.camera_index = index
        logger.info(f"Camera index set to {index}")

    def set_mm_per_pixel(self, value):
        self.mm_per_pixel = value
        logger.info(f"mm_per_pixel set to {value}")

    def set_frame_image(self, path):
        try:
            self.frame_image_path = path
            if path and path != "None":
                self.glasses_img = cv2.imread(resource_path(path), cv2.IMREAD_UNCHANGED)
                if self.glasses_img is None:
                    self.status_update.emit("Error loading frame image. Please check path.", "warning")
                    self.frame_image_path = None
                    self.draw_mesh = True
                    self.status_update.emit("Face mesh enabled.", "info")
                    logger.error(f"Failed to load frame image: {path}")
                else:
                    self.draw_mesh = False
                    self.status_update.emit(f"Frame image loaded: {path.split('/')[-1]}. Face mesh hidden for try-on.", "info")
                    logger.info(f"Frame image loaded: {path}")
            else:
                self.glasses_img = None
                self.draw_mesh = True
                self.status_update.emit("No frame image selected. Face mesh enabled.", "info")
                self.frame_image_path = None
                logger.info("Frame image cleared.")
        except Exception as e:
            logger.error(f"Error in set_frame_image: {str(e)}")
            self.status_update.emit("Error loading frame image.", "error")

    def run(self):
        try:
            self.running = True
            self.cap = cv2.VideoCapture(self.camera_index)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            if not self.cap.isOpened():
                self.camera_error.emit(f"Could not open camera {self.camera_index}. Check connection or try another camera.", "error")
                logger.error(f"Camera {self.camera_index} failed to open.")
                self.running = False
                return
            self.status_update.emit("Camera started. Detecting face...", "info")
            logger.info(f"Camera {self.camera_index} started.")

            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    self.camera_error.emit("Failed to grab frame from camera. Camera may have disconnected.", "error")
                    logger.error("Failed to grab camera frame.")
                    break

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = self.face_mesh.process(rgb)

                display_frame = np.copy(frame)

                params = None
                current_pd_px = 0

                if result.multi_face_landmarks:
                    for face_landmarks in result.multi_face_landmarks:
                        if self.draw_mesh:
                            mp_drawing.draw_landmarks(display_frame, face_landmarks,
                                                      mp.solutions.face_mesh.FACEMESH_TESSELATION,
                                                      landmark_drawing_spec=None,
                                                      connection_drawing_spec=mp_styles.get_default_face_mesh_tesselation_style())

                        params = compute_measurements(frame, face_landmarks, self.mm_per_pixel)
                        
                        if params:
                            self.current_params = params
                            current_pd_px = params['pd_px']

                            if self.last_pd_px is not None and abs(current_pd_px - self.last_pd_px) < self.PD_CHANGE_TOLERANCE:
                                self.stable_counter += 1
                            else:
                                self.stable_counter = 0
                            self.last_pd_px = current_pd_px

                            if self.stable_counter >= self.STABILITY_THRESHOLD:
                                self.status_update.emit("Measurements are stable.", "success")
                            else:
                                self.status_update.emit("Adjust position for stable measurements.", "info")

                            if self.glasses_img is not None and current_pd_px > 0:
                                scale_factor = current_pd_px / self.glasses_target_ipd_px
                                h_orig, w_orig = self.glasses_img.shape[:2]
                                target_width_px = int(w_orig * scale_factor)
                                target_height_px = int(h_orig * scale_factor)

                                if target_width_px > 0 and target_height_px > 0:
                                    resized_glasses = cv2.resize(self.glasses_img, (target_width_px, target_height_px), interpolation=cv2.INTER_AREA)

                                    glasses_left_lens = (target_width_px * 0.3, target_height_px * 0.5)
                                    glasses_right_lens = (target_width_px * 0.7, target_height_px * 0.5)

                                    left_pupil = params['left_pupil']
                                    right_pupil = params['right_pupil']

                                    src_pts = np.float32([
                                        glasses_left_lens,
                                        glasses_right_lens
                                    ])
                                    dst_pts = np.float32([
                                        left_pupil,
                                        right_pupil
                                    ])
                                    try:
                                        M = cv2.estimateAffinePartial2D(src_pts, dst_pts, method=cv2.RANSAC)[0]
                                        if M is not None:
                                            warped_glasses = cv2.warpAffine(resized_glasses, M,
                                                                            (frame.shape[1], frame.shape[0]),
                                                                            flags=cv2.INTER_LINEAR,
                                                                            borderMode=cv2.BORDER_CONSTANT,
                                                                            borderValue=(0, 0, 0, 0))

                                            if warped_glasses.shape[2] == 4:
                                                alpha_s = warped_glasses[:, :, 3] / 255.0
                                                alpha_l = 1.0 - alpha_s
                                                for c in range(0, 3):
                                                    display_frame[:, :, c] = (alpha_s * warped_glasses[:, :, c] +
                                                                             alpha_l * display_frame[:, :, c])
                                            else:
                                                mask = np.any(warped_glasses != 0, axis=2)
                                                display_frame[mask] = warped_glasses[mask]
                                        else:
                                            self.status_update.emit("Failed to compute glasses alignment.", "warning")
                                            logger.warning("Failed to compute glasses alignment.")
                                    except cv2.error as e:
                                        self.status_update.emit("Failed to align glasses image.", "warning")
                                        logger.error(f"OpenCV error in glasses alignment: {str(e)}")

                    if params is not None:
                        self.frame_ready.emit(display_frame, self.current_params)
                    else:
                        self.no_face_detected.emit(display_frame)
                else:
                    self.current_params = None
                    self.last_pd_px = None
                    self.stable_counter = 0
                    self.status_update.emit("No face detected. Please face the camera directly.", "warning")
                    self.no_face_detected.emit(display_frame)

                QThread.msleep(10)

        except Exception as e:
            logger.error(f"Error in VideoWorker.run: {str(e)}")
            self.camera_error.emit(f"Unexpected error: {str(e)}", "error")

    def stop(self):
        self.running = False
        self.wait()
        if self.cap:
            self.cap.release()
        if self.face_mesh:
            self.face_mesh.close()
        logger.info("VideoWorker stopped.")

class IPDInputDialog(QDialog):
    def __init__(self, current_pd_mm=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Your IPD")
        self.setModal(True)
        self.user_ipd = None

        layout = QFormLayout(self)
        self.ipd_input = QLineEdit()
        self.ipd_input.setPlaceholderText("e.g., 63.5")
        self.ipd_input.setValidator(QDoubleValidator(0.0, 100.0, 2))

        layout.addRow("Your Measured IPD (mm):", self.ipd_input)
        
        if current_pd_mm:
            info_label = QLabel(f"Current live measured PD: <b>{current_pd_mm:.1f} mm</b>")
            info_label.setStyleSheet("font-size: 14px;")
            layout.addRow(info_label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept_input)
        layout.addRow(ok_button)

    def accept_input(self):
        try:
            self.user_ipd = float(self.ipd_input.text())
            if self.user_ipd <= 0:
                raise ValueError("IPD must be positive.")
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid positive number for IPD (e.g., 63.5).")
            logger.warning("Invalid IPD input.")

class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Eyewear Recommender")
        self.setGeometry(100, 100, 1200, 850)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.left_layout = QVBoxLayout()
        self.camera_label = QLabel("Camera Feed")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setFixedSize(640, 480)
        self.camera_label.setStyleSheet("""
            border: 3px dashed #666;
            background-color: #333;
            color: #AAA;
            font-size: 20px;
            font-weight: bold;
            padding: 20px;
        """)
        self.left_layout.addWidget(self.camera_label)

        self.status_label = QLabel("Waiting to start camera...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            background-color: #333;
            color: white;
            padding: 8px;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.left_layout.addWidget(self.status_label)

        self.camera_controls_layout = QHBoxLayout()
        self.camera_selector = QComboBox()
        self.populate_camera_options()
        self.camera_selector.setStyleSheet("font-size: 14px; padding: 5px; border: 1px solid #AAA;")
        self.camera_controls_layout.addWidget(self.camera_selector)

        self.start_button = QPushButton("Start Camera")
        self.start_button.clicked.connect(self.start_camera)
        self.start_button.setStyleSheet("font-size: 14px; padding: 8px; background-color: #28a745; color: white; border-radius: 5px;")
        self.camera_controls_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Camera")
        self.stop_button.clicked.connect(self.stop_camera)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("font-size: 14px; padding: 8px; background-color: #dc3545; color: white; border-radius: 5px;")
        self.camera_controls_layout.addWidget(self.stop_button)
        
        self.left_layout.addLayout(self.camera_controls_layout)

        self.frame_controls_layout = QHBoxLayout()
        self.select_frame_button = QPushButton("Select Frame Image for Try-On")
        self.select_frame_button.clicked.connect(self.select_frame_image)
        self.select_frame_button.setStyleSheet("font-size: 14px; padding: 8px; background-color: #007bff; color: white; border-radius: 5px;")
        self.frame_controls_layout.addWidget(self.select_frame_button)

        self.clear_frame_button = QPushButton("Clear Frame Try-On")
        self.clear_frame_button.clicked.connect(self.clear_frame_image)
        self.clear_frame_button.setEnabled(False)
        self.clear_frame_button.setStyleSheet("font-size: 14px; padding: 8px; background-color: #6c757d; color: white; border-radius: 5px;")
        self.frame_controls_layout.addWidget(self.clear_frame_button)
        self.left_layout.addLayout(self.frame_controls_layout)

        self.left_layout.addStretch()
        self.main_layout.addLayout(self.left_layout)

        self.right_layout = QVBoxLayout()

        self.measurements_label = QLabel("LIVE MEASUREMENTS:")
        self.measurements_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 10px; margin-bottom: 5px; color: #0056b3;")
        self.right_layout.addWidget(self.measurements_label)
        
        self.measurements_display = QTextEdit()
        self.measurements_display.setReadOnly(True)
        self.measurements_display.setStyleSheet("""
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 16px;
            color: #333;
            background-color: #e9ecef;
            border: 1px solid #ced4da;
            padding: 12px;
            border-radius: 8px;
        """)
        self.right_layout.addWidget(self.measurements_display)

        self.capture_button = QPushButton("Capture Measurements & Get Recommendation")
        self.capture_button.clicked.connect(self.capture_and_recommend)
        self.capture_button.setStyleSheet("font-size: 16px; padding: 12px; background-color: #17a2b8; color: white; margin-top: 15px; border-radius: 5px;")
        self.right_layout.addWidget(self.capture_button)

        self.recalibrate_button = QPushButton("Recalibrate Scale (Enter Your IPD)")
        self.recalibrate_button.clicked.connect(self.prompt_for_ipd_recalibration)
        self.recalibrate_button.setStyleSheet("font-size: 16px; padding: 12px; background-color: #ffc107; color: #212529; margin-top: 10px; border-radius: 5px;")
        self.right_layout.addWidget(self.recalibrate_button)

        self.recommendation_label = QLabel("FRAME RECOMMENDATIONS:")
        self.recommendation_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 5px; color: #0056b3;")
        self.right_layout.addWidget(self.recommendation_label)

        self.recommendation_display = QTextEdit()
        self.recommendation_display.setReadOnly(True)
        self.recommendation_display.setStyleSheet("""
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 16px;
            color: #333;
            background-color: #e9ecef;
            border: 1px solid #ced4da;
            padding: 12px;
            border-radius: 8px;
        """)
        self.right_layout.addWidget(self.recommendation_display)
        
        self.right_layout.addStretch()
        self.main_layout.addLayout(self.right_layout)

        self.video_worker = None
        self.current_frame_params = None
        logger.info("FaceRecognitionApp initialized.")

        QApplication.instance().aboutToQuit.connect(self.closeEvent)

    def populate_camera_options(self):
        try:
            self.camera_selector.clear()
            for i in range(5):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    self.camera_selector.addItem(f"Camera {i} (Available)")
                    cap.release()
                else:
                    self.camera_selector.addItem(f"Camera {i} (Unavailable)")
            if self.camera_selector.count() > 0 and "Available" in self.camera_selector.itemText(0):
                self.camera_selector.setCurrentIndex(0)
            logger.info("Camera options populated.")
        except Exception as e:
            logger.error(f"Error in populate_camera_options: {str(e)}")

    def start_camera(self):
        try:
            if self.video_worker and self.video_worker.isRunning():
                self.video_worker.stop()
                self.video_worker.wait()

            selected_index_str = self.camera_selector.currentText()
            try:
                camera_index = int(selected_index_str.split(' ')[1].split('(')[0])
            except (IndexError, ValueError):
                camera_index = 0

            self.video_worker = VideoWorker(camera_index)
            self.video_worker.frame_ready.connect(self.update_frame)
            self.video_worker.no_face_detected.connect(self.update_frame_no_face)
            self.video_worker.camera_error.connect(self.handle_camera_error)
            self.video_worker.status_update.connect(self.update_status)
            
            if hasattr(self, 'selected_frame_path') and self.selected_frame_path:
                self.video_worker.set_frame_image(self.selected_frame_path)
            else:
                self.video_worker.set_frame_image(None)

            self.video_worker.start()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.select_frame_button.setEnabled(True)
            self.clear_frame_button.setEnabled(True if hasattr(self, 'selected_frame_path') and self.selected_frame_path else False)
            self.measurements_display.clear()
            self.recommendation_display.clear()
            self.measurements_display.setText("Starting camera and detecting face...")
            self.update_status("Camera initializing...", "info")
            logger.info("Camera started.")
        except Exception as e:
            logger.error(f"Error in start_camera: {str(e)}")
            self.update_status("Failed to start camera.", "error")

    def stop_camera(self):
        try:
            if self.video_worker and self.video_worker.isRunning():
                self.video_worker.stop()
                self.video_worker.wait()
                self.camera_label.clear()
                self.camera_label.setText("Camera Feed Stopped")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.select_frame_button.setEnabled(False)
            self.clear_frame_button.setEnabled(False)
            self.measurements_display.clear()
            self.measurements_display.setText("Camera is stopped.")
            self.recommendation_display.clear()
            self.update_status("Camera stopped.", "info")
            self.clear_frame_image()
            logger.info("Camera stopped.")
        except Exception as e:
            logger.error(f"Error in stop_camera: {str(e)}")

    def update_frame(self, frame, params):
        try:
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
            p = convert_to_qt_format.scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.camera_label.setPixmap(QPixmap.fromImage(p))
            
            self.current_frame_params = params

            if params:
                face_shape = classify_face_shape(params)
                measure_text = (
                    f"<b>Face Shape:</b> {face_shape}<br>"
                    f"<b>PD:</b> {params['pd_mm']:.1f} mm ({params['pd_px']:.1f} px)<br>"
                    f"<b>Face Width:</b> {params['face_width_mm']:.1f} mm<br>"
                    f"<b>Face Length:</b> {params['face_length_mm']:.1f} mm<br>"
                    f"<b>Jaw Width:</b> {params['jaw_width_mm']:.1f} mm<br>"
                    f"<b>Cheekbone Width:</b> {params['cheekbone_width_mm']:.1f} mm<br>"
                    f"<b>Forehead Width:</b> {params['forehead_width_mm']:.1f} mm<br>"
                    f"<b>Bridge Width:</b> {params['bridge_width_mm']:.1f} mm<br>"
                    f"<b>Lens (W x H):</b> {params['lens_width_mm']:.1f} x {params['lens_height_mm']:.1f} mm<br>"
                    f"<b>Temple Arm Length:</b> {params['temple_arm_length_mm']:.1f} mm<br>"
                    f"<b>Scale Used:</b> {self.video_worker.mm_per_pixel:.4f} mm/pixel"
                )
                self.measurements_display.setHtml(measure_text)
            else:
                self.measurements_display.setText("No face detected for measurements.")
        except Exception as e:
            logger.error(f"Error in update_frame: {str(e)}")

    def update_frame_no_face(self, frame):
        try:
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
            p = convert_to_qt_format.scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.camera_label.setPixmap(QPixmap.fromImage(p))
            self.current_frame_params = None
            self.measurements_display.setText("No face detected. Adjust your position.")
        except Exception as e:
            logger.error(f"Error in update_frame_no_face: {str(e)}")

    def handle_camera_error(self, message):
        try:
            self.stop_camera()
            QMessageBox.critical(self, "Camera Error", message)
            self.update_status(f"Camera Error: {message}", "error")
            self.camera_label.setText("Camera Error: Check console/logs and reconnect.")
            logger.error(f"Camera error: {message}")
        except Exception as e:
            logger.error(f"Error in handle_camera_error: {str(e)}")

    def update_status(self, message, msg_type="info"):
        try:
            if msg_type == "info":
                self.status_label.setStyleSheet("background-color: #333; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
            elif msg_type == "warning":
                self.status_label.setStyleSheet("background-color: #ffc107; color: black; padding: 8px; border-radius: 5px; font-weight: bold;")
            elif msg_type == "error":
                self.status_label.setStyleSheet("background-color: #dc3545; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
            elif msg_type == "success":
                self.status_label.setStyleSheet("background-color: #28a745; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
            self.status_label.setText(message)
        except Exception as e:
            logger.error(f"Error in update_status: {str(e)}")

    def capture_and_recommend(self):
        try:
            if self.video_worker and not self.video_worker.running:
                self.recommendation_display.setText("Please start the camera first.")
                logger.warning("Capture attempted without camera running.")
                return

            if not self.current_frame_params:
                self.recommendation_display.setText("No face detected for measurements. Please position yourself correctly.")
                self.update_status("Cannot capture: No face detected.", "warning")
                logger.warning("Capture attempted without face detected.")
                return

            face_shape = classify_face_shape(self.current_frame_params)
            frame_type = recommend_frame_type(face_shape)
            size_recommendations = recommend_frame_size(self.current_frame_params)

            recommendation_text = (
                f"<div style='font-family: Segoe UI, Arial; font-size: 16px;'>"
                f"<h2 style='color: #0056b3; margin-bottom: 10px;'>Your Eyewear Recommendation</h2>"

                f"<h3 style='color: #007bff; margin-top: 15px;'>Face Shape Analysis</h3>"
                f"<ul style='margin-left: 20px;'>"
                f"<li><strong>Detected Shape:</strong> {face_shape}</li>"
                f"</ul>"

                f"<h3 style='color: #007bff; margin-top: 15px;'>Recommended Frame Types</h3>"
                f"<ul style='margin-left: 20px;'>"
                f"<li><strong>Primary Style:</strong> {frame_type['primary']} - {frame_type['why']}</li>"
                f"<li><strong>Other Options:</strong> {', '.join(frame_type['secondary'])}</li>"
                f"</ul>"

                f"<h3 style='color: #007bff; margin-top: 15px;'>Frame Size Recommendations</h3>"
                f"<ul style='margin-left: 20px;'>"
                f"<li><strong>Overall Size:</strong> {size_recommendations['overall_size']} - {size_recommendations['overall_size_desc']}</li>"
                f"<li><strong>Frame Width:</strong> {size_recommendations['recommended_frame_width']} - {size_recommendations['frame_width_desc']}</li>"
                f"<li><strong>Lens Width:</strong> {size_recommendations['recommended_lens_width']} - {size_recommendations['lens_width_desc']}</li>"
                f"<li><strong>Lens Height:</strong> {size_recommendations['recommended_lens_height']} - {size_recommendations['lens_height_desc']}</li>"
                f"<li><strong>Bridge Width:</strong> {size_recommendations['recommended_bridge_width']} - {size_recommendations['bridge_width_desc']}</li>"
                f"<li><strong>Temple Length:</strong> {size_recommendations['recommended_temple_length']} - {size_recommendations['temple_length_desc']}</li>"
                f"</ul>"

                f"<h3 style='color: #007bff; margin-top: 15px;'>Fit and Style Tips</h3>"
                f"<ul style='margin-left: 20px;'>"
                f"{'<li>' + '</li><li>'.join(size_recommendations['fit_notes']) + '</li>'}"
                f"</ul>"

                f"<p style='font-style: italic; margin-top: 15px;'>{size_recommendations['general_notes']}</p>"
                f"</div>"
            )
            self.recommendation_display.setHtml(recommendation_text)
            self.update_status("Recommendation generated!", "success")
            logger.info("Recommendation generated successfully.")
        except Exception as e:
            logger.error(f"Error in capture_and_recommend: {str(e)}")
            self.update_status("Failed to generate recommendation.", "error")

    def prompt_for_ipd_recalibration(self):
        try:
            if not self.current_frame_params or self.current_frame_params['pd_px'] == 0:
                QMessageBox.warning(self, "No Face Detected", "Please ensure a face is detected in the camera feed before calibrating with IPD.")
                logger.warning("IPD recalibration attempted without face detected.")
                return

            dialog = IPDInputDialog(self.current_frame_params.get('pd_mm'), self)
            if dialog.exec_() == QDialog.Accepted:
                user_ipd = dialog.user_ipd
                if user_ipd is not None and user_ipd > 0:
                    current_pd_pixels = self.current_frame_params['pd_px']
                    if current_pd_pixels > 0:
                        new_mm_per_pixel = user_ipd / current_pd_pixels
                        self.video_worker.set_mm_per_pixel(new_mm_per_pixel)
                        QMessageBox.information(self, "Calibration Successful",
                                                f"Scale recalibrated to {new_mm_per_pixel:.4f} mm/pixel "
                                                f"using your IPD of {user_ipd:.1f} mm.")
                        self.update_status(f"Scale recalibrated to {new_mm_per_pixel:.4f} mm/pixel.", "success")
                        logger.info(f"IPD recalibration successful: {new_mm_per_pixel} mm/pixel")
                    else:
                        QMessageBox.warning(self, "Recalibration Error", "Could not get pixel PD. Please ensure a face is visible.")
                        self.update_status("Recalibration failed: No pixel PD.", "error")
                        logger.error("IPD recalibration failed: No pixel PD.")
                else:
                    QMessageBox.warning(self, "Invalid IPD", "IPD must be a positive number.")
                    self.update_status("Recalibration failed: Invalid IPD.", "error")
                    logger.error("IPD recalibration failed: Invalid IPD.")
        except Exception as e:
            logger.error(f"Error in prompt_for_ipd_recalibration: {str(e)}")

    def select_frame_image(self):
        try:
            file_dialog = QFileDialog(self)
            file_dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg)")
            file_dialog.setWindowTitle("Select Glasses Frame Image")
            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    self.selected_frame_path = selected_files[0]
                    if self.video_worker and self.video_worker.isRunning():
                        self.video_worker.set_frame_image(self.selected_frame_path)
                    self.clear_frame_button.setEnabled(True)
                    self.update_status(f"Selected frame: {self.selected_frame_path.split('/')[-1]}", "info")
                    logger.info(f"Selected frame image: {self.selected_frame_path}")
                else:
                    self.update_status("No frame image selected.", "info")
                    logger.info("No frame image selected.")
        except Exception as e:
            logger.error(f"Error in select_frame_image: {str(e)}")
            self.update_status("Failed to select frame image.", "error")

    def clear_frame_image(self):
        try:
            self.selected_frame_path = None
            if self.video_worker and self.video_worker.isRunning():
                self.video_worker.set_frame_image(None)
            self.clear_frame_button.setEnabled(False)
            self.update_status("Frame try-on cleared.", "info")
            logger.info("Frame try-on cleared.")
        except Exception as e:
            logger.error(f"Error in clear_frame_image: {str(e)}")

    def closeEvent(self, event):
        try:
            if self.video_worker and self.video_worker.isRunning():
                self.video_worker.stop()
                self.video_worker.wait()
            logger.info("Application closed.")
            event.accept()
        except Exception as e:
            logger.error(f"Error in closeEvent: {str(e)}")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = FaceRecognitionApp()
        window.show()
        logger.info("Application started.")
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"Application startup error: {str(e)}")
