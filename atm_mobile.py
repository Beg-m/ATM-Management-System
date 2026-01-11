#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATM Management System - Mobile Application
Final Project - Python Programming
Developed with Kivy
"""

import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

# User information stored in dictionary structure
users = {
    "1234567890": {
        "password": "1234",
        "balance": 5000.0
    },
    "2345678901": {
        "password": "2345",
        "balance": 3500.0
    },
    "3456789012": {
        "password": "3456",
        "balance": 8200.0
    },
    "4567890123": {
        "password": "4567",
        "balance": 1200.0
    },
    "5678901234": {
        "password": "5678",
        "balance": 9500.0
    }
}

# File name
TRANSACTION_FILE = "transactions.txt"

# Login attempt counter (resets for each screen)
login_attempts = 0
MAX_ATTEMPTS = 3

# Current user card number
current_card_number = None

# Current language (default: English)
current_language = "en"

# Translations dictionary
translations = {
    "en": {
        "welcome": "WELCOME TO ATM",
        "select_language": "SELECT LANGUAGE",
        "card_number": "Card Number:",
        "password": "Password:",
        "card_hint": "Enter your card number",
        "password_hint": "Enter your password",
        "login": "LOGIN",
        "register": "REGISTER",
        "register_screen": "REGISTER",
        "initial_balance": "Initial Balance:",
        "initial_balance_hint": "Enter initial balance",
        "register_btn": "REGISTER",
        "card_exists": "Card number already exists!",
        "register_success": "Registration successful!\nYou can now login.",
        "back_to_login": "BACK TO LOGIN",
        "back_to_menu": "BACK TO MENU",
        "back": "BACK",
        "logout": "LOGOUT",
        "main_menu": "MAIN MENU",
        "view_balance": "1. VIEW BALANCE",
        "deposit": "2. DEPOSIT",
        "withdraw": "3. WITHDRAW",
        "exit": "4. EXIT",
        "back_to_menu": "BACK TO MENU",
        "balance_screen": "VIEW BALANCE",
        "current_balance": "Current Balance:",
        "deposit_screen": "DEPOSIT",
        "deposit_amount": "Enter the amount you want to deposit ($):",
        "deposit_hint": "Enter amount",
        "deposit_btn": "DEPOSIT",
        "withdraw_screen": "WITHDRAW",
        "withdraw_amount": "Enter the amount you want to withdraw ($):",
        "withdraw_hint": "Enter amount",
        "withdraw_btn": "WITHDRAW",
        "fill_fields": "Please fill in all fields!",
        "wrong_password": "Wrong password! Remaining attempts: {}",
        "invalid_card": "Invalid card number! Remaining attempts: {}",
        "locked_password": "You entered wrong password 3 times.\nSystem temporarily locked.",
        "locked_card": "You made 3 wrong login attempts.\nSystem temporarily locked.",
        "enter_amount": "Please enter an amount!",
        "amount_greater_zero": "Amount must be greater than 0!",
        "valid_amount": "Please enter a valid amount!",
        "insufficient_balance": "Insufficient balance! Current: ${}",
        "deposit_success": "${} deposited successfully.\nNew balance: ${}",
        "withdraw_success": "${} withdrawn successfully.\nRemaining balance: ${}",
        "error": "ERROR",
        "success": "SUCCESS",
        "close": "Close",
        "exit_msg": "Exit",
        "safe_day": "Have a safe day!",
        "error_occurred": "An error occurred: {}",
        "view_balance_tx": "View Balance",
        "deposit_tx": "Deposit",
        "withdraw_tx": "Withdraw"
    },
    "tr": {
        "welcome": "ATM'YE HOŞ GELDİNİZ",
        "select_language": "DİL SEÇİNİZ",
        "card_number": "Kart Numaranız:",
        "password": "Şifreniz:",
        "card_hint": "Kart numaranızı giriniz",
        "password_hint": "Şifrenizi giriniz",
        "login": "GİRİŞ YAP",
        "register": "KAYIT OL",
        "register_screen": "KAYIT OL",
        "initial_balance": "Başlangıç Bakiyesi:",
        "initial_balance_hint": "Başlangıç bakiyesini giriniz",
        "register_btn": "KAYIT OL",
        "card_exists": "Kart numarası zaten kayıtlı!",
        "register_success": "Kayıt başarılı!\nArtık giriş yapabilirsiniz.",
        "back_to_login": "GİRİŞ EKRANINA DÖN",
        "back_to_menu": "ANA MENÜYE DÖN",
        "back": "GERİ",
        "logout": "ÇIKIŞ YAP",
        "main_menu": "ANA MENÜ",
        "view_balance": "1. BAKİYE GÖRÜNTÜLEME",
        "deposit": "2. PARA YATIRMA",
        "withdraw": "3. PARA ÇEKME",
        "exit": "4. ÇIKIŞ",
        "back_to_menu": "ANA MENÜYE DÖN",
        "balance_screen": "BAKİYE GÖRÜNTÜLEME",
        "current_balance": "Güncel Bakiyeniz:",
        "deposit_screen": "PARA YATIRMA İŞLEMİ",
        "deposit_amount": "Yatırmak istediğiniz tutarı giriniz (TL):",
        "deposit_hint": "Tutar giriniz",
        "deposit_btn": "PARA YATIR",
        "withdraw_screen": "PARA ÇEKME İŞLEMİ",
        "withdraw_amount": "Çekmek istediğiniz tutarı giriniz (TL):",
        "withdraw_hint": "Tutar giriniz",
        "withdraw_btn": "PARA ÇEK",
        "fill_fields": "Lütfen tüm alanları doldurunuz!",
        "wrong_password": "Yanlış şifre! Kalan deneme: {}",
        "invalid_card": "Geçersiz kart numarası! Kalan deneme: {}",
        "locked_password": "3 kez yanlış şifre girdiniz.\nSistem geçici olarak kilitlendi.",
        "locked_card": "3 kez yanlış giriş yaptınız.\nSistem geçici olarak kilitlendi.",
        "enter_amount": "Lütfen bir tutar giriniz!",
        "amount_greater_zero": "Tutar 0'dan büyük olmalıdır!",
        "valid_amount": "Geçerli bir tutar giriniz!",
        "insufficient_balance": "Yetersiz bakiye! Mevcut: {} TL",
        "deposit_success": "{} TL yatırıldı.\nYeni bakiyeniz: {} TL",
        "withdraw_success": "{} TL çekildi.\nKalan bakiyeniz: {} TL",
        "error": "HATA",
        "success": "BAŞARILI",
        "close": "Kapat",
        "exit_msg": "Çıkış",
        "safe_day": "Güvenli bir gün dileriz!",
        "error_occurred": "Bir hata oluştu: {}",
        "view_balance_tx": "Bakiye Görüntüleme",
        "deposit_tx": "Para Yatırma",
        "withdraw_tx": "Para Çekme"
    }
}


def get_text(key):
    """
    Gets translated text for the current language.
    """
    global current_language
    return translations[current_language].get(key, key)


def save_transaction(card_number, transaction_type, amount, balance):
    """
    Saves transactions to transactions.txt file.
    """
    try:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Use English for transaction file
        currency = "$" if current_language == "en" else "TL"
        
        with open(TRANSACTION_FILE, "a", encoding="utf-8") as file:
            file.write(f"{timestamp} | Card: {card_number} | Transaction: {transaction_type} | "
                      f"Amount: {currency}{amount:.2f} | Balance: {currency}{balance:.2f}\n")
    except Exception as e:
        print(f"Error saving transaction: {e}")


def show_popup(title, message):
    """
    Shows a popup message.
    """
    content = BoxLayout(orientation='vertical', padding=10, spacing=10)
    content.add_widget(Label(text=message, text_size=(400, None), halign='center', valign='middle'))
    
    btn_close = Button(text=get_text("close"), size_hint_y=None, height=40)
    popup = Popup(
        title=title,
        content=content,
        size_hint=(0.8, 0.4),
        auto_dismiss=False
    )
    btn_close.bind(on_press=popup.dismiss)
    content.add_widget(btn_close)
    popup.open()


class LanguageSelectionScreen(Screen):
    """
    Language selection screen - First screen when app starts.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=50,
            spacing=40
        )
        
        # Spacer at top
        main_layout.add_widget(BoxLayout(size_hint_y=0.25))
        
        # Main title - ATM Management System Secure Banking
        main_title = Label(
            text='ATM Management System\nSecure Banking',
            font_size=36,
            size_hint_y=None,
            height=150,
            bold=True,
            color=(1, 1, 1, 1),  # White text
            text_size=(300, None),
            halign='center',
            valign='middle'
        )
        main_layout.add_widget(main_title)
        
        # Subtitle - Language selection
        subtitle = Label(
            text='SELECT LANGUAGE / DİL SEÇİNİZ',
            font_size=20,
            size_hint_y=None,
            height=50,
            color=(0.8, 0.9, 1, 1),  # Light blue text
            text_size=(300, None),
            halign='center'
        )
        main_layout.add_widget(subtitle)
        
        # Spacer
        main_layout.add_widget(BoxLayout(size_hint_y=0.1))
        
        # Button container
        button_container = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint_y=None,
            height=180
        )
        
        # English button - Blue gradient style
        btn_english = Button(
            text='English',
            size_hint_y=None,
            height=80,
            background_color=(0.2, 0.4, 0.8, 1),  # Bright blue
            background_normal='',
            background_down='',
            font_size=26,
            bold=True,
            color=(1, 1, 1, 1)  # White text
        )
        btn_english.bind(on_press=self.select_english)
        button_container.add_widget(btn_english)
        
        # Turkish button - Darker blue
        btn_turkish = Button(
            text='Türkçe',
            size_hint_y=None,
            height=80,
            background_color=(0.15, 0.3, 0.7, 1),  # Darker blue
            background_normal='',
            background_down='',
            font_size=26,
            bold=True,
            color=(1, 1, 1, 1)  # White text
        )
        btn_turkish.bind(on_press=self.select_turkish)
        button_container.add_widget(btn_turkish)
        
        main_layout.add_widget(button_container)
        
        # Spacer at bottom
        main_layout.add_widget(BoxLayout(size_hint_y=0.3))
        
        self.add_widget(main_layout)
    
    def select_english(self, instance):
        """
        Sets language to English and goes to login screen.
        """
        global current_language
        current_language = "en"
        self.manager.current = 'login'
    
    def select_turkish(self, instance):
        """
        Sets language to Turkish and goes to login screen.
        """
        global current_language
        current_language = "tr"
        self.manager.current = 'login'


class LoginScreen(Screen):
    """
    Login screen - Login with card number and password.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = None
        self.title_label = None
        self.card_label = None
        self.password_label = None
        self.card_input = None
        self.password_input = None
        self.login_btn = None
        self.register_btn = None
        self.back_btn = None
        self.info_label = None
        
        self.build_ui()
        
        # Reset global attempt counter
        global login_attempts
        login_attempts = 0
    
    def build_ui(self):
        """
        Builds the UI elements.
        """
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Title
        self.title_label = Label(
            text=get_text("welcome"),
            font_size=32,
            size_hint_y=None,
            height=60,
            bold=True
        )
        self.layout.add_widget(self.title_label)
        
        # Card number
        self.card_label = Label(text=get_text("card_number"), size_hint_y=None, height=30)
        self.layout.add_widget(self.card_label)
        self.card_input = TextInput(
            multiline=False,
            hint_text=get_text("card_hint"),
            size_hint_y=None,
            height=50,
            input_filter='int'
        )
        self.layout.add_widget(self.card_input)
        
        # Password
        self.password_label = Label(text=get_text("password"), size_hint_y=None, height=30)
        self.layout.add_widget(self.password_label)
        self.password_input = TextInput(
            multiline=False,
            password=True,
            hint_text=get_text("password_hint"),
            size_hint_y=None,
            height=50
        )
        self.layout.add_widget(self.password_input)
        
        # Login button
        self.login_btn = Button(
            text=get_text("login"),
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.6, 0.9, 1)
        )
        self.login_btn.bind(on_press=self.login)
        self.layout.add_widget(self.login_btn)
        
        # Register button
        self.register_btn = Button(
            text=get_text("register"),
            size_hint_y=None,
            height=60,
            background_color=(0.3, 0.5, 0.8, 1)
        )
        self.register_btn.bind(on_press=self.go_to_register)
        self.layout.add_widget(self.register_btn)
        
        # Back to language selection button
        self.back_btn = Button(
            text=get_text("back"),
            size_hint_y=None,
            height=50,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'language'))
        self.layout.add_widget(self.back_btn)
        
        # Info label
        self.info_label = Label(
            text='',
            size_hint_y=None,
            height=40,
            color=(1, 0, 0, 1)
        )
        self.layout.add_widget(self.info_label)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        """
        Updates UI when entering the screen.
        """
        if self.title_label:
            self.title_label.text = get_text("welcome")
        if self.card_label:
            self.card_label.text = get_text("card_number")
        if self.password_label:
            self.password_label.text = get_text("password")
        if self.card_input:
            self.card_input.hint_text = get_text("card_hint")
        if self.password_input:
            self.password_input.hint_text = get_text("password_hint")
        if self.login_btn:
            self.login_btn.text = get_text("login")
        if self.register_btn:
            self.register_btn.text = get_text("register")
        if self.back_btn:
            self.back_btn.text = get_text("back")
    
    def go_to_register(self, instance):
        """
        Navigates to register screen.
        """
        self.manager.current = 'register'
    
    def login(self, instance):
        """
        Checks login credentials.
        """
        global login_attempts, current_card_number
        
        card_number = self.card_input.text.strip()
        password = self.password_input.text.strip()
        
        if not card_number or not password:
            self.info_label.text = get_text("fill_fields")
            return
        
        # Card number check
        if card_number in users:
            # Password check
            if users[card_number]["password"] == password:
                # Successful login
                current_card_number = card_number
                login_attempts = 0
                self.card_input.text = ''
                self.password_input.text = ''
                self.info_label.text = ''
                self.manager.current = 'menu'
            else:
                # Wrong password
                login_attempts += 1
                remaining = MAX_ATTEMPTS - login_attempts
                if remaining > 0:
                    self.info_label.text = get_text("wrong_password").format(remaining)
                else:
                    show_popup(get_text("error"), get_text("locked_password"))
                    login_attempts = 0
        else:
            # Invalid card number
            login_attempts += 1
            remaining = MAX_ATTEMPTS - login_attempts
            if remaining > 0:
                self.info_label.text = get_text("invalid_card").format(remaining)
            else:
                show_popup(get_text("error"), get_text("locked_card"))
                login_attempts = 0


class RegisterScreen(Screen):
    """
    Register screen - Register new user with card number, password, and initial balance.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = None
        self.title_label = None
        self.card_label = None
        self.password_label = None
        self.balance_label = None
        self.card_input = None
        self.password_input = None
        self.balance_input = None
        self.register_btn = None
        self.back_btn = None
        self.info_label = None
        
        self.build_ui()
    
    def build_ui(self):
        """
        Builds the UI elements.
        """
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Title
        self.title_label = Label(
            text=get_text("register_screen"),
            font_size=32,
            size_hint_y=None,
            height=60,
            bold=True
        )
        self.layout.add_widget(self.title_label)
        
        # Card number
        self.card_label = Label(text=get_text("card_number"), size_hint_y=None, height=30)
        self.layout.add_widget(self.card_label)
        self.card_input = TextInput(
            multiline=False,
            hint_text=get_text("card_hint"),
            size_hint_y=None,
            height=50,
            input_filter='int'
        )
        self.layout.add_widget(self.card_input)
        
        # Password
        self.password_label = Label(text=get_text("password"), size_hint_y=None, height=30)
        self.layout.add_widget(self.password_label)
        self.password_input = TextInput(
            multiline=False,
            password=True,
            hint_text=get_text("password_hint"),
            size_hint_y=None,
            height=50
        )
        self.layout.add_widget(self.password_input)
        
        # Initial balance
        self.balance_label = Label(text=get_text("initial_balance"), size_hint_y=None, height=30)
        self.layout.add_widget(self.balance_label)
        self.balance_input = TextInput(
            multiline=False,
            hint_text=get_text("initial_balance_hint"),
            size_hint_y=None,
            height=50
        )
        self.layout.add_widget(self.balance_input)
        
        # Register button
        self.register_btn = Button(
            text=get_text("register_btn"),
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        self.register_btn.bind(on_press=self.register)
        self.layout.add_widget(self.register_btn)
        
        # Back to login button
        self.back_btn = Button(
            text=get_text("back_to_login"),
            size_hint_y=None,
            height=60,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        self.layout.add_widget(self.back_btn)
        
        # Info label
        self.info_label = Label(
            text='',
            size_hint_y=None,
            height=40,
            color=(1, 0, 0, 1)
        )
        self.layout.add_widget(self.info_label)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        """
        Updates UI when entering the screen.
        """
        if self.title_label:
            self.title_label.text = get_text("register_screen")
        if self.card_label:
            self.card_label.text = get_text("card_number")
        if self.password_label:
            self.password_label.text = get_text("password")
        if self.balance_label:
            self.balance_label.text = get_text("initial_balance")
        if self.card_input:
            self.card_input.hint_text = get_text("card_hint")
            self.card_input.text = ''
        if self.password_input:
            self.password_input.hint_text = get_text("password_hint")
            self.password_input.text = ''
        if self.balance_input:
            self.balance_input.hint_text = get_text("initial_balance_hint")
            self.balance_input.text = ''
        if self.register_btn:
            self.register_btn.text = get_text("register_btn")
        if self.back_btn:
            self.back_btn.text = get_text("back_to_login")
        if self.info_label:
            self.info_label.text = ''
    
    def register(self, instance):
        """
        Registers a new user.
        """
        global users
        
        card_number = self.card_input.text.strip()
        password = self.password_input.text.strip()
        balance_text = self.balance_input.text.strip()
        
        # Validate all fields
        if not card_number or not password or not balance_text:
            self.info_label.text = get_text("fill_fields")
            return
        
        # Check if card number already exists
        if card_number in users:
            self.info_label.text = get_text("card_exists")
            return
        
        # Validate balance
        try:
            initial_balance = float(balance_text)
            if initial_balance < 0:
                self.info_label.text = get_text("amount_greater_zero")
                return
        except ValueError:
            self.info_label.text = get_text("valid_amount")
            return
        
        # Add new user
        users[card_number] = {
            "password": password,
            "balance": initial_balance
        }
        
        # Success message
        show_popup(get_text("success"), get_text("register_success"))
        
        # Clear inputs
        self.card_input.text = ''
        self.password_input.text = ''
        self.balance_input.text = ''
        self.info_label.text = ''
        
        # Go back to login screen after a short delay
        # (In Kivy, we can navigate immediately)
        self.manager.current = 'login'


class MenuScreen(Screen):
    """
    Main menu screen - ATM operations menu.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = None
        self.title_label = None
        self.btn_balance = None
        self.btn_deposit = None
        self.btn_withdraw = None
        self.btn_exit = None
        self.btn_logout = None
        
        self.build_ui()
    
    def build_ui(self):
        """
        Builds the UI elements.
        """
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Title
        self.title_label = Label(
            text=get_text("main_menu"),
            font_size=32,
            size_hint_y=None,
            height=60,
            bold=True
        )
        self.layout.add_widget(self.title_label)
        
        # Balance button
        self.btn_balance = Button(
            text=get_text("view_balance"),
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        self.btn_balance.bind(on_press=lambda x: setattr(self.manager, 'current', 'balance'))
        self.layout.add_widget(self.btn_balance)
        
        # Deposit button
        self.btn_deposit = Button(
            text=get_text("deposit"),
            size_hint_y=None,
            height=60,
            background_color=(0.3, 0.5, 0.8, 1)
        )
        self.btn_deposit.bind(on_press=lambda x: setattr(self.manager, 'current', 'deposit'))
        self.layout.add_widget(self.btn_deposit)
        
        # Withdraw button
        self.btn_withdraw = Button(
            text=get_text("withdraw"),
            size_hint_y=None,
            height=60,
            background_color=(0.8, 0.5, 0.3, 1)
        )
        self.btn_withdraw.bind(on_press=lambda x: setattr(self.manager, 'current', 'withdraw'))
        self.layout.add_widget(self.btn_withdraw)
        
        # Exit button
        self.btn_exit = Button(
            text=get_text("exit"),
            size_hint_y=None,
            height=60,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        self.btn_exit.bind(on_press=self.exit_app)
        self.layout.add_widget(self.btn_exit)
        
        # Logout button (back to login)
        self.btn_logout = Button(
            text=get_text("logout"),
            size_hint_y=None,
            height=60,
            background_color=(0.6, 0.4, 0.2, 1)
        )
        self.btn_logout.bind(on_press=self.logout)
        self.layout.add_widget(self.btn_logout)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        """
        Updates UI when entering the screen.
        """
        if self.title_label:
            self.title_label.text = get_text("main_menu")
        if self.btn_balance:
            self.btn_balance.text = get_text("view_balance")
        if self.btn_deposit:
            self.btn_deposit.text = get_text("deposit")
        if self.btn_withdraw:
            self.btn_withdraw.text = get_text("withdraw")
        if self.btn_exit:
            self.btn_exit.text = get_text("exit")
        if self.btn_logout:
            self.btn_logout.text = get_text("logout")
    
    def logout(self, instance):
        """
        Logs out and returns to login screen.
        """
        global current_card_number
        current_card_number = None
        self.manager.current = 'login'
    
    def exit_app(self, instance):
        """
        Exits the application.
        """
        show_popup(get_text("exit_msg"), get_text("safe_day"))
        App.get_running_app().stop()


class BalanceScreen(Screen):
    """
    Balance display screen.
    """
    def on_enter(self):
        """
        Shows balance when entering the screen and saves the transaction.
        """
        global current_card_number
        
        if current_card_number and current_card_number in users:
            balance = users[current_card_number]["balance"]
            
            # Clear layout
            self.clear_widgets()
            
            layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
            
            # Title
            title = Label(
                text=get_text("balance_screen"),
                font_size=28,
                size_hint_y=None,
                height=50,
                bold=True
            )
            layout.add_widget(title)
            
            # Balance display
            currency = "$" if current_language == "en" else "TL"
            balance_label = Label(
                text=f'{get_text("current_balance")}\n{currency}{balance:.2f}',
                font_size=36,
                size_hint_y=None,
                height=150,
                bold=True,
                color=(0.2, 0.7, 0.3, 1)
            )
            layout.add_widget(balance_label)
            
            # Back to menu button
            btn_back = Button(
                text=get_text("back_to_menu"),
                size_hint_y=None,
                height=60,
                background_color=(0.5, 0.5, 0.5, 1)
            )
            btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
            layout.add_widget(btn_back)
            
            self.add_widget(layout)
            
            # Save transaction
            save_transaction(current_card_number, get_text("view_balance_tx"), 0.0, balance)


class DepositScreen(Screen):
    """
    Deposit screen.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = None
        self.title_label = None
        self.amount_label = None
        self.amount_input = None
        self.btn_deposit = None
        self.btn_back = None
        self.info_label = None
        
        self.build_ui()
    
    def build_ui(self):
        """
        Builds the UI elements.
        """
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Title
        self.title_label = Label(
            text=get_text("deposit_screen"),
            font_size=28,
            size_hint_y=None,
            height=50,
            bold=True
        )
        self.layout.add_widget(self.title_label)
        
        # Amount input
        self.amount_label = Label(text=get_text("deposit_amount"), size_hint_y=None, height=30)
        self.layout.add_widget(self.amount_label)
        self.amount_input = TextInput(
            multiline=False,
            hint_text=get_text("deposit_hint"),
            size_hint_y=None,
            height=50
        )
        self.layout.add_widget(self.amount_input)
        
        # Deposit button
        self.btn_deposit = Button(
            text=get_text("deposit_btn"),
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        self.btn_deposit.bind(on_press=self.deposit)
        self.layout.add_widget(self.btn_deposit)
        
        # Back to menu button
        self.btn_back = Button(
            text=get_text("back_to_menu"),
            size_hint_y=None,
            height=60,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(self.btn_back)
        
        # Info label
        self.info_label = Label(
            text='',
            size_hint_y=None,
            height=40,
            color=(1, 0, 0, 1)
        )
        self.layout.add_widget(self.info_label)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        """
        Updates UI when entering the screen.
        """
        if self.title_label:
            self.title_label.text = get_text("deposit_screen")
        if self.amount_label:
            self.amount_label.text = get_text("deposit_amount")
        if self.amount_input:
            self.amount_input.hint_text = get_text("deposit_hint")
        if self.btn_deposit:
            self.btn_deposit.text = get_text("deposit_btn")
        if self.btn_back:
            self.btn_back.text = get_text("back_to_menu")
    
    def deposit(self, instance):
        """
        Performs the deposit transaction.
        """
        global current_card_number
        
        try:
            amount_text = self.amount_input.text.strip()
            if not amount_text:
                self.info_label.text = get_text("enter_amount")
                return
            
            amount = float(amount_text)
            
            # Negative or zero check
            if amount <= 0:
                self.info_label.text = get_text("amount_greater_zero")
                return
            
            # Update balance
            if current_card_number and current_card_number in users:
                users[current_card_number]["balance"] += amount
                new_balance = users[current_card_number]["balance"]
                
                # Save transaction
                save_transaction(current_card_number, get_text("deposit_tx"), amount, new_balance)
                
                # Success message
                message = get_text("deposit_success").format(f"{amount:.2f}", f"{new_balance:.2f}")
                show_popup(get_text("success"), message)
                
                # Clear input
                self.amount_input.text = ''
                self.info_label.text = ''
        except ValueError:
            self.info_label.text = get_text("valid_amount")
        except Exception as e:
            show_popup(get_text("error"), get_text("error_occurred").format(str(e)))


class WithdrawScreen(Screen):
    """
    Withdraw screen.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = None
        self.title_label = None
        self.balance_label = None
        self.amount_label = None
        self.amount_input = None
        self.btn_withdraw = None
        self.btn_back = None
        self.info_label = None
        
        self.build_ui()
    
    def build_ui(self):
        """
        Builds the UI elements.
        """
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Title
        self.title_label = Label(
            text=get_text("withdraw_screen"),
            font_size=28,
            size_hint_y=None,
            height=50,
            bold=True
        )
        self.layout.add_widget(self.title_label)
        
        # Current balance display
        self.balance_label = Label(
            text='',
            size_hint_y=None,
            height=40,
            font_size=18
        )
        self.layout.add_widget(self.balance_label)
        
        # Amount input
        self.amount_label = Label(text=get_text("withdraw_amount"), size_hint_y=None, height=30)
        self.layout.add_widget(self.amount_label)
        self.amount_input = TextInput(
            multiline=False,
            hint_text=get_text("withdraw_hint"),
            size_hint_y=None,
            height=50
        )
        self.layout.add_widget(self.amount_input)
        
        # Withdraw button
        self.btn_withdraw = Button(
            text=get_text("withdraw_btn"),
            size_hint_y=None,
            height=60,
            background_color=(0.8, 0.5, 0.3, 1)
        )
        self.btn_withdraw.bind(on_press=self.withdraw)
        self.layout.add_widget(self.btn_withdraw)
        
        # Back to menu button
        self.btn_back = Button(
            text=get_text("back_to_menu"),
            size_hint_y=None,
            height=60,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(self.btn_back)
        
        # Info label
        self.info_label = Label(
            text='',
            size_hint_y=None,
            height=40,
            color=(1, 0, 0, 1)
        )
        self.layout.add_widget(self.info_label)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        """
        Shows current balance when entering the screen.
        """
        global current_card_number
        
        if self.title_label:
            self.title_label.text = get_text("withdraw_screen")
        if self.amount_label:
            self.amount_label.text = get_text("withdraw_amount")
        if self.amount_input:
            self.amount_input.hint_text = get_text("withdraw_hint")
        if self.btn_withdraw:
            self.btn_withdraw.text = get_text("withdraw_btn")
        if self.btn_back:
            self.btn_back.text = get_text("back_to_menu")
        
        if current_card_number and current_card_number in users:
            balance = users[current_card_number]["balance"]
            currency = "$" if current_language == "en" else "TL"
            self.balance_label.text = f'{get_text("current_balance")} {currency}{balance:.2f}'
    
    def withdraw(self, instance):
        """
        Performs the withdraw transaction.
        """
        global current_card_number
        
        try:
            amount_text = self.amount_input.text.strip()
            if not amount_text:
                self.info_label.text = get_text("enter_amount")
                return
            
            amount = float(amount_text)
            
            # Negative or zero check
            if amount <= 0:
                self.info_label.text = get_text("amount_greater_zero")
                return
            
            # Balance check
            if current_card_number and current_card_number in users:
                current_balance = users[current_card_number]["balance"]
                currency = "$" if current_language == "en" else "TL"
                
                if amount > current_balance:
                    self.info_label.text = get_text("insufficient_balance").format(f"{current_balance:.2f}")
                    return
                
                # Update balance
                users[current_card_number]["balance"] -= amount
                new_balance = users[current_card_number]["balance"]
                
                # Save transaction
                save_transaction(current_card_number, get_text("withdraw_tx"), amount, new_balance)
                
                # Success message
                message = get_text("withdraw_success").format(f"{amount:.2f}", f"{new_balance:.2f}")
                show_popup(get_text("success"), message)
                
                # Clear input and update balance
                self.amount_input.text = ''
                self.info_label.text = ''
                self.balance_label.text = f'{get_text("current_balance")} {currency}{new_balance:.2f}'
        except ValueError:
            self.info_label.text = get_text("valid_amount")
        except Exception as e:
            show_popup(get_text("error"), get_text("error_occurred").format(str(e)))


class ATMMobileApp(App):
    """
    Main application class.
    """
    def build(self):
        """
        Builds the application structure.
        """
        # Screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(LanguageSelectionScreen(name='language'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(BalanceScreen(name='balance'))
        sm.add_widget(DepositScreen(name='deposit'))
        sm.add_widget(WithdrawScreen(name='withdraw'))
        
        return sm


if __name__ == '__main__':
    # Set window size (mobile-like)
    Window.size = (400, 700)
    # Set window background color to match the design
    Window.clearcolor = (0.1, 0.2, 0.4, 1)  # Dark blue background
    ATMMobileApp().run()
