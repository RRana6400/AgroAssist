async function getWeather(city) {
  try {
    const response1 = await fetch(
      `http://api.openweathermap.org/geo/1.0/direct?q=${city}&limit=5&appid=494faa539456f414f3be9ca110a645da`,
    );
    const result = await response1.json();
    const lat = result[0].lat;
    const lon = result[0].lon;

    const weather_response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=494faa539456f414f3be9ca110a645da&units=metric`,
    );
    const weather_obj = await weather_response.json();

    const temperature = weather_obj.main.temp;
    const humidity = weather_obj.main.humidity ;
    const wind_speed = weather_obj.wind.speed ;
    const pressure = weather_obj.main.pressure ;
    const sunrise = weather_obj.sys.sunrise ;
    const sunset = weather_obj.sys.sunset ;
    const visibility = weather_obj.visibility ;
    const weather_condition = weather_obj.weather[0];

    

    document.getElementById("place-name-id").innerHTML = city.toString().toUpperCase();

    document.getElementById("weather-condition-id").innerHTML = weather_condition;
    document.getElementById("wind-speed-id").innerHTML = wind_speed;
    document.getElementById("sunrise-id").innerHTML = sunrise;
    document.getElementById("sunset-id").innerHTML = sunset;
    document.getElementById("pressure-id").innerHTML = pressure;
    document.getElementById("humidity-id").innerHTML = humidity;
    document.getElementById("visibility-id").innerHTML = visibility;
    

    // const weather_icon_code = weather_obj.weather[0].icon;

    // try {
    //   const weather = await fetch(
    //     `https://openweathermap.org/img/wn/${weather_icon_code}@2x.png`,
    //   );
    //   const weather_logo_ = document.getElementById("weather-id");
    //   weather_logo_.src = weather;

    //   console.log(weather_obj);
    // } catch (err) {
    //   console.warn("Weather Icon not found!");
    // }
  } catch (error) {
    console.log(error);
  }
}

let search_btn = document.getElementById("search-btn-id");

search_btn.addEventListener("click", (e) => {
  let city_name = document.getElementById("search-id").value;
  getWeather(city_name);
});
