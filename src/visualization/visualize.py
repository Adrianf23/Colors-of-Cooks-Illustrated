from pathlib import Path

import gif_maker as gif_m


def main():
    og_image_list: list[str] = gif_m.get_filtered_images()
    destination_path: Path = Path.cwd() / "data" / "processed" / "final-image-folder"

    Path.mkdir(destination_path, exist_ok=True)

    gif_m.transfer_files(source=og_image_list, destination_path=destination_path)

    magazine_squares_filepath: Path = (
        Path.cwd() / "data" / "processed" / "kmeans-squares"
    )
    gif_m.transfer_files(
        source=magazine_squares_filepath, destination_path=destination_path
    )

    final_img_filepath: Path = (
        Path.cwd() / "reports" / "figures" / "magazine-covers.gif"
    )
    gif_m.make_gif(frame_folder=destination_path, output_file=final_img_filepath)

    compressed_final_img_filepath: Path = (
        Path.cwd() / "reports" / "figures" / "compressed-magazine-covers.gif"
    )
    gif_m.compress_gif(
        image=final_img_filepath, output_file=compressed_final_img_filepath
    )


if __name__ == "__main__":
    main()
