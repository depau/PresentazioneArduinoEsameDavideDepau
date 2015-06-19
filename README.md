# Presentazione per l'Esame di Stato su Arduino di Davide Depau

Questa presentazione verrà presentata da Davide Depau durante gli orali dell'Esame di maturità. È scritta in Python e utilizza come Kivy come interfaccia grafica per essere multipiattaforma.

Testata su GNU/Linux (Ubuntu 15.04), Android 5.1 e Windows 7, dovrebbe funzionare anche su Mac OS X e iOS, se opportunamente compilata e se è installato un codec video supportato da Kivy in grado di leggere video OGG (Theora+Vorbis) o MP4 (x256+AAC).

## Requisiti di sistema

* Sistema operativo GNU/Linux, Windows 7+, Android 2.3+, Mac OS X (non testato).
* Circa 200 MB liberi su Android, e GNU/Linux, almeno 1.5 GB su Windows.
* Scheda grafica che supporti OpenGL 2.0+
* Almeno 200 MB di memorai RAM su GNU/Linux e Android, 500 MB su Windows.

## Utilizzo su GNU/Linux

* Visitare http://kivy.org/#download e installare Kivy per la propria distribuzione
* Assicurarsi di avere installato GStreamer 0.10 o 1.0, oppure FFMPEG per la riproduzione dei video.
* Eseguire **main.py** (Arch Linux: assicurarsi che venga eseguito con Python 2.*!)

## Utilizzo su Windows

* Visitare http://kivy.org/#download e scaricare Kivy con Python 2.7 per la propria architettura.
* Estrarre il pacchetto scaricato in una cartella accessibile.
* Trascinare il file **main.py** sopra **kivy-2.7.bat** dentro la cartella di Kivy per avviare l'app.

## Compilazione per Android (solo da GNU/Linux)

* Scaricare e installare Buildozer: http://github.com/kivy/buildozer
* Collegare un dispositivo Android con il debug USB attivato.
* Eseguire nel terminale (dentro questo repository) `buildozer android debug deploy run`.


Seguire le istruzioni su http://kivy.org per utilizzarla anche su Mac OS X e iOS.

Il software è rilasciato sotto la licenza MIT. Il contenuto è rilasciato sotto la licenza Creative Commons Attribuzione.

Il video su "Years" è stato preso da https://vimeo.com/30501143

L'immagine della modella nella slide "Altre immagini", rilasciata sotto la licenza Creative Commons Attribution-NonCommercial-ShareAlike da Udo Klein, è stata presa da http://blog.blinkenlight.net/experiments/measurements/foto-trigger/