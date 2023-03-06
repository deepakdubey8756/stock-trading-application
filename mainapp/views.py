from django.shortcuts import render
from yahoo_fin.stock_info import * 
import queue
from threading import Thread

def stockpicker(request):
    stock_picker = tickers_nifty50()
    # print(stock_picker)
    return render(request, "mainapp/stockpicker.html", {'stockpicker': stock_picker})


def stocktracker(request):
    """
        >>>> Get the selected stock list.
        >>>> Check if they are in our availble stock options.
        >>>> if they are availble in stock options
        >>>> then get their data and update into dictionary.
    """
    stockPicker = request.GET.getlist("stockpicker")
    newStockPicker = []
    # print(stockPicker)
    availbleData = tickers_nifty50()
    for i in stockPicker:
        if i in availbleData:
            newStockPicker.append(i)
    
    data = {}
    n_thread = len(newStockPicker)
    thread_list = []
    que = queue.Queue()

    for i in range(n_thread):
        thread = Thread(target = lambda q, arg1: q.put({newStockPicker[i]: get_quote_table(arg1)}), args = (que, newStockPicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    
    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)

    print(data)
    return render(request, "mainapp/stocktracker.html", {"data":data})