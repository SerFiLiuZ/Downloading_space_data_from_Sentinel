import main

domen_ = 'https://apps.sentinel-hub.com/sentinel-playground'
source_ = 'S2L2A'
lat_ = '47.26571797013935'
lng_ = '47.076072692871094'
zoom_ = '11'
preset_ = '5_MOISTURE_INDEX' # 1_TRUE_COLOR 2_FALSE_COLOR 3_NDVI 4_FALSE_COLOR__URBAN 5_MOISTURE_INDEX
layers_ = 'B01,B02,B03'
maxcc_ = '20'
gain_ = '1.0'
gamma_ = '1.0'
time_ = '2022-01-01%7C2022-07-18'
atmFilter_ = ''
showDates_ = 'false'
path_to_folder_download = r'C:/Users/User/Downloads'
path_to_folder_images = r"C:/Test"
name_files = "new name file"

main.downloading_space_data(domen_, source_, lat_, lng_,
                            zoom_, preset_, layers_, maxcc_,
                            gain_, gamma_, time_, atmFilter_, showDates_,
                            path_to_folder_download, path_to_folder_images, name_files)


