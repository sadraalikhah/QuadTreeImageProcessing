import cv2
import csv
import numpy as np
import os
from matplotlib import pyplot as plt
from QuadTree import QuadTree


class VideoProcessor:
    def video_to_frames(self, video_file):
        cap = cv2.VideoCapture(video_file)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        return frames
    def save_frame_to_csv(self, frame, frame_index, output_folder):

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if len(frame.shape) == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flattened_frame = frame.flatten()
        frame_filename = os.path.join(output_folder, f"frame_{frame_index}.csv")
        with open(frame_filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(flattened_frame)
    def csv_to_image_array(self, csv_file):
        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        data = [int(cell) for row in data for cell in row]

        return data
    def compress_frame(self, frame, target_size):
        return QuadTree(frame).compress(target_size)

    def frames_to_video(self, frames, output_video, frame_size, fps=7.0):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_video, fourcc, fps, frame_size)
        for frame in frames:
            writer.write(frame)

        writer.release()

    def compress_video(self, video_file, output_video, output_folder, target_size):
        frames = self.video_to_frames(video_file)
        for i, frame in enumerate(frames):
            self.save_frame_to_csv(frame, i, output_folder)
        compressed_frames = []
        for i in range(len(frames)):
            frame_filename = os.path.join(output_folder, f"frame_{i}.csv")
            frame_data = self.csv_to_image_array(frame_filename)
            compressed_frame = self.compress_frame(frame_data, target_size)
            compressed_frames.append(compressed_frame)
        self.frames_to_video(compressed_frames, output_video, target_size)
        print("Video compression complete!")





# تست کد
if __name__ == "__main__":
    video_processor = VideoProcessor()


    video_file = "vid1.mov"
    output_video = "compressed_video.mov"
    output_folder = "frames_csv"
    target_size = 64

    video_processor.compress_video(video_file, output_video, output_folder, target_size)









