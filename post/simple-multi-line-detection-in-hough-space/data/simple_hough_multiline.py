from dataclasses import dataclass
from typing import Sequence

import cv2 as cv
import numpy as np
import numpy.typing as npt


@dataclass
class LineVoteResult:
    theta: float
    rho: float
    votes: int


@dataclass
class HoughAccumulator:
    row_index_to_rho: Sequence[float]  # rho values for accumulator rows
    col_index_to_theta_rad: Sequence[float]  # theta values for accumulator columns
    rho_resolution: float
    theta_resolution: float
    votes: npt.NDArray[np.int32]  # accumulator array

    @classmethod
    def create_empty(
        cls,
        rho_max: float,
        rho_min: float = 0,
        rho_resolution: float = 1,
        theta_max: float = np.pi,
        theta_min: float = 0,
        theta_resolution: float = np.pi / 180,
    ) -> "HoughAccumulator":
        rho_count = int((rho_max - rho_min) / rho_resolution)
        theta_count = int((theta_max - theta_min) / theta_resolution)
        accumulator = np.zeros((rho_count, theta_count), dtype=np.int32)
        row_index_to_rho = np.arange(rho_count, dtype=np.float32) * rho_resolution + rho_min
        col_index_to_theta_rad = np.arange(theta_count, dtype=np.float32) * theta_resolution + theta_min
        return cls(row_index_to_rho, col_index_to_theta_rad, rho_resolution, theta_resolution, accumulator)
    
    @classmethod
    def build_from_binarized_image(cls, image: npt.NDArray[np.uint8], rho_resolution: float = 1, theta_resolution: float = np.pi / 180) -> "HoughAccumulator":
        rho_max = int(np.sqrt(image.shape[0]**2 + image.shape[1]**2) + 0.5)
        hough = cls.create_empty(rho_max, rho_resolution=rho_resolution, theta_resolution=theta_resolution)
        hough.add_votes(image)
        return hough
        
    def add_votes(self, binarized_image: npt.NDArray[np.uint8]) -> None:
        y_indices, x_indices = np.indices(binarized_image.shape)
        mask = binarized_image > 0
        x = x_indices[mask].reshape(-1, 1)
        y = y_indices[mask].reshape(-1, 1)
        n = np.prod(x.shape)

        theta_count = len(self.col_index_to_theta_rad)
        thetas = np.tile(self.col_index_to_theta_rad, n).reshape(n, -1)
        theta_indices = np.tile(np.arange(theta_count), n).reshape(n, -1).astype(np.int32)

        rho_count = len(self.row_index_to_rho)
        rho_values = x * np.cos(thetas) + y * np.sin(thetas)
        rho_indices = np.around(rho_values / self.rho_resolution).astype(np.int32)

        rho_indices_flat = rho_indices.flatten()
        theta_indices_flat = theta_indices.flatten()
        flat_mask = (rho_indices_flat >= 0) & (rho_indices_flat < rho_count) & (theta_indices_flat >= 0) & (theta_indices_flat < theta_count)
        flat_indices = np.ravel_multi_index((rho_indices_flat[flat_mask], theta_indices_flat[flat_mask]), self.votes.shape)
        counts = np.bincount(flat_indices)
        counts_mask = counts > 0
        self.votes.flat[np.arange(len(counts))[counts_mask]] += counts[counts_mask]
    
    def get_maximum_vote(self, min_votes: int | None = None) -> LineVoteResult | None:
        rho_index, theta_index = np.unravel_index(np.argmax(self.votes), self.votes.shape)
        max_votes = self.votes[rho_index, theta_index]
        if min_votes is not None and max_votes < min_votes:
            return None
        theta = self.col_index_to_theta_rad[theta_index]
        rho = self.row_index_to_rho[rho_index]
        return LineVoteResult(theta, rho, int(max_votes))
    
    def visualize(self, brightness: float = 1, maximum_value: float | None = None) -> npt.NDArray[np.uint8]:
        maximum_value = maximum_value or self.votes.max()
        votes_norm = self.votes.astype(np.float32) * 255 / maximum_value
        return np.clip(votes_norm * brightness, 0, 255).astype(np.uint8)


def imshow(image: npt.NDArray[np.uint8], title: str | None = None, debug: bool = False, wait: bool = False) -> None:
    if debug:
        cv.imshow(title, image)
        if wait:
            cv.waitKey()


def set_image_around_line(im: npt.NDArray[np.uint8], value: int | tuple[int, int, int], theta: float, rho: float, rho_delta: float) -> None:
    ys, xs = np.indices(im.shape[:2])
    im_rho = xs * np.cos(theta) + ys * np.sin(theta)
    mask = (im_rho > rho - rho_delta) & (im_rho < rho + rho_delta)
    im[mask] = value


def detect_lines(binarized_image: npt.NDArray[np.uint8], min_length: int, line_thickness: int, rho_resolution: float = 1, theta_resolution: float = np.pi / 180, debug: bool = False) -> Sequence[LineVoteResult]:
    lines = []

    hough = HoughAccumulator.build_from_binarized_image(binarized_image, rho_resolution=rho_resolution, theta_resolution=theta_resolution)
    max_line = hough.get_maximum_vote(min_votes=min_length)
    imshow(binarized_image, title=f"input", debug=debug)
    imshow(hough.visualize(4), title=f"hough", debug=debug, wait=True)
    line0 = max_line

    while max_line is not None:
        lines.append(max_line)
        set_image_around_line(binarized_image, 0, max_line.theta, max_line.rho, line_thickness)

        hough = HoughAccumulator.build_from_binarized_image(binarized_image, rho_resolution=rho_resolution, theta_resolution=theta_resolution)
        max_line = hough.get_maximum_vote(min_votes=min_length)
        imshow(binarized_image, title=f"input", debug=debug)
        imshow(hough.visualize(4, maximum_value=line0.votes), title=f"hough", debug=debug, wait=True)

    return lines

# -------------------------------------------------------------------------------------------------

def dev() -> None:
    im = cv.imread("highway50_cropped.jpg")
    
    im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    im_blurred = cv.GaussianBlur(im_gray, (5, 5), 0)
    #cv.imshow("gray", im_blurred)
    
    im_edge = cv.Canny(im_blurred, 100, 200)
    #cv.imshow("edge", im_edge)

    hough = HoughAccumulator.build_from_binarized_image(im_edge, theta_resolution=np.pi / 360)
    cv.imshow("hough", hough.visualize(brightness=4))
    
    cv.waitKey()
    cv.destroyAllWindows()


def main() -> None:
    im = cv.imread("highway50_cropped.jpg")
    debug = True
    
    im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    im_blurred = cv.GaussianBlur(im_gray, (5, 5), 0)
    im_edge = cv.Canny(im_blurred, 100, 200)

    min_length = min(im_edge.shape) * 0.3
    lines = detect_lines(
        im_edge,
        min_length=min_length,
        line_thickness=8,
        rho_resolution=1,
        theta_resolution=np.pi / 360,
        debug=debug,
    )

    for line in lines:
        print(line)

        if debug:
            set_image_around_line(im, (50, 255, 0), line.theta, line.rho, rho_delta=2)
            imshow(im, title=f"input_with_lines", debug=debug, wait=True)
    
    cv.waitKey()
    cv.destroyAllWindows()


if __name__ == "__main__":
    # dev()
    main()

