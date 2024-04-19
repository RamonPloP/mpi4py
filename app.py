from flask import Flask, render_template, request
from mpi4py import MPI
import numpy as np

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
                msg = f"El elemento {target} fue encontrado en el proceso {i} en el índice {res}."
            else:
                msg = f"El elemento {target} no fue encontrado en el proceso {i}."

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
    "datos": [1,2,3,4,5]
}
    return render_template('quick.html', data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)