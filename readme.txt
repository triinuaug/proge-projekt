K�ETUVASTUS ALPHA

Programmi t��tamiseks on tarvis j�rgmisi mooduleid: os, sys, pywin32, win32api, win32con, 
win32gui_struct, winxpgui/win32gui, tkinter, ctypes, comtypes, pycaw.pycaw, statistics, 
cv2 (opencv versioon 4.1.1), imutils, numpy, math, sklearn.metrics, itertools, 
multiprocessing, wmi

Programmi avamisel tekib system tray-sse ikoon, kus on valikud. 
Sealt parema hiireklikiga men�� valides saab s�ttida k�e asendid vastavusse funktsioonidega.
Kui men��st on valitud "Salvesta", aktiveerub pildit��tlus. 

! Selle koodiga on kaasas testimisaken, et sa saaks aru, kuhu k�e panema peab,
selle saab v�lja kommenteerida, asukoht RIDA 127.
!vahel j��b kogemata kaamera t��le, siis saab task managerist panna "python"-i kinni,
see sulgeb kaamera, et uuesti testida

Pildit��tlus v�tab kaamera vaatev�lja vasakust �lemisest nurgast v�lja osa,
mida see t��tlema hakkab. Selle aja jooksul(kuni 5 sekundit), kui kaamera
salvestab tausta, ei tohi seal olla liikumist ega kasutajat ees. Peale seda aega
peab kasutaja terve labak�e asetama t��tlusalasse ja hoidma p�sti teatud n�ppude arvu,
kuni programm on vastava funktsiooni k�ivitanud.

Iga 15ne kaadri tagant arvutatakse keskmine m��detud n�ppude arv ja see otsustab, 
mis funktsioon k�ivitatakse.

#�ldiselt salvestab tausta paari sekundiga ja saab v�ga t�pselt n�ppudest aru,
aga k�ik oleneb su keskkonnast, valgusest ja arvuti kiirusest, niiet tulemused
v�ivad varieeruda. 
