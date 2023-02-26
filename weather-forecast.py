import requests
city = "Moscow,RU"
appid ="9563ac050fe3dce440f30bb732b930e4"
res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                   params={'q':city,'units':'metric','lang':'ru','APPID':appid})
data = res.json()
print("Прогноз победы на неделю:")
for i in data['list']:
    print("Дата<",i['dt_txt'],">\r\nТемпература<",'{0:+3.0f}'.format(i['main']['temp']),">\r\nПогодные условия<",i['weather'][0]['description'],">\r\nСкорость ветра<",i['wind']['speed'],">\r\nВидимость<",i['visibility'],">")
    print('_____________')