def compound_average_growth_rate(arr):
    first = arr[0]
    last = arr[-1]
    periods = len(arr)
    return (last / first)**(1 / periods)-1


def data_handler(known_entries, predicted_entry=None):
    entries = known_entries[-2:]
    cagr_entries = compound_average_growth_rate(entries)
    if predicted_entry != None:
        cagr_all = compound_average_growth_rate([entries[-1]] + [predicted_entry])
    if cagr_entries <= -0.0006:
        return -1
    elif cagr_entries >= 0.0001:
        return 1
    else:
        return 0
