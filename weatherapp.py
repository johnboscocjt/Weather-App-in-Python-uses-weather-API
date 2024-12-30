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
        api_key = "7d6e21ba6effd79456d23bc5sdfsdsa198"
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
                    print("Bad request\nPlease check your input")
                    
                case 401:
                    print("Unauthorized\nInvalid API key")
                    
                case 403:
                    print("Forbidden\nAccess is denied")
                    
                case 404:
                    print("Not found\nCity not found")
                    
                case 500:
                    print("Internal server error\nPlease try again later")
                    
                case 502:
                    print("Bad gateway\nInvalid response from the server")
                    
                case 503:
                    print("Service unavailable\nServer is down")
                    
                case 504:
                    print("gateway timeout\nNo response from the server")
                    
                case __:
                    print(f"HTTP error occurred\n{http_error}")
        
        except requests.exceptions.ConnectionError:
            print("Connection Error:\nCheck your internet connection")
        
        except requests.exceptions.Timeout:
            print("Timeout error:\nThe requesttimed out")
        
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects\nCheck the url")
        
        except requests.exceptions.RequestException as req_error:
            print("Request error:\n{req_error }")
    
    def display_error(self, message):
        pass
    
    def display_weather(self, data):
        pass     

# if we are running main python directly, create the weather app object
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
    
