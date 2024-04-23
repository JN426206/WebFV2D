Narzędzie do uruchomienia narzędzia FV2D jako usługi internetowej.

Wymaga środowiska `python >= 3.7`, `miniconda`, `cuda` oraz systemu `linux`   
Wymaga stworzenia środowiska conda (dokładna instrukcja instalacji opisana została w pliku [FV2D/README.md](FV2D/README.md#tworzenie-środowiska-tv2d))   

Po zainstalowaniu wymaganych zależności oraz stworzeniu środowiska FV2D należy przejść do głównego katalogu tego repozytorium i wykonać polecenia:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Zalecane jest aby nagrania wideo przetwarzać pojedyńczo.


## Licencja

Narzędzie WebFV2D wydane zostało na licencji [Apache 2.0](FV2D/LICENSE).

## Autor narzędzia
mgr inż. Jan Nowak   
email: 95jan.nowak@gmail.com   
Uniwersytet im. Adama Mickiewicza w Poznaniu   
Wydział Matematyki i Informatyki    
Promotor: prof. UAM dr hab. Krzysztof Dyczkowski   
Narzędzie powstało przy współpracy z klubem sportowym KKS Lech Poznań   
<p align="center">
    <img src="FV2D/images_repo/brands.png"/>
</p>

Narzedzie stworzone i wykorzystywane na potrzeby przedmiotu "Projekt badawczo-rozwojowy" oraz na użytek dla klubu sportowego KKS Lech Poznań
