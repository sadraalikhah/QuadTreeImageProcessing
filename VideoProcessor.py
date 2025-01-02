import cv2
import csv
import numpy as np
import os

from matplotlib import pyplot as plt

from QuadTree import QuadTree


class VideoProcessor:
    def frame_generator(self, video):
        cap = cv2.VideoCapture(video)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        return frames
    def frame_to_csv_convertor(self, frame, frame_index, folder):

        if not os.path.exists(folder):
            os.makedirs(folder)

        if len(frame.shape) == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flat_frame = frame.flatten()
        frame_name = os.path.join(output_folder, f"frame_{frame_index}.csv")
        with open(frame_name, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(flat_frame)
    def csv_to_image_array(self, csv_file):
        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        data = [int(cell) for row in data for cell in row]

        return data
    def frame_compressor(self, frame, target_size):
        return QuadTree(frame).compress(target_size)

    def frames_to_video(self, frames, output_video, frame_size, fps=7.0):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_video, fourcc, fps, (frame_size, frame_size))
        for frame in frames:
            if frame.shape[:2] != (frame_size, frame_size):
                frame = cv2.resize(frame, (frame_size, frame_size))
            writer.write(frame.astype(np.uint8))
        writer.release()

    def compress_video(self, video, output_video, folder, target_size):
        frames = self.frame_generator(video)
        for i, frame in enumerate(frames):
            self.frame_to_csv_convertor(frame, i, folder)
        compressed_frames = []
        for i in range(len(frames)):
            frame_filename = os.path.join(folder, f"frame_{i}.csv")
            frame_data = self.csv_to_image_array(frame_filename)
            compressed_frame = self.frame_compressor(frame_data, target_size)
            compressed_frames.append(compressed_frame)
            print(f"frame {i} created successfully")
        self.frames_to_video(compressed_frames, output_video, target_size)
        print("Video compression complete!")





# only and only for testing frames

    def csv_to_image(self, csv_file_path):

        pixel_values = []

        # Read the CSV file
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                pixel_values.extend([int(value) for value in row])
        total_pixels = len(pixel_values)
        suggested_shape = None

        for i in range(1, int(total_pixels ** 0.5) + 1):
            if total_pixels % i == 0:
                suggested_shape = (i, total_pixels // i)

        if suggested_shape is None:
            raise ValueError("Cannot determine a valid shape for the image.")

        print(f"Total pixels: {total_pixels}. Suggested shape: {suggested_shape}")
        return np.array(pixel_values).reshape(suggested_shape)

    def display_image(self, image_array):
        plt.imshow(image_array, cmap='gray')
        plt.axis('off')
        plt.show()








# تست کد
if __name__ == "__main__":
    video_processor = VideoProcessor()


    video = "vid1.mov"
    output_video = "compressed_video.mp4"
    output_folder = "frames_csv"
    target_size = 64


    # only for testing the functions

    # video_processor.compress_video(video, output_video, output_folder, target_size)

    # frame_generator,frame_to_csv_convertor test

    frames = video_processor.frame_generator(video)
    for i in range(len(frames)):
        x = frames[i]
        video_processor.frame_to_csv_convertor(x,i,output_folder)
    csv_file_path = 'frames_csv/frame_0.csv'
    array = video_processor.csv_to_image_array(csv_file_path)
    print(array)

    img2 = video_processor.frame_compressor(array,32)
    img = video_processor.csv_to_image(csv_file_path)
    # csv check
    video_processor.display_image(img)
    # compressed check
    video_processor.display_image(img2)

    #














