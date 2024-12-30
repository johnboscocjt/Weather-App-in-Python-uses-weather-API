import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        # layout manager
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        # css
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        self.setStyleSheet("""
              QLabel, QPushButton{
                  font-family: calibri;
              }      
              QLabel#city_label{
                  font-size: 40px;
                  font-style: italic;
              }    
              QLineEdit#city_input{
                  font-size: 40px; 
              }   
              QPushButton#get_weather_button{
                  font-size: 30px;
                  font-weight: bold;
              }
              QLabel#temperature_label{
                    font-size: 75px;  
              }
              QLabel#emoji_label{
                  font-size: 100px;
                  font-family: Segeo UI emoji;
              }
              QLabel#description_label{
                  font-size: 50px;
              }
              
        """)
        
        # connecting signal to a slot
        self.get_weather_button.clicked.connect(self.get_weather)
    
    def get_weather(self):
        api_key = "7d6e21ba6effd79456d23bc5e8eba198"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)
            
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                    
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                    
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                    
                case 404:
                    self.display_error("Not found:\nCity not found")
                    
                case 500:
                    self.display_error("Internal server error:\nPlease try again later")
                    
                case 502:
                    self.display_error("Bad gateway:\nInvalid response from the server")
                    
                case 503:
                    self.display_error("Service unavailable:\nServer is down")
                    
                case 504:
                    self.display_error("gateway timeout:\nNo response from the server")
                    
                case __:
                    self.display_error(f"HTTP error occurred:\n{http_error}")
        
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe requesttimed out")
        
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the url")
        
        except requests.exceptions.RequestException as req_error:
            self.display_error("Request error:\n{req_error }")
    
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px")
        temperature_k = data["main"]["temp"]    
        temperature_c = temperature_k  - 273.4
        temperature_f = (temperature_k * 9/5) - 459.67
        # print(temperature_c)
        
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        
        
        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    # static method :they belong to a class, but dont require any instance
    @staticmethod
    def get_weather_emoji(weather_id):
        # if weather_id >= 200 and weather_id <= 232:
        if 200<= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 521:
            return "🌧️"
        elif 5600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 762:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""
        
        
        
# if we are running main python directly, create the weather app object
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
    