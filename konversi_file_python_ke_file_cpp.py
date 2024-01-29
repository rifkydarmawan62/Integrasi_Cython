from tkinter.filedialog import askopenfilename as pilih_file
from subprocess import run, CalledProcessError
from colorama import Fore, Back
from platform import system
from os.path import exists
from os import remove

def bersihkan_layar(teks : str | None = None):
    if system() == "Windows":
        run("cls", shell = True)
    else:
        run("clear", shell = True)
    if teks:
        print(teks)
bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi kompiler Cython ...{Fore.RESET}")
error : bool = False
try:
    run("cython --version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Kompiler Cython tidak ditemukan!")
    error = True
    PERINTAH_INSTALASI_CYTHON = "pip install cython" if system() == "Windows" else "pip3 install cython"
    print(f"{Fore.YELLOW}Menjalankan perintah instalasi Cython {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH_INSTALASI_CYTHON}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
    try:
        run(PERINTAH_INSTALASI_CYTHON, shell = True, check = True)
    except CalledProcessError:
        print(f"{Fore.LIGHTRED_EX}Gagal menginstal Cython!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Instalasi Cython dihentikan!{Fore.RESET}")
    else:
        print(f"{Fore.LIGHTGREEN_EX}Selesai menginstal Cython{Fore.RESET}")
        error = False
except Exception:
    error = True
if not error:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    file_input = pilih_file(title = "Pilih file Python untuk dikonversi ke file cpp", defaultextension = ".py", filetypes = [("Kode sumber Python", "*.py *.pyx")])
    if file_input:
        DIREKTORI_FOLDER = "/".join(file_input.split("/")[:-1])
        NAMA_FILE_OUTPUT = ".".join(file_input.split("/")[-1].split(".")[:-1]) + ".cpp"
        file_output = f"{DIREKTORI_FOLDER}/{NAMA_FILE_OUTPUT}"
        if system() == "Windows":
            file_input = file_input.replace("/", "\\")
            file_output = file_output.replace("/", "\\")
        PERINTAH = f"cython --output-file \"{file_output}\" -3 --embed --cplus --force --gdb --verbose \"{file_input}\""
        print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
        try:
            run(PERINTAH, shell = True, check = True)
        except CalledProcessError:
            print(f"{Fore.LIGHTRED_EX}Kompilasi Gagal!{Fore.RESET}")
            if exists(file_output):
                remove(file_output)
        except KeyboardInterrupt:
            print(f"{Fore.LIGHTRED_EX}Kompilasi Dihentikan!{Fore.RESET}")
            if exists(file_output):
                remove(file_output)
        else:
            print(f"{Fore.LIGHTGREEN_EX}Kompilasi Berhasil!{Fore.RESET}")
    else:
        print(f"{Fore.LIGHTRED_EX}File Python tidak dipilih{Fore.RESET}")