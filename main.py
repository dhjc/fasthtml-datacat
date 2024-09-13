from fasthtml.common import *

def render(dataset):
    tid = f'todo-{dataset.id}'
    toggle = A('Mark Favourite', hx_get=f'/toggle/{dataset.id}', target_id=tid)
    delete = A('Delete', hx_delete=f'/{dataset.id}', target_id=tid, hx_swap='outerHTML')

    return Li(toggle,delete,
              dataset.title + ' ' + dataset.apiendpoint + ' ' + dataset.docsurl + (' ⭐' if dataset.done else ''),
              id=tid)

app, rt, datasets, DataSet = fast_app('data/datacat.db', 
                                live=False,
                                render=render, 
                                id=int,
                                title=str,
                                apiendpoint=str,
                                docsurl=str,
                                url=str,
                                done=bool, 
                                pk='id',
                                )

def mk_input():
    return Input(placeholder='Add a new Dataset', id='title',
                 hx_swap_oob='true')

def mk_input2():
    return Input(placeholder='API Endpoint', id='apiendpoint',
                 hx_swap_oob='true')

def mk_input3():
    return Input(placeholder='Docs are Important', id='docsurl',
                 hx_swap_oob='true')

@rt("/")
def get():
    frm = Form((mk_input(),mk_input2(), mk_input3(),
                     Button("Add")),
            hx_post='/',
            target_id='dataset-list', hx_swap='beforeend')
    return Titled(
        'Data Catalog',
        Card(Ul(*datasets(), id='dataset-list'),
             header=frm)
    )



@rt("/{tid}")
def post(dataset:DataSet):
    return datasets.insert(dataset), mk_input(), mk_input2(),mk_input3()

@rt("/{tid}")
def delete(tid:int):
    datasets.delete(tid)


@rt("/toggle/{tid}")
def get(tid:int):
    todo = datasets[tid]
    todo.done = not todo.done
    return datasets.update(todo)


serve()