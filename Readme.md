# Achordarte


## TODO

* Uniformizar en el codigo la notacion de las notas (americano o latino)
* Agregar mas Proto acordes (inversiones de mayores y menores, septimas y sus inversiones)
* Agregarle soporte de argumentos al programa principal (acordi.py) con la biblioteca argparse
  https://docs.python.org/3/howto/argparse.html#id1 , https://docs.python.org/3/library/argparse.html
  * Recibe el nombre del archivo de entrada como argumento no opcional (achordi.py /dev/snd/midiC1D0) 
  * Recibe el nombre de un archivo de salida como argumento opcional (achordi.py --store-input foo.rec )
* Support MIDI files (SMF, .mid) as input