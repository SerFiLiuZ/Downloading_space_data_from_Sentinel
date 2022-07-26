from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


def downloading_space_data(domen_, source_, lat_, lng_, zoom_, preset_, layers_, maxcc_, gain_, gamma_, time_,
                           atmFilter_, showDates_, path_to_folder_download, path_to_folder_images, name_file):
    # Формирование url
    global sort_date_list
    domen = domen_
    source = 'source=' + source_
    lat = 'lat=' + lat_
    lng = 'lng=' + lng_
    zoom = 'zoom=' + zoom_
    preset = 'preset=' + preset_
    layers = 'layers=' + layers_
    maxcc = 'maxcc=' + maxcc_
    gain = 'gain=' + gain_
    gamma = 'gamma=' + gamma_
    times = 'time=' + time_
    atmFilter = 'atmFilter=' + atmFilter_
    showDates = 'showDates=' + showDates_

    url_buff = "{}&{}&{}&{}&{}&{}&{}&{}&{}&{}&{}&{}".format(source, lat, lng, zoom, preset, layers, maxcc, gain, gamma,
                                                            times, atmFilter, showDates)

    url = domen + '/?' + url_buff

    # Открытие браузера и переход по url
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(url)

    # XPATH пути до трёх кнопок - принятие полититки, сгенерировать изображение, скачать изображение
    xpath_for_Terms_of_Service_and_Privacy_Policy = '/html/body/div/div/div/div[1]/div[2]/div/div/div[2]/div[1]'
    xpath_for_generate_image = '/html/body/div[1]/div/div/div[5]/footer/div[1]/button'
    xpath_for_download_image = '/html/body/div[1]/div/div/div[7]/div[2]/div/div[2]/a'

    # XPATH пути до элементов страницы, после прогрузки которых, нажатие на кнопки ошибок не вызовет
    xpath_for_rendering_menu = '/html/body/div[1]/div/div/div[5]/div/article/div/div/div[1]/div/a[10]/img'
    xpath_for_loading_wheel = '/html/body/div[1]/div/div/div[7]/div[2]/div/div[1]/span'

    # Нажатие на кнопку принятия политики после загрузки сайта
    while True:
        try:
            driver.find_element(By.XPATH, xpath_for_Terms_of_Service_and_Privacy_Policy).click()
            print('btn 0 - press')
            break
        except:
            print("btn 0 - no press")
            time.sleep(.3)

    # Ожидание возможности корректно сгенерировать изображениe
    while True:
        try:
            driver.find_element(By.XPATH, xpath_for_rendering_menu)
            break
        except:
            print("rendering menu not found")
            time.sleep(.3)

    # Нажатие на кнопку генерации изображения
    while True:
        try:
            driver.find_element(By.XPATH, xpath_for_generate_image).click()
            print('btn 1 - press')
            break
        except:
            print("btn 1 - no press")
            time.sleep(.3)

    # Проверка загрузки конечного изображения для возможности скачивания
    while True:
        try:
            driver.find_element(By.XPATH, xpath_for_loading_wheel)
        except:
            break

    # Нажатие на кнопку скачивания изображения
    while True:
        try:
            driver.find_element(By.XPATH, xpath_for_download_image).click()
            print('btn 2 - press')
            break
        except:
            print("btn 2 - no press")
            time.sleep(.3)

    # Перенос скаченного файла из папки Загрузки в заданную папку
    import os
    import shutil

    # Цикл будет выполняться до тех пор, пока файл не скачается полностью
    while True:
        try:
            dir_list = [os.path.join(path_to_folder_download, x) for x in os.listdir(path_to_folder_download)]

            if dir_list:
                # Создадим список из путей к файлам и дат их создания.
                date_list = [[x, os.path.getctime(x)] for x in dir_list]

                # Отсортируем список по дате создания в обратном порядке
                sort_date_list = sorted(date_list, key=lambda x: x[1], reverse=True)

            # Перенос файла в заданную папку
            original_path = sort_date_list[0][0]
            des = shutil.move(original_path, path_to_folder_images)
            print('File transfer has been ' + path_to_folder_images)
            break
        except:
            time.sleep(.3)

    # Создание нового имени файла
    file_old_name = des
    file_newname_newfile = os.path.join(path_to_folder_images, name_file + '&'
                                        + preset + '&'
                                        + zoom + '&'
                                        + lat + '&'
                                        + lng + ".jpg")

    # Переименование нового файла в конечной папке
    os.rename(file_old_name, file_newname_newfile)
    print('The file has been renamed. new name - '
          + name_file + '&'
          + preset + '&'
          + zoom + '&'
          + lat + '&'
          + lng + ".jpg")

    # Удаление файлов типа tmp (Может быть появление файлов этого типа следует из ошибки при переносе файла, но при этом, конечные файла открываются корректно)
    tmp_count = 0
    for file_for_remove in os.listdir(path_to_folder_images):
        if not file_for_remove.endswith(".tmp"):
            continue
        os.remove(os.path.join(path_to_folder_images, file_for_remove))
        tmp_count = tmp_count + 1

    print('Files with the extension .tmp deleted. count deleted - ' + str(tmp_count))

    # Выход из браузера
    driver.quit()
