KÄETUVASTUS ALPHA

Programmi töötamiseks on tarvis järgmisi mooduleid: os, sys, pywin32, win32api, win32con, 
win32gui_struct, winxpgui/win32gui, tkinter, ctypes, comtypes, pycaw.pycaw, statistics, 
cv2 (opencv versioon 4.1.1), imutils, numpy, math, sklearn.metrics, itertools, 
multiprocessing, wmi

Programmi avamisel tekib system tray-sse ikoon, kus on valikud. 
Sealt parema hiireklikiga menüü valides saab sättida käe asendid vastavusse funktsioonidega.
Kui menüüst on valitud "Salvesta", aktiveerub pilditöötlus. 

! Selle koodiga on kaasas testimisaken, et sa saaks aru, kuhu käe panema peab,
selle saab välja kommenteerida, asukoht RIDA 127.
!vahel jääb kogemata kaamera tööle, siis saab task managerist panna "python"-i kinni,
see sulgeb kaamera, et uuesti testida

Pilditöötlus võtab kaamera vaatevälja vasakust ülemisest nurgast välja osa,
mida see töötlema hakkab. Selle aja jooksul(kuni 5 sekundit), kui kaamera
salvestab tausta, ei tohi seal olla liikumist ega kasutajat ees. Peale seda aega
peab kasutaja terve labakäe asetama töötlusalasse ja hoidma püsti teatud näppude arvu,
kuni programm on vastava funktsiooni käivitanud.

Iga 15ne kaadri tagant arvutatakse keskmine mõõdetud näppude arv ja see otsustab, 
mis funktsioon käivitatakse.

#üldiselt salvestab tausta paari sekundiga ja saab väga täpselt näppudest aru,
aga kõik oleneb su keskkonnast, valgusest ja arvuti kiirusest, niiet tulemused
võivad varieeruda. 
