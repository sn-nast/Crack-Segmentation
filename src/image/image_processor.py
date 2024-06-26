import cv2
from utility.file_utils import *
from utility.project import *
from .image_utils import *


class ImageProcessor:
    def __init__(self, image_path: str):
        self.kernel_size = None
        self.image_path: str = image_path
        self.image: cv2.typing.MatLike = self.__load_image_grayscale()
        self.set_kernel_size()

    # TODO: draft
    def __load_image(self, flags: int = cv2.IMREAD_UNCHANGED) -> cv2.typing.MatLike:
        image = cv2.imread(self.image_path, flags)
        check_loaded_image(image)
        print(f"type: {type(image)}")
        return image

    def __load_image_grayscale(self) -> cv2.typing.MatLike:
        image = self.__load_image(cv2.IMREAD_GRAYSCALE)
        return image

    # TODO: Draft
    def convert_image_grayscale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def set_kernel_size(self, size: int = 3):
        self.kernel_size: np.ndarray = np.ones((size, size), np.uint8)

    def do_adaptive_mean(self, block_size: int = 199, constant: int = 5):
        self.image = cv2.adaptiveThreshold(
            self.image,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            block_size,
            constant,
        )
        return self

    def do_adaptive_gaussian(self, block_size: int = 199, constant: int = 5):
        self.image = cv2.adaptiveThreshold(
            self.image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size,
            constant,
        )
        return self

    def do_adaptive_mean_fix1(self):
        return (
            self.do_adaptive_mean(111, 13)
            .do_denoise_morphology_close()
            .do_denoise_morphology_open()
        )

    def do_equalize_histogram(self):
        self.image = cv2.equalizeHist(self.image)
        return self
        return self

    def do_denoise_morphology_close(self):
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, self.kernel_size)
        return self

    def do_denoise_morphology_open(self):
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, self.kernel_size)
        return self

    def do_denoise(self):
        self.image = cv2.fastNlMeansDenoising(self.image, None)
        return self

    def do_denoise_morphology_combined(self):
        return self.do_denoise_morphology_close().do_denoise_morphology_open()

    # TODO: Fix
    def do_sobel_combined(self):
        sobel_x = cv2.Sobel(self.image, cv2.CV_64F, 1, 0)
        sobel_y = cv2.Sobel(self.image, cv2.CV_64F, 0, 1)
        self.image = cv2.bitwise_or(sobel_x, sobel_y)
        return self

    def do_sobel_x(self):
        self.image = cv2.Sobel(self.image, cv2.CV_64F, 1, 0)
        return self

    def do_sobel_y(self):
        self.image = cv2.Sobel(self.image, cv2.CV_64F, 0, 1)
        return self

    def do_canny(self, min_threshold: float = 10, max_threshold: float = 200):
        self.image = cv2.Canny(self.image, min_threshold, max_threshold)
        return self

    def do_laplacian(self):
        temp_transform = cv2.Laplacian(self.image, cv2.CV_64F, ksize=5)
        # self.image = np.uint8(np.absolute(temp_transform))
        self.image = np.absolute(temp_transform).astype(np.uint8)
        return self

    def export_image(self, file_name: str, folder_path: str = "../output/"):
        if not is_path_exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.images_path.join(folder_path, file_name)
        cv2.imwrite(file_path, self.image)

    def flip_image(self, flip_code: int = 0):
        self.image = cv2.flip(self.image, flip_code)
        return self

    def reset_image(self):
        self.image = self.__load_image_grayscale()

    def get_contours(self):
        return cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def is_image_loaded(self):
        return self.image is not None

    def show(self, window_name: str = "My Image", size_x: int = 500, size_y: int = 650):
        show_image(image=self.image, window_name=window_name, size_x=size_x, size_y=size_y)
