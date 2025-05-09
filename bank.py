"""
Gelişmiş Bankamatik Simülasyonu
Bu proje, gerçek bir bankamatik deneyimini simüle eden kapsamlı bir uygulamadır.
"""

import time
import random
import sys
from datetime import datetime

class BankAccount:
    def __init__(self, name, surname, account_no, password, balance=0):
        self.name = name
        self.surname = surname
        self.account_no = account_no
        self.password = password
        self.balance = balance
        self.transaction_history = []
        self.login_attempts = 0
        self.is_locked = False
        self.last_login = None
    
    def add_transaction(self, transaction_type, amount, target_account=None):
        transaction = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': transaction_type,
            'amount': amount,
            'balance_after': self.balance,
            'target_account': target_account
        }
        self.transaction_history.append(transaction)
    
    def view_account_info(self):
        print("\n" + "="*50)
        print(f"HESAP BİLGİLERİ".center(50))
        print("="*50)
        print(f"Ad Soyad: {self.name} {self.surname}")
        print(f"Hesap No: {self.account_no}")
        print(f"Bakiye: {self.balance:.2f} TL")
        print(f"Son Giriş: {self.last_login}" if self.last_login else "İlk Giriş")
        print("="*50 + "\n")
        time.sleep(2)
    
    def withdraw(self, amount):
        if self.is_locked:
            print("Hesabınız geçici olarak kilitlenmiştir. Bankanızla iletişime geçin.")
            return False
        
        if amount <= 0:
            print("Geçersiz miktar girdiniz.")
            return False
            
        if amount > self.balance:
            print("Yetersiz bakiye!")
            return False
            
        if amount > 10000:  # Günlük limit kontrolü
            print("Günlük çekim limitiniz 10,000 TL'dir.")
            return False
            
        self.balance -= amount
        self.add_transaction('Para Çekme', amount)
        print(f"\n{amount:.2f} TL çekiliyor... Lütfen paranızı alınız.")
        print(f"Yeni bakiye: {self.balance:.2f} TL")
        time.sleep(2)
        return True
    
    def deposit(self, amount):
        if amount <= 0:
            print("Geçersiz miktar girdiniz.")
            return False
            
        self.balance += amount
        self.add_transaction('Para Yatırma', amount)
        print(f"\n{amount:.2f} TL yatırıldı.")
        print(f"Yeni bakiye: {self.balance:.2f} TL")
        time.sleep(2)
        return True
    
    def transfer(self, target_account, amount):
        if self.is_locked:
            print("Hesabınız geçici olarak kilitlenmiştir. Bankanızla iletişime geçin.")
            return False
            
        if amount <= 0:
            print("Geçersiz miktar girdiniz.")
            return False
            
        if amount > self.balance:
            print("Yetersiz bakiye!")
            return False
            
        if amount > 20000:  # Günlük transfer limiti
            print("Günlük transfer limitiniz 20,000 TL'dir.")
            return False
            
        self.balance -= amount
        target_account.balance += amount
        self.add_transaction('Para Transferi (Gönderilen)', amount, target_account.account_no)
        target_account.add_transaction('Para Transferi (Alınan)', amount, self.account_no)
        
        print(f"\n{amount:.2f} TL, {target_account.name} {target_account.surname} adlı kişiye transfer edildi.")
        print(f"Yeni bakiye: {self.balance:.2f} TL")
        time.sleep(2)
        return True
    
    def view_transaction_history(self):
        print("\n" + "="*50)
        print(f"İŞLEM GEÇMİŞİ".center(50))
        print("="*50)
        
        if not self.transaction_history:
            print("Henüz işlem geçmişi bulunmamaktadır.")
        else:
            for idx, transaction in enumerate(self.transaction_history[-10:], 1):  # Son 10 işlem
                print(f"{idx}. {transaction['date']} - {transaction['type']}")
                print(f"   Miktar: {transaction['amount']:.2f} TL")
                if transaction['target_account']:
                    print(f"   Hedef Hesap: {transaction['target_account']}")
                print(f"   Bakiye: {transaction['balance_after']:.2f} TL")
                print("-"*50)
        
        print("="*50 + "\n")
        time.sleep(3)
    
    def change_password(self, new_password):
        if len(new_password) != 5 or not new_password.isdigit():
            print("Şifre 5 haneli rakamlardan oluşmalıdır.")
            return False
            
        self.password = new_password
        print("Şifreniz başarıyla değiştirildi.")
        time.sleep(1)
        return True
    
    def login(self, entered_password):
        if self.is_locked:
            print("Hesabınız geçici olarak kilitlenmiştir. Bankanızla iletişime geçin.")
            return False
            
        if entered_password == self.password:
            self.login_attempts = 0
            self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True
        else:
            self.login_attempts += 1
            if self.login_attempts >= 3:
                self.is_locked = True
                print("3 başarısız giriş denemesi. Hesabınız kilitlendi.")
            else:
                print(f"Yanlış şifre! Kalan deneme hakkı: {3 - self.login_attempts}")
            return False

class ATM:
    def __init__(self):
        # Örnek hesaplar oluşturuyoruz
        self.accounts = [
            BankAccount("Ahmet", "Yılmaz", "123456", "11111", 15000),
            BankAccount("Mehmet", "Kaya", "654321", "22222", 25000),
            BankAccount("Ayşe", "Demir", "987654", "33333", 5000)
        ]
        self.current_account = None
    
    def find_account(self, account_no):
        for account in self.accounts:
            if account.account_no == account_no:
                return account
        return None
    
    def show_welcome_screen(self):
        print("\n" + "="*50)
        print("BANKAMATİK SİSTEMİNE HOŞGELDİNİZ".center(50))
        print("="*50)
        print("Lütfen kartınızı takınız (hesap numarası giriniz)\n")
    
    def show_main_menu(self):
        while True:
            print("\n" + "="*50)
            print("ANA MENÜ".center(50))
            print("="*50)
            print(f"Hoşgeldiniz, {self.current_account.name} {self.current_account.surname}")
            print("1 - Hesap Bilgileri")
            print("2 - Para Çekme")
            print("3 - Para Yatırma")
            print("4 - Para Transferi")
            print("5 - İşlem Geçmişi")
            print("6 - Şifre Değiştirme")
            print("0 - Çıkış")
            print("="*50)
            
            try:
                choice = int(input("Lütfen işlem seçiniz (0-6): "))
                
                if choice == 1:
                    self.current_account.view_account_info()
                elif choice == 2:
                    self.withdraw_money()
                elif choice == 3:
                    self.deposit_money()
                elif choice == 4:
                    self.transfer_money()
                elif choice == 5:
                    self.current_account.view_transaction_history()
                elif choice == 6:
                    self.change_password()
                elif choice == 0:
                    print("Çıkış yapılıyor... Kartınızı almayı unutmayınız.")
                    time.sleep(2)
                    self.current_account = None
                    break
                else:
                    print("Geçersiz seçim! Lütfen 0-6 arası bir sayı giriniz.")
            except ValueError:
                print("Geçersiz giriş! Lütfen bir sayı giriniz.")
    
    def withdraw_money(self):
        print("\n" + "="*50)
        print("PARA ÇEKME".center(50))
        print("="*50)
        print("Mevcut Bakiye:", self.current_account.balance)
        
        try:
            amount = float(input("\nÇekilecek miktarı giriniz: "))
            if amount <= 0:
                print("Geçersiz miktar!")
                return
                
            self.current_account.withdraw(amount)
        except ValueError:
            print("Geçersiz miktar!")
    
    def deposit_money(self):
        print("\n" + "="*50)
        print("PARA YATIRMA".center(50))
        print("="*50)
        
        try:
            amount = float(input("\nYatırılacak miktarı giriniz: "))
            if amount <= 0:
                print("Geçersiz miktar!")
                return
                
            # Para yatırma simülasyonu
            print("Lütfen paranızı yatırma bölmesine yerleştiriniz...")
            time.sleep(2)
            print("Paranız sayılıyor...")
            time.sleep(2)
            
            self.current_account.deposit(amount)
        except ValueError:
            print("Geçersiz miktar!")
    
    def transfer_money(self):
        print("\n" + "="*50)
        print("PARA TRANSFERİ".center(50))
        print("="*50)
        print("Mevcut Bakiye:", self.current_account.balance)
        
        target_account_no = input("\nTransfer edilecek hesap numarasını giriniz: ")
        target_account = self.find_account(target_account_no)
        
        if not target_account:
            print("Hesap bulunamadı!")
            return
            
        print(f"\nHesap Sahibi: {target_account.name} {target_account.surname}")
        confirm = input("Transferi onaylıyor musunuz? (E/H): ").upper()
        
        if confirm != 'E':
            print("Transfer iptal edildi.")
            return
            
        try:
            amount = float(input("\nTransfer miktarını giriniz: "))
            if amount <= 0:
                print("Geçersiz miktar!")
                return
                
            self.current_account.transfer(target_account, amount)
        except ValueError:
            print("Geçersiz miktar!")
    
    def change_password(self):
        print("\n" + "="*50)
        print("ŞİFRE DEĞİŞTİRME".center(50))
        print("="*50)
        
        old_password = input("Mevcut şifrenizi giriniz: ")
        if old_password != self.current_account.password:
            print("Mevcut şifreniz yanlış!")
            return
            
        new_password = input("Yeni şifrenizi giriniz (5 haneli rakam): ")
        confirm_password = input("Yeni şifrenizi tekrar giriniz: ")
        
        if new_password != confirm_password:
            print("Şifreler uyuşmuyor!")
            return
            
        self.current_account.change_password(new_password)
    
    def run(self):
        while True:
            self.show_welcome_screen()
            account_no = input("Hesap No: ").strip()
            
            account = self.find_account(account_no)
            if not account:
                print("Hesap bulunamadı!")
                time.sleep(2)
                continue
                
            if account.is_locked:
                print("Bu hesap kilitlenmiş. Bankanızla iletişime geçin.")
                time.sleep(2)
                continue
                
            attempts = 0
            logged_in = False
            
            while attempts < 3:
                password = input("Şifrenizi giriniz: ").strip()
                if account.login(password):
                    logged_in = True
                    break
                attempts += 1
                
            if not logged_in:
                continue
                
            self.current_account = account
            self.show_main_menu()

# ATM'yi başlat
if __name__ == "__main__":
    atm = ATM()
    try:
        atm.run()
    except KeyboardInterrupt:
        print("\nProgram sonlandırılıyor...")
        sys.exit(0)
