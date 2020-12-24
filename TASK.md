Parkking - King of the parking
=======

Wymagania
---------

System do rezerwacji parkingu. Bądź królem parkingu!

W najprostszej wersji użytkownik systemu ma do wyboru miejsca parkingowe. Identyfikatorem miejsca jest jego numer.
Użytkownik może zarezerwować miejsce w piątek po godzinie 15, sobotę lub niedzielę na dowolny dzień kolejnego tygodnia.
W dniach pn-pt może zarezerwować tylko na bieżący tydzień. Użytkownik może zarezerwować tylko jedno miejsce.
Admin ma możliwość zdefiniowania, które numery miejsc należą do której firmy.
Z systemu może korzystać więcej niż jedna firma.
Na potrzeby aplikacj można przyjąć górną granicę miejsc parkingowych dostępnych na parkingu: 1000.

W podstawowej wersji wystarczy rezerwacja na cały dzień, ale w bazie danych należy przewidzieć możliwośc rezerwowania na ustalone
godziny.

System powinien mieć widok terminarza, z dostępnymi miejscami.


Na co zwracamy uwagę:
---------------------
* łatwość instalacji i uruchomienia (opis w README.md)
* testy
* caly kod i dokumentacja powinne byc w jezyku angielskim
* iteratywne podejście odzwierciedlające się w merge requestach (każdy merge request z backendu powinien być przypisany do Kamil @ferene, z frontu do @czubik )
* pomysły na przyszłe ulepszenie (do dyskusji na spotkaniu)
* podstawowa dokumentacja (README.md)

Wymagania techniczne:
---------------------
* python3
* Django 3.x
* Docker
* Podstawowa implementacja po stronie frontu, najlepiej wykorzystując reactjs, material UI lub jeszcze lepiej - react native for web (wystarczy wersja na przeglądarkę, ale zachęcamy do eksperymentu i stworzenia wersji PWA lub na android/ios)
* Opcjonalnie - aplikacja powinna być dla celów demo deployowalna na aws (bezkosztowo, free tier)
