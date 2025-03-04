## Взаимодействие с внешними Open API

- TheCatAPI  ([сайт API](thecatapi.com)) - бот c TOKEN_CW, который может искать и отправлять изображения и информацию о кошках по породе ([код бота](cats.py));
- NASA API ([сайт API](api.nasa.gov)) - бот TOKEN_CW, который отправляет случайное космическое изображение дня ([код бота](nasa.py));
- JokeAPI ([сайт API](https://github.com/benjhar/JokeAPI-Python#readme)) и gifAPI ([сайт API](https://tenor.com/gifapi)) - бот c TOKEN, который может подбирать GIF по ключевому слову и выдавать произвольную шутку [код бота](hw.py)

#### Добавьте токены своих ботов и ключи API  в config.py:
  ```bash
  TOKEN_CW = 'your-bot-token'
  API_CAT_KEY = 'your-API-key'
  API_NASA_KEY = 'your-API-key'
  
  TOKEN = 'your-bot-token'
  API_GIF = 'your-API-key'
  ``` 

#### Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
