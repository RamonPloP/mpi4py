from flask import Flask, render_template, request
from mpi4py import MPI
import numpy as np
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def binary_search(arr, target):

    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def parallel_quicksort(arr):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Dividir los datos
    local_data = np.array_split(arr, size)[rank]

    # Ordenar localmente
    sorted_local = quicksort(local_data)

    # Recopilar los datos ordenados
    sorted_data = comm.gather(sorted_local, root=0)

    if rank == 0:
        # Combinar los datos ordenados
        sorted_array = np.concatenate(sorted_data)
        return sorted_array
    else:
        return None

@app.route('/')

def index():
    data = {
    "title": "Proyecto MPI4py",
    "datos": [1,2,3,4,5]
}
    return render_template('index.html', data=data)

@app.route('/web')

def web():
    data = {
    "title": "Web Scrapping",
    "datos": [1,2,3,4,5]
}
    return render_template('web.html', data=data)

@app.route('/webres', methods=['POST'])

def webres():        
    # Inicialización de MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Obtener la URL para hacer scraping
    url = request.form['url']

    # Procesa la URL asignada a este proceso
    results = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text_content = '\n'.join(p.get_text() for p in paragraphs)
    results.append(text_content)

    # Recolecta los resultados de todos los procesos
    gathered_results = comm.gather(results, root=0)

    # El proceso raíz combina los resultados e imprime la salida
    if rank == 0:
        combined_results = []
        for process_results in gathered_results:
            combined_results.extend(process_results)

        # Combina todos los textos en un solo texto
        combined_text = '\n'.join(combined_results)

    print(combined_text)

    data = {
    "title": "Web Scrapping",
    "datos": [1,2,3,4,5],
    "texto": combined_text
}
    return render_template('webres.html', data=data)

#---------------------------------------------------------------------

@app.route('/binary')

def binary():
    data = {
    "title": "Binary Search",
    "datos": [1,2,3,4,5]
}
    return render_template('binary.html', data=data)

@app.route('/binaryres', methods=["POST"])

def binaryres():
    # Arreglo de ejemplo (debe estar ordenado)
    arr = np.array(list(map(int, request.form['datos'].split(','))))
    arr.sort()
    sorted(arr)
    # Elemento a buscar
    target = int(request.form['target'])

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Dividir el arreglo en partes iguales
    chunk_size = len(arr) // size
    local_arr = np.zeros(chunk_size, dtype=int)

    # Distribuir partes del arreglo a cada proceso
    comm.Scatter(arr, local_arr, root=0)

    # Realizar búsqueda binaria en cada parte del arreglo
    result = binary_search(local_arr, target)

    # Reunir los resultados de todos los procesos en el proceso raíz
    all_results = comm.gather(result, root=0)

    # Mostrar el resultado en el proceso raíz
    if rank == 0:
        for i, res in enumerate(all_results):
            if res != -1:
                msg = f"El elemento {target} fue encontrado en el índice {res}."
            else:
                msg = f"El elemento {target} no fue encontrado."

    data = {
    "title": "Binary Search",
    "msg": msg

}
    return render_template('binaryres.html', data=data)

#---------------------------------------------------------------------

@app.route('/quick')
def quick():
    data = {
        "title": "Quick Sort",
        "datos": [1, 2, 3, 4, 5]
    }
    return render_template('quick.html', data=data)

@app.route('/quickres', methods=["POST"])
def quickres():
    # Obtener los datos del formulario y convertirlos en un arreglo de enteros
    arr = np.array(list(map(int, request.form['datos'].split(','))))

    # Realizar el ordenamiento utilizando QuickSort
    sorted_arr = parallel_quicksort(arr)

    # Preparar los datos para mostrar en la plantilla
    if sorted_arr is not None:
        sorted_str = ','.join(map(str, sorted_arr))
        msg = f"Arreglo ordenado: {sorted_str}"
    else:
        msg = "Error al procesar los datos"

    data = {
        "title": "Quick Sort",
        "msg": msg
    }

    return render_template('quickres.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)