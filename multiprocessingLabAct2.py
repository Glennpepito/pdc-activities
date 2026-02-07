from multiprocessing import Process, Queue
import ipywidgets as widgets
from IPython.display import display
import time

def compute_gwa_process(pid, grades, queue):
    gwa = sum(grades) / len(grades)
    time.sleep(1)
    queue.put(f"Process {pid}: GWA = {gwa:.2f}")

subject_count = widgets.IntText(value=3, description="Subjects:")
grades_box = widgets.VBox()
grade_inputs = []

def generate_inputs(change=None):
    grade_inputs.clear()
    grades_box.children = ()
    for i in range(subject_count.value):
        g = widgets.FloatText(description=f"Grade {i+1}:")
        grade_inputs.append(g)
        grades_box.children += (g,)

generate_inputs()
subject_count.observe(generate_inputs, names="value")

run_button = widgets.Button(description="Compute GWA (Multiprocessing)")
output = widgets.Output()

def run_multiprocessing(b):
    output.clear_output()
    grades = [g.value for g in grade_inputs]
    queue = Queue()
    processes = []
    start = time.time()
    for i in range(3):
        p = Process(target=compute_gwa_process, args=(i + 1, grades, queue))
        processes.append(p)
        p.start()
    with output:
        for _ in range(3):
            print(queue.get())
    for p in processes:
        p.join()
    end = time.time()
    with output:
        print(f"Execution Time: {end - start:.4f} seconds")

run_button.on_click(run_multiprocessing)

display(subject_count, grades_box, run_button, output)
