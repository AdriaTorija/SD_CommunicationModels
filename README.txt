# SD_CommunicationModels
Practica1

Autors: 
Xavier Roca Canals
Adrià Rubio Busquets
Adrià Torija Ruiz

---------------------

Github: https://github.com/hatori9/SD_CommunicationModels

Com ens hem repartit la feina
Xavier Roca Canals: Multitask i http. Per a que es puguin atendre tasques amb més d'un fitxer de manera dinàmica i connexió al server http.
Adrià Rubio Busquets: Creació de les funcions bàsiques del servidor/worker i comandes de l'usuari
Adrià Torija Ruiz: Creació de les funcions bàsiques del servidor/worker i comandes de l'usuari

En els commits només surten dos dels membres degut a que es va treballar conjuntament i es van utilizar un sol/dos ordinadors.

---------------------

Execució

Fitxers de prova: prova.txt, prova2.txt, prova3.txt

Crear worker -> client.py create
Esborrar worker -> client.py delete (id)
Llistar workers -> client.py list
Obtenir els resultats -> client.py result
Executar counting_words -> client.py job counting_words http://localhost:8000/prova.txt http://localhost:8000/prova2.txt http://localhost:8000/prova3.txt
Executar word_count -> client.py job word_count http://localhost:8000/prova.txt http://localhost:8000/prova2.txt http://localhost:8000/prova3.txt

---------------------

client.py

Descripció:
Fitxer per l'execució del client, a partir d'aquest farem diverses peticions al servidor.

Utilitzem les següents llibreries:
xmlrpc
click

Comandes/peticions:
create - Ens permet crear un worker
delete(X) - Ens permet esborrar el worker passat per paràmetre
list - Ens permet llistar els workers que hi ha al servidor
job word_count (X) - Ens permet crear una tasca que executarà la funció word_count amb els fitxers passats per paràmetre
job counting_words (X) - Ens permet crear una tasca que executarà la funció counting_words amb els fitxers passats per paràmetre
result - Ens permet visualitzar tots els resultats

---------------------

server.py

Descripció:
Fitxer per l'execució del servidor, aquest rebrà i executarà les peticions del client

Utilitzem les següents llibreries:
xmlrpc
multiprocessing
redis
json

Funcions:
create_worker: Crea un nou worker
delete_worker: Esborra un worker
list_workers: Llista tots els workers
create_task: Crea una nova tasca, aquesta s'encuarà a la cua de redis, per tal de respondre a múltiples fitxers passats per paràmetre
es crea una tasca per fitxer i finalment una última tasca per juntar el resultat. Encara que només hi hagi un fitxer també es crearà 
aqusta última tasca.
get_results: Retorna al client tots els resultats

---------------------

worker.py

Descripció:
Fitxer per l'execució dels workers, aquests són creats dins del servidor i executaran les funcions/jobs que ordeni el client

Utilitzem les següents llibreries:
json
urllib

Funcions:
start_worker: Inicia l'execució del worker, aquest té dos modes d'execució: 1. Executar la funció i 2. Juntar el resultat
create_result: Crea el resultat final, juntant tots els resultats obtinguts
read_file: Permet llegir el fitxer
counting_words: Compta quantes paraules hi ha en el fitxer passat per paràmetre
word_count: Compta quants cops surten les paraules en el fitxer passat per paràmetre
res_counting_words: Junta tots els resultats obtinguts a partir de counting_words
res_word_count: Junta tots els resultats obtinguts a partir de word_count
